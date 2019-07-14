# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


try:
    import Tkinter as tk
    from Tkinter import *
except:
    import tkinter as tk
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    import progressbar as pb
    
#from requests.exceptions import ConnectionError
import time
import threading
import webbrowser
   
#import Tkinter, Tkconstants, tkFileDialog
import pandas as pd
import constants
from json_converter import convert_to_json
from UI_notification_queue import UINotification
#from PIL import ImageTK, Image
 
processing_started = False
total_rows = 0
processed_row = 0

root = tk.Tk(screenName = "OE Reporter",className = "OE REPORTS APPLICATION")
root.geometry("500x600")
root.lift()
#root.attributes('-topmost',True)
frame = tk.Frame(root).pack()
#self.Border = tk.Frame(self, relief='flat', borderwidth=4)

message = tk.StringVar()
source_of_csv_file = ""


error_message = tk.StringVar()
error_message.set('No Errors')

img = tk.PhotoImage(file="oeProdImg.gif")
img = img.zoom(3)
img=img.subsample(8)
img_lbl = tk.Label(root,image=img,bg='red')

img_logo = tk.PhotoImage(file="saraswathy_logo.gif")
title_label = tk.Label(root, text="Saraswathi Mills", image=img_logo, fg='green',height=170, width=400, relief=RAISED).pack(pady=10)

analytics_logo = tk.PhotoImage(file="analytics.gif")
analytics_logo = analytics_logo.zoom(2)
analytics_logo=analytics_logo.subsample(10)
analytics_lbl = tk.Label(root,image=analytics_logo)

l1 = tk.Label(root, text="File Not Uploaded")
error_lbl = tk.Label(root, text="Current Status: No Errors")
labelfont = ('times', 20, 'bold')

def upload():
    global source_of_csv_file
    
    btn2['state'] = 'disabled'
    btn3['state'] = 'disabled'
    
    constants.successfully_processed = False
    
    try:
        root.lift()
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("excel files","*.xlsx"),("all files","*.*")))
       
        if filename:
            data_xls = pd.read_excel(filename, 'Sheet1', index_col=None)
            data_xls.to_csv(constants.csv_filename, encoding='utf-8')
            source_of_csv_file = filename
            
            l1.config(text= filename + "\nSuccessfully Uploaded!",bg='green', fg='black', font=labelfont, height=3, width=10)
            l1.pack(expand=YES, fill=BOTH)
    except Exception as e:
        btn2['state'] = 'active'
        btn3['state'] = 'active'
        print ("exception:", str(e), ":", filename)
        if filename:
            l1.config(text= filename + "\nFailed Uploading\n" + str(e),bg='red', fg='black', font=labelfont, height=3, width=10)
            l1.pack(expand=YES, fill=BOTH)
            
    btn2['state'] = 'active'
    btn3['state'] = 'active'

def push_to_es():
    global processing_started
    
    constants.successfully_processed = False
    
    threadWork = threading.Thread(target=convert_to_json, args=(constants.csv_filename, root))
    thread_progress = threading.Thread(target=show_progress)
    
    if(btn2['text'] == "Start Processing"):
        constants.stop_processing = False
        btn1['state'] = 'disabled'
        btn3['state'] = 'disabled'
        
        try:
            processing_started = True
            btn2.config(text="Stop Processing")
            l1.config(text= constants.csv_filename + "\nProcessing...!",bg='green', fg='black', font=labelfont, height=3, width=10)
            threadWork.start()
            thread_progress.start()
            processing_started = False
            if not threadWork.is_alive():
                #Restore buttons state after successful processing
                btn1['state'] = 'active'
                btn2['state'] = 'active'
                btn3['state'] = 'active'
        except Exception as e:
            processing_started = False
            error_lbl.config(text="Error:" + str(e))
            error_lbl.pack(pady=10)
    else:
        constants.stop_processing = True
        if threadWork.is_alive():
            threadWork.join()
        if thread_progress.is_alive():
            thread_progress.join()
        constants.stop_processing = True
        btn2.config(text="Start Processing")
        btn1['state'] = 'active'
        btn3['state'] = 'active'
        

def close():
    global root
    root.destroy()
    
def callback(url):
    webbrowser.open_new(url)
    
