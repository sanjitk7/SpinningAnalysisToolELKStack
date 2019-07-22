#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 16:35:33 2019

@author: eperiyasamy
"""

import math

import constants


from multiprocessing import cpu_count, Queue, Process
from convert_to_json import persist_to_es

def get_cpu_count():
    print ("cpu_count:", cpu_count())
    return cpu_count()

def mp_persist_to_es(rows):
    
    def worker(chunk_code, rows, exc_q, out_q):
        processed_row = 0
        new_dict = {}
        id_row = 0
        
        try:
            for row in rows:
                if constants.stop_processing:
                    break
                for k in row:
                    if "Unnamed"  not in k:
                        new_dict[k] = row[k]
                        
                    else:
                        #print(new_dict)
                        id_row += 1
                        persist_to_es(new_dict, chunk_code, id_row)
                        out_q.put((chunk_code,processed_row))
                        #time.sleep(1)
                        new_dict.clear()
                        processed_row += 1
        #                app.onThread(app.increment_progress_bar, processed_row)
                        if constants.stop_processing:
                            break
        except Exception as e:
            import sys
            exc_q.put(sys.exc_info())
            raise e

    # Each process will get 'chunksize' nums and a queue to put his out
    # dict into
    out_q = Queue()
    exc_q = Queue()
    nprocs = get_cpu_count()
    if constants.processing_mode == "sequential":
        nprocs = 1
        
    chunksize = int(math.ceil(len(rows) / float(nprocs)))
    procs = []

    for i in range(nprocs):
        print("i=",i)
        p = Process(
                target=worker,
                args=(i+1, rows[chunksize * i:chunksize * (i + 1)],
                      exc_q,out_q))
        procs.append(p)
        p.start()

    # Collect all results into a single result dict. We know how many dicts
    # with results to expect.
    resultlist = []
    print("before for")
    for i in range(nprocs):
        resultlist.append(out_q.get())

    # Wait for all worker processes to finish
    print("before wait")
    for p in procs:
        print("p:", p)
        p.join()

    return resultlist