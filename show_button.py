# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import tkinter as tk
from tkinter import filedialog
#import Tkinter, Tkconstants, tkFileDialog
import pandas as pd
from json_converter import convert_to_json
#from PIL import ImageTK, Image

CSV_FILENAME = 'OEProductionChart.csv'

root = tk.Tk(className = "button_click_label")
root.geometry("500x500")
root.lift()
root.attributes('-topmost',True)
#self.Border = tk.Frame(self, relief='flat', borderwidth=4)

message = tk.StringVar()
message.set('hi')

error_message = tk.StringVar()
error_message.set('No Errors')

img = tk.PhotoImage(file="oeProdImg.gif")

l1 = tk.Label(root, text="File Not Uploaded")
error_lbl = tk.Label(root, text="Current Status: No Errors")
img_lbl = tk.Label(image=img)


def upload():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("excel files","*.xlsx"),("all files","*.*")))
    print ("in upload: "+ filename)
    l1.config(text="File Successfully Uploaded!")
    data_xls = pd.read_excel(filename, 'Sheet1', index_col=None)
    data_xls.to_csv(CSV_FILENAME, encoding='utf-8')

def push_to_es():
	try:
		convert_to_json(CSV_FILENAME)
	except Exception as e:
		print(e)
		error_lbl.config(text="Error - Bad File Format: "+str(e))

def close():
	root.destroy()

b1 = tk.Button(root, text = "Upload", command = upload, height=3, width=17).pack(pady=10)
b2 = tk.Button(root, text = "Push To Elastic Search", command=push_to_es, height=3, width=17).pack(pady=10)
b3 = tk.Button(root, text = "Close", command=close, height=3, width=17).pack(pady=10)

l1.pack(pady=10)
error_lbl.pack(pady=10)
img_lbl.pack(expand=1)

root.mainloop()