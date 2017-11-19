'''
Created on Nov 18, 2017

@author: zhenyu

report device status as following format

data format
{
  "method": "devStatus",
  "params": {
    "id": 35,
    "extInfo": "",
    "text": "",
    "rfidList": [
      {
        "rfid": 0
      },
      {
        "rfid": 0
      }
    ],
    "camList": [
      {
        "cam": 0
      },
      {
        "cam": 0
      }
    ],
    "apList": [
      {
        "ap": 0
      },
      {
        "ap": 0
      }
    ],
    "brList": [
      {
        "br": 0
      },
      {
        "br": 0
      }
    ],
    "objList": [
      {
        "stat0": "",
        "stat1": "",
        "stat2": 0,
        "stat3": ""
      }
    ]
  }
}
'''
import json

class Reporter(object):
    '''
    report the state of this onboard server and 
    states of various devices
    '''

    def do_report(self):
        self.apList.append({"ap1":0,} )
        self.apList.append({"ap2":0,} )
        
        self.params["id"]= 100;
        
        
        print(json.dumps(self.rep))
        self.apList.clear()
        self.camList.append({"cam1":1})
        self.camList.append({"cam2":3})

        print(json.dumps(self.rep))
        
        pass
    
    def __init__(self, interval):
        '''
        Constructor
        '''
        self.rep = {}
        self.params = {}
        self.rfidList = []
        self.apList = []
        self.camList = []
        self.brList = []
        self.objList = []
        
        #init param
        self.params["id"]= 1
        self.params["extInfo"]= "testinfo"
        self.params["text"]= "test"
        self.params["rfidList"]= self.rfidList
        self.params["apList"]= self.apList
        self.params["camList"]= self.camList
        self.params["brList"]= self.brList
        self.params["objList"]= self.objList
        # init report
        self.rep["method"] = "devStatus"
        self.rep["params"] = self.params
        
        