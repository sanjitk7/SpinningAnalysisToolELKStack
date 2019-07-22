#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 17:43:16 2019

@author: eperiyasamy
"""
try:
    import Tkinter as tk
    from Tkinter import *
except:
    import tkinter as tk
    from tkinter import *

root = tk.Tk(className = "OE REPORTS APPLICATION")
root.geometry("500x500")
#root.lift()
#root.attributes('-topmost',True)
topFrame = tk.Frame(root,borderwidth=10)
topFrame.grid(column=0, row=0)

bottomFrame = Frame(root,bg="red",borderwidth=10)
bottomFrame.pack(side=BOTTOM)

button1 = Button(topFrame, text='Button 1', bg='red',activebackground='pink').grid(column=0, row=1)
button2 = Button(topFrame, text='Button 2', bg='blue',activebackground='pink').grid(column=0, row=2)
button3 = Button(topFrame, text='Button 3', bg='green', activebackground='pink').grid(column=0, row=3)

root.configure(background='black')
topFrame.configure(background='red')

#button1.pack(side=TOP)
#button2.pack(side=LEFT)
#button3.pack(side=BOTTOM)



imgpath = 'oeProdImg.gif'
img = tk.PhotoImage(file=imgpath)
img = img.zoom(10) #with 250, I ended up running out of memory
img = img.subsample(20) #mechanically, here it is adjusted to 32 instead of 320
panel = tk.Label(bottomFrame, image = img)
panel.pack(side = BOTTOM, fill = NONE, expand = YES)

root.mainloop()


root = tk.Tk()

frame = tk.Frame(root)
frame.grid(column=0, row=0)

tk.Button(frame, text="Open file", command=None,bg='red', fg='green').grid(column=0, row=1 )
lab = tk.Label(frame, text="test test test test test test ")
lab.grid(column=0, row=10)

root.configure(background='pink')
lab.configure(background='blue', foreground='white')
frame.configure(background='red')

root.mainloop()