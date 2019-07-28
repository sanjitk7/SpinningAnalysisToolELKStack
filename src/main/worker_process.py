#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 02:04:23 2019

@author: eperiyasamy
"""
import constants
from convert_to_json import persist_to_es


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