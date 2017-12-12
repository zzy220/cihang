'''
Created on Nov 18, 2017

@author: zhenyu
'''
from platform import system as system_name # Returns the system/OS name
from os import system as system_call       # Execute a shell command
import os
import logging
import threading
import json

class DevMon(object):
    '''
    Monitor the status of devices
    this monitor reads device list from a json file in following format:
    {
        "rfidList": [ { "name": "rfid1", "ip": "ip_addr1"  },  { "name": "rfid2", "ip": "ip_addr2"  }  ],
        "camList": [  { "name": "cam1", "ip": "ip_addr1"  },  { "name": "cam2", "ip": "ip_addr2"  }  ],
        "apList": [   { "name": "ap1", "ip": "ip_addr1"  },  { "name": "ap2", "ip": "ip_addr2"  }  ],
        "brList": [   { "name": "br1", "ip": "ip_addr1"  },  { "name": "br2", "ip": "ip_addr2"  }  ]
    }
    '''

    def __init__(self, workdir):
        '''
        Constructor
        '''
        self.devlist = {}
        self.devlist_file = os.path.join(workdir, 'devlist.json')
        try:
            with open(self.devlist_file) as fp:
                self.devlist = json.load(fp)
        except Exception as e:
            logging.error('device monitor, load device list failed:' + str(e))
            
        self.results = {}
        self.lock = threading.Lock()
        return
        
    def get_apStatus(self):
        r = []
        if "apList" in self.devlist:
            r = self._make_status_result(self.devlist["apList"])
        return r
        
    def get_brStatus(self):
        r = []
        if "brList" in self.devlist:
            r = self._make_status_result(self.devlist["brList"])
        return r
        
    def get_rfidStatus(self):
        r = []
        if "rfidList" in self.devlist:
            r = self._make_status_result(self.devlist["rfidList"])
        return r
        
    def get_camStatus(self):
        r = []
        if "camList" in self.devlist:
            r = self._make_status_result(self.devlist["camList"])
        return r
        
    def _make_status_result(self, spec_devlist):
        '''
        make the status result for specified device list
        spec_devlist :  [ { "name": "devName", "ip": "ip_addr1"  }, ... ]
        return list [ {"name":"dev1", "status":0}, ... ]
        '''
        devstatus = []
        for i in spec_devlist:
            # we have result for the ip
            if i['ip'] in self.results:
                stat = 0;
                if self.results[i['ip']]:
                    stat = 1 
                devstatus.append( {"name":i['name'], "status":stat} )
        return devstatus
       
    def updateDevStatus(self):
        try:
            if os.path.exists("ping_out.txt"):
                system_call('rm ping_out.txt')
        except Exception as e:
            logging.error('[devmon] failed to rm ping_out.txt:'+ str(e))
        
        # clear the status
        self.results.clear()
        
        iplist = []
        if "rfidList" in self.devlist:
            for i in self.devlist["rfidList"]:
                iplist.append(i['ip'])
                
        if "camList" in self.devlist:
            for i in self.devlist["camList"]:
                iplist.append(i['ip'])
                
        if "apList" in self.devlist:
            for i in self.devlist["apList"]:
                iplist.append(i['ip'])
                
        if "brList" in self.devlist:
            for i in self.devlist["brList"]:
                iplist.append(i['ip'])
            
        threads = []
        # ping all devices in different threads
        for devip in iplist:
            t = threading.Thread(target=self._get_alive_status, args = (devip,))
            t.start()
            threads.append(t)
            
        # wait all threads to be done
        for t in threads:
            t.join(None)
        
        print('[devmon] update dev status done')
        # return the ping results
        return self.results
    
    # called by each thread
    def _get_alive_status(self, devip):
        alive = False
        try:
            alive = self.ping(devip)
        except Exception as e:
            logging.error('ping dev failed:' + str(e))
            
        # the results can be mod by multiple threads so, need a lock
        self.lock.acquire()
        self.results[devip]= alive
        self.lock.release()
        
    def ping(self, host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that some hosts may not respond to a ping request even if the host name is valid.
        """
        # Ping parameters as function of OS
        if system_name().lower()=="windows":
            parameters = "-n 1"
        else:
            parameters = "-c 1"
    
        # Pinging
        return system_call("ping " + parameters + " " + host + " >> ping_out.txt") == 0      

#UT code
if __name__ == '__main__':
    dm = DevMon('D:/')
    dm.updateDevStatus()
    print(dm.get_apStatus())
    print(dm.get_brStatus())
    print(dm.get_camStatus())
    print(dm.get_rfidStatus())
    
    pass
        