#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 15:41:51 2019

@author: eperiyasamy
"""

import unittest
 
class TestFileUpload(unittest.TestCase):
 
    def setUp(self):
        pass

    def test_validate_datatype(self):
        #open csv file
        
        
        #read rows
        
        
        self.assertEqual(edist((1,2), (3,4)),2.83)
   
#    def test_cluster_1_iteration(self):
#       prev=[(2,2),(8,2)]
#       centroid=[(2,3),(7,2)]
#       pop_pm=[(1,2),(1,3),(3,4),(3,3),(6,1),(6,3),(7,2),(8,3),(2,2),(2,4)]
#       cluster_dict={0:[(0,0),(0,1)],1:[(1,1),(2,2)]}
#       dict1={0: [(1, 2), (1, 3), (3, 4), (3, 3), (2, 2), (2, 4)], 1: [(6, 1), (6, 3), (7, 2), (8, 3)]}
#       self.assertDictEqual(cluster(prev,centroid,pop_pm,cluster_dict,2)[0],dict1)
#       self.assertListEqual(cluster(prev,centroid,pop_pm,cluster_dict,2)[1],centroid)

if __name__ == '__main__':
    unittest.main()





