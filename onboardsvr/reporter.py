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
    "rfidList": [ { "name":"rfid1", "status":0  },  { "name":"rfid2", "status":1  } ],
    "camList": [  { "name":"rfid1", "status":0  },  { "name":"rfid2", "status":1  } ],
    "apList": [  { "name":"rfid1", "status":0  },  { "name":"rfid2", "status":1  }  ],
    "brList": [  { "name":"rfid1", "status":0  },  { "name":"rfid2", "status":1  }  ],
    "objList": [  {  "stat0": "", "stat1": "", "stat2": 0, "stat3": ""  } ]
  }
}
'''
import json
import urllib.request 
import datetime
import logging

# packages for current program
from onboardsvr import aescrypto
from onboardsvr import devmon
from onboardsvr import svrstate

class Reporter(object):
    '''
    report the state of this onboard server and 
    states of various devices
    '''
    def __init__(self, workdir, device_id):
        '''
        Constructor
        '''
        self.workdir = workdir
        self.devmon = devmon.DevMon(workdir)
        
        self.report = {}
        self.params = {}
        
        #init param
        self.params["id"]= device_id
        self.params["extInfo"]= ""
        self.params["text"]= ""
        self.params["rfidList"]= []
        self.params["apList"]= []
        self.params["camList"]= []
        self.params["brList"]= []
        self.params["objList"]= []
        # init report
        self.report["method"] = "devStatus"
        self.report["params"] = self.params
    
    def do_report(self):
        # collect dev status
        self.devmon.updateDevStatus(); #execute ping util to check dev status
        
        # setup reports        
        #self.params["time"]=str(datetime.datetime.now())  # do not use time now
        self.params["extInfo"]= ""
        self.params["text"]= ""
        
        self.params["rfidList"]= self.devmon.get_rfidStatus()
        self.params["apList"]= self.devmon.get_apStatus()
        self.params["camList"]= self.devmon.get_camStatus()
        self.params["brList"]= self.devmon.get_brStatus()
        '''
        get current server states
        '''
        self.params["objList"]= svrstate.get_onboardsvr_state()
        
        self._send_report()    
        pass
    
    def _send_report(self): 
        print('[reporter] now send following reports to server:')
        print(json.dumps(self.report))
        req = urllib.request.Request("https://server.chrail.cn/equipment!request.action")
        #req.add_header('Content-Type', 'application/octet-stream')
        #req.add_header('Content-Type', 'application/json; charset=UTF-8')
        req.add_header('Accept', '*/*')  
        req.add_header("Access-Control-Allow-Origin", "*")
        
        # prepare the form data
        key = '4590auf34567hilm2390noqrst890uyz'
        #key = '4590auf34567hiom2390noqrst890uyz' #fake key for test
        use_aes = True;
        json_data = json.dumps(self.report)
        if use_aes:
            json_data = aescrypto.encode(key, json_data)
            #test dec
            plaintxt = aescrypto.decode(key, json_data)

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
        print('[reporter] server reponse:')
        print(result)
        pass
    
    def test_report(self):
        '''
        just some fake data for testing
        '''
        self.params["id"] = 160 #self.reportId
        self.params["rfidList"].clear()
        self.params["apList"].clear()
        self.params["camList"].clear()
        self.params["brList"].clear()
        self.params["objList"].clear()        
        self._send_report()    
    
        
if __name__ == '__main__':
    r = Reporter('d:/Test')
    #r.test_report()
    r.do_report()
        