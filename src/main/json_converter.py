#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 12:32:34 2019

@author: eperiyasamy
"""

import constants

import csv
import json
import platform

import queue
import time
from threading import current_thread
import traceback

from UI_notification_queue import UINotification
from convert_to_json import connect_and_delete_index

import sys
#print("sys path:", sys.path)
from multiprocess import mp_persist_to_es

total_rows=0
processed_row=0

SUCCESS_EVENT = 'success'


def convert_to_json(filename,root):
    global processed_row
    global notify_q, glb_id
    
    # Initialize for every run as processed_row is a global variable
    processed_row=0
    
    rows=[]
    try:
        with open(filename) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        constants.stop_processing = True
        err_str = "File not found: " + filename
        err = (constants.file_not_found, err_str)
        constants.notify_q.put(err)
        return
    except EnvironmentError:
        constants.stop_processing = True
        err_str = "Enviornment error opening " + filename
        err = (constants.os_error, err_str)
        constants.notify_q.put(err)
        return
    
    with open('test.json', 'w') as f:
        json.dump(rows, f)
        
    connect_and_delete_index()
    
    create_machine_data(rows,root, filename)
    
    # publish event to UI event queue if processed successfully
    if not constants.stop_processing:
        constants.successfully_processed = True
        msg = (SUCCESS_EVENT, "")
        constants.notify_q.put(msg)
    
    # Change the state for other consumers
    constants.stop_processing = True
    glb_id = 0
    
def create_machine_data(rows,root, filename):
    global processed_row
    global total_rows
    
    total_rows= len(rows)
    
    try:
        if platform.system() == 'Windows':
             out_q = Queue()
             exc_q = Queue()
             resultlist = worker_process.worker(1, rows, exc_q, out_q)
        elif platform.system() == 'Darwin':
            resultlist = mp_persist_to_es(rows)
        else:
            raise Exception("Platform Unsupported")
            
    except Exception as e:
        constants.stop_processing = True
        err_str = "Bad data in " + filename
        err = (constants.value_error, err_str)
        constants.notify_q.put(err)
        return
        
    print ("resultlist:", resultlist)
    #print(rows[0])

#res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=1, body= machine1a_day1)
#res = es.get(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=1)
 
#convert_to_json("OEProductionChart.csv")