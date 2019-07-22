#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 22:29:51 2019

@author: eperiyasamy
"""



root = tk.Tk()
root.geometry("100x50")

def close_window ():
    root.destroy()

button = tk.Button(text = "Click and Quit", command = close_window)
button.pack()

root.mainloop()