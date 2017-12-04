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
    "rfidList": [ { "rfid": 0  },  { "rfid": 0 }  ],
    "camList": [  { "cam": 0 }, {  "cam": 0 } ],
    "apList": [  { "ap": 0  }, { "ap": 0  }  ],
    "brList": [  {    "br": 0   },    { "br": 0  }   ],
    "objList": [  {  "stat0": "", "stat1": "", "stat2": 0, "stat3": ""  } ]
  }
}
'''
import json
import urllib.request 
import datetime
from onboardsvr import aescrypto
import logging

class Reporter(object):
    '''
    report the state of this onboard server and 
    states of various devices
    '''

    def do_report(self):
        self.reportId +=1
        self.params["id"] = 159 #self.reportId
        self.params['time']=str(datetime.datetime.now())
        
        print(json.dumps(self.report))
        self.apList.clear()
        self.camList.append({"cam1":1})
        self.camList.append({"cam2":1})
        self.apList.append({"ap1":0,} )
        self.apList.append({"ap2":0,} )
        self.brList.append({"br1":0,})
        self.rfidList.append({"rfid1":0,})
        self.objList.append({"stat0":10 , "stat1":10 , "stat2":10 , "stat3":10})
        print(json.dumps(self.report))
        req = urllib.request.Request("https://server.chrail.cn/equipment!request.action")
        #req.add_header('Content-Type', 'application/octet-stream')
        #req.add_header('Content-Type', 'application/json; charset=UTF-8')
        req.add_header('Accept', '*/*')  
        req.add_header("Access-Control-Allow-Origin", "*")
        
        # prepare the form data
        key = '4590auf34567hilm2390noqrst890uyz'
        use_aes = True;
        json_data = json.dumps(self.report)
        if use_aes:
            json_data = aescrypto.encode(key, json_data)
            #test dec
            plaintxt = aescrypto.decode(key, json_data)
            print(plaintxt)    

        formdata = {'data': json_data}
        formdata_enc = urllib.parse.urlencode(formdata)
        
        # now post the data
        result=''
        try:
            req.data = formdata_enc.encode();
            resp = urllib.request.urlopen(req)
            
            if resp.status == 200:
                bytes = b''
                for chunck in resp:
                    bytes += chunck
                pass
            #result = resp.read();
            result = bytes.decode("utf-8") 
        except Exception as e:
            logging.error('report data failed:' + str(e))
        
        print(result)
        pass
    
    def __init__(self, interval):
        '''
        Constructor
        '''
        self.reportId=0
        self.report = {}
        self.params = {}
        self.rfidList = []
        self.apList = []
        self.camList = []
        self.brList = []
        self.objList = []
        
        #init param
        self.params["id"]= 2
        self.params["extInfo"]= "testinfo"
        self.params["text"]= "test"
        self.params["rfidList"]= self.rfidList
        self.params["apList"]= self.apList
        self.params["camList"]= self.camList
        self.params["brList"]= self.brList
        self.params["objList"]= self.objList
        # init report
        self.report["method"] = "devStatus"
        self.report["params"] = self.params
        
if __name__ == '__main__':
    r = Reporter(10)
    r.do_report()
        