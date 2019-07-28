#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 19:21:09 2019

@author: eperiyasamy
"""
import yaml
import constants
import csv


def validate_csv_file(filename):
    rows=[]
    try:
        with open(filename) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        constants.stop_processing = True
        err_str = "File not found: " + filename
        err = (constants.file_not_found, err_str)
        constants.notify_q.put(err)
        return
    except EnvironmentError:
        constants.stop_processing = True
        err_str = "Enviornment error opening " + filename
        err = (constants.os_error, err_str)
        constants.notify_q.put(err)
        return
    
    config_dict = {}
    #read configuration yaml file
    with open(constants.validation_config_file) as f:
        doc = yaml.load(f)
        
    
    for key in doc:
        if isinstance(doc[key], str):
            l = doc[key].split()
            d = {}
            for item in l:
                d[item.split(':')[0]]=item.split(':')[1]
            
            config_dict[key] = d
        elif isinstance(doc[key], dict):
            config_dict[key] = doc[key]
        else: 
            raise Exception("Unsupported configuration")
            
    print (config_dict)
    print ("\n")
    
    new_dict = {}
    row_num = 0
    try:
        for row in rows:
            row_num += 1
            print ("row_num:" + str(row_num))
            for k in row:
                if "Unnamed"  not in k:
                    new_dict[k] = row[k]
                else:
                    #print(new_dict)
                    validate(row_num, new_dict,config_dict)
                    #time.sleep(1)
                    new_dict.clear()
    except Exception as e:
            print ("exception:" + str(e))
            raise e
            

def validate(row_num,d,config_dict):
    if len(d)==0 :
        return
    d1={}
    for i in d:
        d1[i.split(".")[0]] =d[i]

    if d1["cur_production"]=="" or d1["cur_production"]== 0:
        return
   
    for key in d:
        if key in config_dict:
            validate_data(row_num,(key,d[key]),config_dict[key])


def validate_data(row_num, input_data_tuple, config_dict):
    if(config_dict['data_type']) == 'enum':
        if(input_data_tuple[1] != ""):
            # check for allowed discrete value
            if (config_dict['required']) == True and input_data_tuple[1] == "":
                raise Exception("Validation Error:" + " a required data missing ".join(input_data_tuple) + "in row " + str(row_num))
            if input_data_tuple[1] not in config_dict["value"]:
                raise Exception("Validation Error:" + " has invalid enum ".join(input_data_tuple) + "in row " + str(row_num) )
    
    elif (config_dict['data_type'] == 'string'):
        if(input_data_tuple[1] != ""):
            # check for max and min length
            if(int(config_dict["min_length"]) > len(input_data_tuple[1])):
                raise Exception("Validation Error:" + " less than allowed min ".join(input_data_tuple) + "in row " + str(row_num))
            if(int(config_dict["max_length"]) < len(input_data_tuple[1])):
                raise Exception("Validation Error:" + " greater than allowed max ".join(input_data_tuple) + "in row " + str(row_num))
            
    elif (config_dict['data_type'] == 'numeric'):
        if(input_data_tuple[1] != ""):
            #check if value is a numeric value
            try:
                float(input_data_tuple[1])
            except ValueError:
                raise Exception("Validation Error:" + " not a numeric value ".join(input_data_tuple)+ "in row " + str(row_num))
            # check for min, max and required
            if(float(config_dict["min_value"]) > float(input_data_tuple[1])):
                raise Exception("Validation Error:" + " less than allowed min ".join(input_data_tuple) + "in row " + str(row_num))
            if(float(config_dict["max_value"]) < float(input_data_tuple[1])):
                raise Exception("Validation Error:" + " greater than allowed max ".join(input_data_tuple) + "in row " + str(row_num))
    return
        
#if __name__ == '__main__':
#    validate_csv_file(constants.csv_filename)