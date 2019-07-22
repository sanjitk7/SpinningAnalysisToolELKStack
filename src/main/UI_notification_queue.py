#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 14:34:25 2019

@author: eperiyasamy
"""

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
#from show_button import processed_succesfully

import constants


class UINotification(threading.Thread):
    def __init__(self, q):
        self.q = q
        super(UINotification, self).__init__()                

    def pushEvent(self, event):
        self.q.put(event)
        print ("UI event pushed")

    def run(self):
        while True:
            try:
                function, args, kwargs = self.q.get(timeout=self.timeout)
                function(*args, **kwargs)
                print("run processed")
            except queue.Empty:
                self.idle()
                print("run empty")
            except Exception:
                print("exception")

    def pullEvent(self):
        print ("UI event pull")
        try:
            if not queue.Empty:
                event = self.q.get()
                return event
        except queue.empty:
            return "Q_EMPTY"
