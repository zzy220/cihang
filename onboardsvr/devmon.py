'''
Created on Nov 18, 2017

@author: zhenyu
'''
from platform import system as system_name # Returns the system/OS name
from os import system as system_call       # Execute a shell command

import threading

class DevMon(object):
    '''
    Monitor the status of devices
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.hostlist = []
        self.results = {}
        self.lock = threading.Lock()
        return
    
    def adddev(self, devip ):
        self.hostlist.insert(0, devip)
        
    def removedev(self, devip):
        self.hostlist.remove(devip)
    
    def getdevlist(self):
        return self.hostlist
    
    def getDevStatus(self):
        # clear the status
        self.results.clear()
        
        ths = []
        # ping all devices in different threads
        for devip in self.hostlist:
            t = threading.Thread(target=self.get_alive_status, args = (devip,))
            t.daemon = True
            t.start()
            ths.append(t)
            
        # wait all threads to be done
        for t in ths:
            t.join(None)
        
        # return the ping results
        return self.results
    
    # called by each thread
    def get_alive_status(self, devip):
        alive = self.ping(devip)
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
        parameters = "-n 1" if system_name().lower()=="windows" else "-c 1"
    
        # Pinging
        return system_call("ping " + parameters + " " + host) == 0      