def show_progress():
    global total_rows
    global processed_row
    global source_of_csv_file

    while not constants.stop_processing:
        l1.config(text= source_of_csv_file +"\nProcessing.",bg='green', fg='black', font=labelfont, height=3, width=10)
        l1.pack(expand=YES, fill=BOTH)
        if not constants.stop_processing:
            time.sleep(0.2)
        l1.config(text= source_of_csv_file + "\nProcessing. .",bg='green', fg='black', font=labelfont, height=3, width=10)
        l1.pack(expand=YES, fill=BOTH)
        if not constants.stop_processing:
            time.sleep(0.2)
        l1.config(text= source_of_csv_file + "\nProcessing. . .",bg='green', fg='black', font=labelfont, height=3, width=10)
        l1.pack(expand=YES, fill=BOTH)
        if not constants.stop_processing:
            time.sleep(0.2)
        l1.config(text= source_of_csv_file + "\nProcessing. . . .",bg='green', fg='black', font=labelfont, height=3, width=10)
        l1.pack(expand=YES, fill=BOTH)
        if not constants.stop_processing:
            time.sleep(0.2)
    l1.pack_forget()
        
def event_handler():
    while True:
        time.sleep(1)
        try:
            event_tuple = constants.notify_q.get()
            time.sleep(0.2)
            if event_tuple[0] == "success":
                btn1['state'] = 'active'
                btn2['state'] = 'active'
                btn3['state'] = 'active'
                btn2['text'] = "Start Processing"
                l1.config(text= "Data successfully processed. \nView Reports in Kibana",bg='green', fg='black', font=labelfont, height=3, width=10)
                l1.pack(expand=YES, fill=BOTH)
            elif event_tuple[0] ==constants.file_not_found:
                btn1['state'] = 'active'
                btn2['state'] = 'active'
                btn3['state'] = 'active'
                btn2['text'] = "Start Processing"
                time.sleep(0.1)
                l1.config(text= event_tuple[0] + "\nFailed Processing\n" + event_tuple[1],bg='red', fg='black', font=labelfont, height=3, width=10)
                l1.pack(expand=YES, fill=BOTH)
            elif event_tuple[0] == constants.os_error:
                btn1['state'] = 'active'
                btn2['state'] = 'active'
                btn3['state'] = 'active'
                btn2['text'] = "Start Processing"
                time.sleep(0.1)
                l1.config(text= event_tuple[0] + "\nFailed Processing\n" + event_tuple[1],bg='red', fg='black', font=labelfont, height=3, width=10)
                l1.pack(expand=YES, fill=BOTH)
            else:
                l1.config(text= "Unknown Error" + "\nFailed Processing\n",bg='red', fg='black', font=labelfont, height=3, width=10)
                l1.pack(expand=YES, fill=BOTH)
        except Exception:
            print ("no events to process")

btn1 = tk.Button(root, text = "Upload", command = upload, height=1, width=17,bg='blue')
btn1.pack(pady=10)

btn2 = tk.Button(root, text = "Start Processing", command=push_to_es, height=1, width=17,bg='blue')
btn2.pack(pady=10)

btn3 = tk.Button(root, text = "Close", command=close, height=1, width=17,bg='blue')
btn3.pack(pady=10)

link1 = tk.Label(root, text="Open Kibana", fg="blue", cursor="hand2")
link1.pack()
link1.bind("<Button-1>", lambda e: callback("http://localhost:5601"))

thread_event = threading.Thread(target=event_handler)
thread_event.setDaemon(True)
thread_event.start()


##initialize widgets
#widgets = ['Time for loop of 1 000 000 iterations: ', pb.Percentage(), ' ', 
#            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
##initialize timer
#timer = pb.ProgressBar(widgets=widgets, maxval=1000000).start()
#
##for loop example
#for i in range(0,1000000):
#    #update
#    timer.update(i)
##finish
#timer.finish()

#progress_frame = tk.Frame(root)
##progress_frame.grid()
#s = ttk.Style()
#s.theme_use('clam')
#s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
#p = ttk.Progressbar(root, style="red.Horizontal.TProgressbar", orient="horizontal", length=600, mode="determinate", maximum=4, value=1).grid(row=1, column=1)
#progress_frame.pack()

#popup = tk.Toplevel()
#progress_var = tk.DoubleVar()
#progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=total_rows, orient=HORIZONTAL,length=120, mode='determinate')
#progress_bar.pack(pady=10)
#popup.pack_slaves()
#
#while processing_started:
#    popup.update()
#    time.sleep(5) # lauch task
#    progress_var.set(processed_row)
        
        

root.configure(background='turquoise4')

if(constants.successfully_processed):
    l1.config(text= "Data successfully processed. \nView Reports in Kibana",bg='red', fg='black', font=labelfont, height=3, width=10)
    l1.pack(expand=YES, fill=BOTH)

#l1.pack(pady=10)

img_lbl.pack(side=BOTTOM)
analytics_lbl.pack(side=LEFT)

root.mainloop()

 
if __name__ == '__main__':
    print("Exiting OE Reports...Good Bye!")
    