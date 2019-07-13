#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 20:29:08 2019

@author: eperiyasamy
"""

try:
    raise Exception
except Exception as e:
    s,r = getattr(e, 'message', str(e)), getattr(e, 'message', repr(e))
    print ('s:', s, 'len(s):', len(s))
    print ('r:', r, 'len(r):', len(r))