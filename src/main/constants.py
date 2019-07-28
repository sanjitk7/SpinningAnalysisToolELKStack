#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 10:20:19 2019

@author: eperiyasamy
"""
import queue

stop_processing = False
successfully_processed = False
notify_q = queue.Queue(maxsize = 30)
csv_filename = 'OEProductionReport.csv'
validation_config_file = '../config/data_validation.yaml'
processing_mode = 'sequential'
index_name='oe_index'

#Event types
os_error="OS_ERROR"
file_not_found="FILE_NOT_FOUND"
value_error="VALUE_ERROR"