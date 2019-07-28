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
from worker_process import worker

def get_cpu_count():
    print ("cpu_count:", cpu_count())
    return cpu_count()

def mp_persist_to_es(rows):
    # Each process will get 'chunksize' nums and a queue to put his out
    # dict into
    out_q = Queue()
    exc_q = Queue()
    nprocs = get_cpu_count()
    if constants.processing_mode == "sequential":
        nprocs = 1
        
    chunksize = int(math.ceil(len(rows) / float(nprocs)))
    procs = []
    print ("__name__:", __name__)
    resultlist = []

    if __name__ == 'multiprocess':
        print ("__name__:", __name__)
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
        print("before for")
        for i in range(nprocs):
            resultlist.append(out_q.get())
    
        # Wait for all worker processes to finish
        print("before wait")
        for p in procs:
            print("p:", p)
            p.join()

    return resultlist