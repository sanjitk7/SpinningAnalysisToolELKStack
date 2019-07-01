#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 12:32:34 2019

@author: eperiyasamy
"""

import csv
import json
import datetime
from elasticsearch import Elasticsearch

glb_id=0
carding_count = 0

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME='oe_index'
TYPE_NAME_MACHINE = 'machine'

es = Elasticsearch(hosts = [ES_HOST])
 

def convert_to_json(filename):
    global carding_count
    
    with open(filename) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    with open('test.json', 'w') as f:
        json.dump(rows, f)
        
        
    if es.indices.exists(INDEX_NAME):
        print("deleting '%s' index..." % (INDEX_NAME))
        res = es.indices.delete(index = INDEX_NAME)
        print(" response: '%s'" % (res))
    
    
    create_machine_data(rows)
    print("carding count:", carding_count)
    
def create_machine_data(rows):
    #print(rows[0])
    print("\n &&&&&&&&&&&&&&&&&&&&&&&7  \n")
    new_dict = {}
    i=0
    for row in rows:
        for k in row:
            if "Unnamed"  not in k:
                new_dict[k] = row[k]
            else:
                #print(new_dict)
                persist_to_es(new_dict)
                new_dict.clear()
              #  i+=1
               # if i==11:
               #     break
    
def format_date(date):
    return datetime.datetime.strptime(date,'%d.%m.%y').strftime('%Y-%m-%d')+ "T12:00:00"

def convert_to_int(number):
    return int(round(float(number),0))

def convert_to_float(number):
    return round(float(number),3)

def convert_to_float_2(number):
    return round(float(number),2)
        
    
    
def persist_to_es(d):
    global glb_id
    global carding_count
    
    #create machine data
    if len(d)==0 :
        return
    d1={}
    for i in d:
        d1[i.split(".")[0]] =d[i]

    if d1["cur_production"]=="" or d1["cur_production"]== 0:
        return
   
    json_machine_dict = {}
    
    json_machine_dict["type"]="machine"
    
    if "shift" in d1:
        json_machine_dict["shift"]=d1["shift"]
    
    if "machine_type" in d1:
        json_machine_dict["machine_type"] =d1["machine_type"]
        
    if json_machine_dict["machine_type"] == 'CARDING':
        carding_count += 1
        
    if "machine_id" in d1:
        json_machine_dict["machine_id"] =d1["machine_id"]
        
    if "godown" in d1:
        json_machine_dict["godown"] =d1["godown"]
        
    if "date" in d1 and d1["date"] != "":
        json_machine_dict["date"]=format_date(d1["date"])
        
    prod_dict = {}
    if "count" in d1:
        prod_dict["count"] =d1["count"]
        
    if "color/lot" in d1:
        prod_dict["color/lot"] =d1["color/lot"]
        
    if "cur_production" in d1 and d1["cur_production"] != "":
        prod_dict["cur_production"] =convert_to_int(d1["cur_production"])
        
    if "drum_mpm" in d1:
        prod_dict["drum_mpm"]=convert_to_int(d1["drum_mpm"])
        
    json_machine_dict["production"]=prod_dict
    
    sider = {}
    if "sider_name1" in d1 and d1["sider_name1"] != "":
        sider["sider_name1"] = d1["sider_name1"]
        
    if "sider_name2" in d1 and d1["sider_name2"] != "":
        sider["sider_name2"] = d1["sider_name2"]
        
    if "sider_name3" in d1 and d1["sider_name3"] != "":
        sider["sider_name3"] = d1["sider_name3"]
        
    if "no of sider" in d1 and d1["no of sider"] != "":
        sider["no_of_sider"] = d1["no of sider"]
        
    json_machine_dict["sider"]=sider
    
    ind_waste={}
    if "sliver_waste" in d1 and d1["sliver_waste"] != "":
        ind_waste["sliver_waste"]=convert_to_float(d1["sliver_waste"])
        
    if "yarn_waste" in  d1 and d1["yarn_waste"] != "":
        ind_waste["yarn_waste"]=convert_to_float(d1["yarn_waste"])
        
    if "rotor_waste" in d1 and d1["rotor_waste"] != "":
        ind_waste["rotor_waste"]=convert_to_float(d1["rotor_waste"])
        
    json_machine_dict["ind_waste"]=ind_waste
        
    running_dict = {}
    if "eb_units" in d1 and d1["eb_units"] != "":
        running_dict["eb_units"] = convert_to_int(d1["eb_units"])
        
    if "delivery_speed" in d1 and d1["delivery_speed"] != "":
        running_dict["delivery_speed"] = convert_to_int(d1["delivery_speed"])
        
    if "running_hours" in d1 and d1["running_hours"] != "":
        running_dict["running_hours"] = convert_to_float_2(d1["running_hours"])
        
    if "eb_blow" in d1 and d1["eb_blow"] != "":
        running_dict["eb_blow"] =convert_to_float_2(d1["eb_blow"])
        
    if "oe_rotors" in d1 and d1["oe_rotors"] != "":
        running_dict["oe_rotors"]=convert_to_int(d1["oe_rotors"])
        
    if "doffer_rpm" in d1 and d1["doffer_rpm"] != "":
        running_dict["doffer_rpm"]=convert_to_int(d1["doffer_rpm"])
        
    json_machine_dict["running"]=running_dict
    #print("\n")
    #print(json_machine_dict)
    if json_machine_dict:
        res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=glb_id+1, body=json_machine_dict )
        glb_id+=1
        
    ### Process shift waste
    
        if "filter_waste" in d1 or "sweep_waste" in d1 or "MBO_waste" in d1 or "powder_waste" in d1 or "flat_waste" in d1:
            json_waste_dict={}
                
            waste_details={}
            data_exist=False
                
            if "filter_waste" in d1 and d1["filter_waste"] != "" :  
                waste_details["filter_waste"]=convert_to_int(d1["filter_waste"])
                data_exist=True
                
            if "sweep_waste" in d1 and d1["sweep_waste"] != "" :
                waste_details["sweep_waste"]=convert_to_int(d1["sweep_waste"])
                data_exist=True
                
            if "MBO_waste" in d1 and d1["MBO_waste"] != "" :
                waste_details["MBO_waste"]=convert_to_int(d1["MBO_waste"])
                data_exist=True
                
            if "powder_waste" in d1 and d1["powder_waste"] != "" :
                waste_details["powder_waste"]=convert_to_int(d1["powder_waste"])
                data_exist=True
                
            if "flat_waste" in d1 and d1["flat_waste"] != "" :
                waste_details["flat_waste"]=convert_to_int(d1["flat_waste"])
                data_exist=True
                
            if data_exist:
                json_waste_dict["type"]="shift_waste"
                
                if "shift" in d1:
                    json_waste_dict["shift"] =d1["shift"]
            
                if "machine_type" in d1:
                    json_waste_dict["machine_type"] =d1["machine_type"]
                
                if "machine_id" in d1:
                    json_waste_dict["machine_id"] =d1["machine_id"]
                
                if "godown" in d1:
                    json_waste_dict["godown"] =d1["godown"]
                
                if "date" in d1 and d1["date"] != "":
                    json_waste_dict["date"]=format_date(d1["date"])
                    
                json_waste_dict["waste_details"]=waste_details
            #print("_____________________________\n")
            #print(json_waste_dict)
            if json_waste_dict:
                res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=glb_id+1,
                               body=json_waste_dict )
                glb_id+=1
                print(glb_id)
    
    daily_waste_dict={}
    daily_waste_exist = False
    
    if "usable_waste" in d1 and d1["usable_waste"] != "":
        daily_waste_dict["usable_waste"]=convert_to_float(d1["usable_waste"])
        daily_waste_exist = True
        
    if "trash" in d1 and d1["trash"] != "":
        daily_waste_dict["trash"]=convert_to_int(d1["trash"])
        daily_waste_exist = True
        
    if daily_waste_exist:
        daily_waste_dict["type"]="daily_waste"
        daily_waste_dict["godown"]=d1["godown"]
        if d1["date"] != "":
            daily_waste_dict["date"]=format_date(d1["date"])
     
    if daily_waste_dict:
        res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=glb_id+1,
                               body=daily_waste_dict )
        glb_id+=1
        print(glb_id)
    
        
    #print("_____________________________\n")
    #print(daily_waste_dict)
    
    mix_input_dict={}
    if "mix_color" in d1 and d1["mix_color"] != "":
        mix_input_dict["mix_color"]=d1["mix_color"]
        
    if "mix_kgs" in d1 and d1["mix_kgs"] != "":
        mix_input_dict["mix_kgs"]=convert_to_int(d1["mix_kgs"])
        
    if "mix_color" in d1 or "mix_kgs" in d1:
        if d1["date"] != "":
            mix_input_dict["date"]=format_date(d1["date"])
        
        mix_input_dict["color/lot"]=d1["color/lot"]
        
        mix_input_dict["type"]="mix"
    #print("_____________________________\n")
    #print(mix_input_dict)
    if mix_input_dict:
        res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE,
                       id=glb_id+1, body=mix_input_dict )
        glb_id+=1
    
    print("+++++++++++++++++++++++++++++\n")
    

    

#res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=1, body= machine1a_day1)
#res = es.get(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=1)
 
    
    
convert_to_json("OEProductionChart.csv")