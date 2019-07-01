
import tkinter as tk
from tkinter import filedialog
#import Tkinter, Tkconstants, tkFileDialog
import pandas as pd

CSV_FILENAME = 'OEProductionChart.csv'

root = Tk(className = "button_click_label")
root.geometry("500x500")

message = StringVar()
message.set('hi')

l1 = Label(root, text=" ")

def upload():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("excel files","*.xlsx"),("all files","*.*")))
    print (filename)
    l1.config(text=filename)
    data_xls = pd.read_excel(filename, 'Sheet1', index_col=None)
    data_xls.to_csv(CSV_FILENAME, encoding='utf-8')

def push_to_es():
    convert_to_json(CSV_FILENAME)

b1 = Button(root, text = "Upload", command = upload).pack()
b2 = Button(root, text = "Push To Elastic Search", command=push_to_es).pack()

l1.pack()

root.mainloop()