#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 20:09:39 2019

@author: eperiyasamy
"""

import threading, time

# This is a global variable to hold our current progress
progress = 0

# This is a long running function that updates it's progress
def longProcess():
    global progress
    print ("longProcess:", threading.current_thread())
    for i in range(10000):
        time.sleep(0.0001)
        progress = i

# This function monitor's the other's progress
def getProgress():
    global progress
    print ("getprogress:", threading.current_thread())
    while progress < 9999:
        print (progress)
        time.sleep(0.3)

# Create a separate thread for the worker and the monitor
threadProgress = threading.Thread(target=getProgress)
threadWork = threading.Thread(target=longProcess)

# Start the worker and monitor
threadWork.start()
threadProgress.start()
print("main:", threading.current_thread())

# Wait for the work to finish
threadWork.join()
print ('Done')