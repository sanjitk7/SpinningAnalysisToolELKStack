#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 00:54:57 2019

@author: eperiyasamy
"""

import queue
import threading
from threading import current_thread
import time
import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter.ttk import Progressbar

import constants

MAX=30

class SomeClass(threading.Thread):
    def __init__(self, q, total_rows, parent, loop_time = 1.0/60):
        self.q = q
        self.tk = tk
        self.root = tk.Tk()
        self.total_rows = total_rows
        self.timeout = loop_time
        self.progress_var=0
        self.popup = tk.Toplevel()
        self.parent = ttk.Frame(parent, padding="3 3 3 3")
        self.parent.pack()
        self.progress = Progressbar(self.parent,orient=HORIZONTAL,variable=self.progress_var, length=120, maximum=total_rows, mode='determinate',value=1)
        self.progress.grid(row=1,column=0)
        self.progress.start()
        #self.parent.pack_slaves()
        self.progress.pack()
        super(SomeClass, self).__init__()
        print ("ctr thread:", current_thread().name)
        
        

    def onThread(self, function, *args, **kwargs):
        self.q.put((function, args, kwargs))

    def run(self):
        while True:
            try:
                function, args, kwargs = self.q.get() #timeout=self.timeout)
                function(*args, **kwargs)
                print("run processed")
                if(constants.stop_processing == True):
                    break;
            except queue.Empty:
                self.idle()
                print("run empty")
            except Exception:
                print("exception")

    def idle(self):
        self.progress = Progressbar(self.parent,orient=HORIZONTAL,variable=self.progress_var, length=120, maximum=self.total_rows, mode='determinate')
        self.progress.grid(row=1,column=0)
        #self.progress.start()
        #self.btn = tk.Button(self, text='Traitement', command=self.traitement)
        #self.btn.grid(row=0,column=0)
        #self.progress = Progressbar(self, orient=HORIZONTAL,variable=self.progress_var, maximum=MAX)
        #self.btn['state']='disabled'
        #self.progress.grid(row=1,column=0)
        #self.progress.start()

    def increment_progress_bar(self,processed_row):
        print ("increment success")
        self.progress_var = processed_row
        print ("inc thread:", current_thread().name)
#        #time.sleep(1)
#        print("waiting in increment_progress_bar...",processed_row,":", self.total_rows)
#        #int_processed_row = int(processed_row,10)
#        if( processed_row == self.total_rows):
#            print ("in progress stop", flush=True)
#            self.progress.stop()
#            self.progress.grid_forget()
#            #self.btn['state']='normal'
#        else:
#            print ("in progress step",flush=True)
#            #self.progress.step(processed_row)
#            self.progress_var.set(processed_row)
#            print("updated progress bar...",flush=True)
