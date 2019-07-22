#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 13:47:05 2019

@author: eperiyasamy
"""

import queue
import threading
import time
import tkinter as tk
from tkinter import HORIZONTAL 
from tkinter.ttk import Progressbar

MAX = 30

class SomeClass1(threading.Thread):
    def __init__(self, q, root, total_rows, loop_time = 1.0/60):
        self.q = q
        self.timeout = loop_time
        self.total_rows = 50
        self.root1 = tk.Tk()
        self.root_ref = root
        self.processed = 0
        self.progress = Progressbar(root,orient=HORIZONTAL,variable=1, length=120)
        self.progress.config(maximum=MAX, mode='determinate',value=1)
        self.progress.step(1)
        self.progress.grid(row=0,column=1)
        super(SomeClass1, self).__init__()

    def onThread(self, function, *args, **kwargs):
        self.q.put((function, args, kwargs))

    def run(self):
        while True:
            try:
                function, args, kwargs = self.q.get(timeout=self.timeout)
                function(*args, **kwargs)
                print("run processed")
            except queue.Empty:
                self.idle()
                print("run empty")

    def idle(self):
        # put the code you would have put in the `run` loop here 
        print("idle")
        self.progress = Progressbar(self.root_ref,orient=HORIZONTAL,variable=self.processed, length=120)
        self.progress.config(maximum=MAX, mode='determinate',value=1)
        

    def doSomething(self,processed_row):
        global processed
        print("waiting in increment_progress_bar...", processed_row, ":", self.total_rows)
        #int_processed_row = int(processed_row,10)
        if( processed_row >= self.total_rows):
            print ("in progress stop")
            self.progress.stop()
            self.progress.grid_forget()
        else:
            print ("in progress step")
            #self.progress.step(processed_row)
            self.processed = processed_row
            print("updated progress bar...")

    def doSomethingElse(self,b):
        print("doSomethingElse",b)
        self.progress.step(1)
        time.sleep(2)
    
