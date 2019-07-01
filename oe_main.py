# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import json
from elasticsearch import Elasticsearch

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME='oe_index'
TYPE_NAME_MACHINE = 'machine'
TYPE_NAME_SHIFT_WASTE = 'shift_waste'
TYPE_NAME_DAY_WASTE = 'day_waste'

es = Elasticsearch(hosts = [ES_HOST])

if es.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))
    
# since we are running locally, use one shard and no replicas
request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}
    
print("creating '%s' index..." % (INDEX_NAME))
res = es.indices.create(index = INDEX_NAME, body = request_body)
print(" response: '%s'" % (res))



#--------------------------------------- Day 1
machine1a_day1 = {"type": "machine", "shift":"A", "machine_type":"CARDING", "machine_id":"C1", "godown":"A",
            "date":"2019-06-15", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=1, body= machine1a_day1)
#res = es.get(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=1)
#print(res['_source'])

            
machine2a_day1 = {"type": "machine","shift":"A", "machine_type":"CARDING", "machine_id":"C2", "godown":"A",
            "date":"2019-06-15", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=2, body= machine2a_day1)

            
machine3a_day1 = {"type": "machine","shift":"A", "machine_type":"CARDING", "machine_id":"C3", "godown":"A",
            "date":"2019-06-15", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=3, body= machine3a_day1)           
            
machine4a_day1 = {"type": "machine","shift":"A", "machine_type":"CARDING", "machine_id":"C4", "godown":"A",
            "date":"2019-06-15", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=4, body= machine4a_day1)
                  
                    
shift_waste_a_day1 = {"type": "shift_waste","shift": "A", "godown":"A", "date":"2019-06-15", "waste_details":
                {"filter_waste":23,"sweeping_waste":8, "MBO_waste":16, 
                      "powder_waste":24, "flat_waste":65, "total_shift_waste":100}}
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=5, body= shift_waste_a_day1)
   

machine1c_day1 = {"type": "machine","shift":"C", "machine_type":"CARDING", "machine_id":"C1", "godown":"A",
            "date":"2019-06-15", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=6, body= machine1c_day1)

            
machine2c_day1 = {"type": "machine","shift":"C", "machine_type":"CARDING", "machine_id":"C2", "godown":"A",
            "date":"2019-06-15", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=7, body= machine2c_day1)

            
machine3c_day1 = {"type": "machine","shift":"C", "machine_type":"CARDING", "machine_id":"C3", "godown":"A",
            "date":"2019-06-15", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=8, body= machine3c_day1)

            
machine4c_day1 = {"type": "machine","shift":"C", "machine_type":"CARDING", "machine_id":"C4", "godown":"A",
            "date":"2019-06-15", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=9, body= machine4c_day1)            
                    
                    
shift_waste_c_day1 = {"type": "shift_waste","shift": "C", "godown":"A", "date":"2019-06-15", "waste_details":
                {"filter_waste":23,"sweeping_waste":8, "MBO_waste":16, 
                      "powder_waste":24, "flat_waste":65, "total_shift_waste":136}}
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=10, body= shift_waste_c_day1)

    
day1_waste={"type": "daily_waste","date":"2019-06-15", "godown":"A", "usable_waste":16}
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=11, body= day1_waste)
    
#--------------------------------------- Day 2
machine1a_day2 = {"type": "machine","shift":"A", "machine_type":"CARDING", "machine_id":"C1", "godown":"A",
            "date":"2019-06-16", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=12, body= machine1a_day2)  

            
machine2a_day2 = {"type": "machine","shift":"A", "machine_type":"CARDING", "machine_id":"C2", "godown":"A",
            "date":"2019-06-16", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=13, body= machine2a_day2)

            
machine3a_day2 = {"type": "machine","shift":"A", "machine_type":"CARDING", "machine_id":"C3", "godown":"A",
            "date":"2019-06-16", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=14, body= machine3a_day2)

            
machine4a_day2 = {"type": "machine","shift":"A", "machine_type":"CARDING", "machine_id":"C4", "godown":"A",
            "date":"2019-06-16", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=15, body= machine4a_day2)
                    
                    
shift_waste_a_day2 = {"type": "shift_waste","shift": "A", "godown":"A", "date":"2019-06-16", "waste_details":
                {"filter_waste":23,"sweeping_waste":8, "MBO_waste":16, 
                      "powder_waste":24, "flat_waste":65, "total_shift_waste":100}}
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=16, body= shift_waste_a_day2)
    

machine1c_day2 = {"type": "machine","shift":"C", "machine_type":"CARDING", "machine_id":"C1", "godown":"A",
            "date":"2019-06-16", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=17, body= machine1c_day2)

            
machine2c_day2 = {"type": "machine","shift":"C", "machine_type":"CARDING", "machine_id":"C2", "godown":"A",
            "date":"2019-06-16", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=18, body= machine2c_day2)

            
machine3c_day2 = {"type": "machine","shift":"C", "machine_type":"CARDING", "machine_id":"C3", "godown":"A",
            "date":"2019-06-16", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=19, body= machine3c_day2)

            
machine4c_day2 = {"type": "machine","shift":"C", "machine_type":"CARDING", "machine_id":"C4", "godown":"A",
            "date":"2019-06-16", 
            "production": {"count":"20s", "color":"red01",
                                              "quantity": 800.2},
            "waste": {"slaver_waste":1.2}
            }
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=20, body= machine4c_day2)
                    
                    
shift_waste_c_day2 = {"type": "shift_waste","shift": "C", "godown":"A", "date":"2019-06-16", "waste_details":
                {"filter_waste":23,"sweeping_waste":8, "MBO_waste":16, 
                      "powder_waste":24, "flat_waste":65, "total_shift_waste":100}}
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=21, body= shift_waste_c_day2)

day2_waste={"type": "daily_waste","date":"2019-06-16", "godown":"A", "usable_waste":16}
res = es.index(index= INDEX_NAME, doc_type=TYPE_NAME_MACHINE, id=22, body= day2_waste)