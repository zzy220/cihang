'''
Created on Dec 2, 2017

@author: zhenyu

this is a simple scheduler to run
   the reporter and the patcher timely

'''

import threading
import logging
import time
import sys, traceback

from onboardsvr import downloader
from onboardsvr import reporter
from onboardsvr import patcher
from builtins import str
           
class Scheduler(threading.Thread):
    def __init__(self, workdir, config):
        '''
        Constructor
        workdir: work dir to put working files
        patch_root: the root path to apply patches
        report_interval : the interval to send device report (in seconds)
        patch_interval : the interval to run the patcher (in seconds)
        '''
        super(Scheduler, self).__init__()

        # work dir
        self.workdir = workdir
        # setup app config
        self.report_interval = config["report_interval"]
        self.patch_interval = config["patch_interval"]
        self.patch_root = config["patch_root"]
        self.device_id = config["device_id"]
        self.stop_flag=False; 
        
    def startup(self):
        self.stop_flag=False;
        #self.thread = threading.Thread(target=self._run(), args=())
        #self.thread.start()
        self.start()
    
    def shutdown(self):
        if self.isAlive()==False: # Not running
            return
        self.stop_flag=True;
        self.join()
        
    def run(self):
        '''
        This is the main loop the run the scheduler
        '''
        _reporter = reporter.Reporter(self.workdir, self.device_id)
        _patcher = patcher.Patcher(self.workdir, self.patch_root, self.device_id)
    
        try:
            _reporter.do_report()
            _patcher.do_patch()
        except Exception as e: # catch all exceptions to keep this thread alive
            traceback.print_exc()
            logging.error('exception in scheduler:' + str(e))
            
        last_report_time = time.time()
        last_patcher_time = time.time()
        
        while self.stop_flag == False:
            cur_time =  time.time()
            # is is time to send a report
            if cur_time - last_report_time > self.report_interval:
                try:
                    _reporter.do_report()
                except Exception as e: # catch all exceptions to keep this thread alive
                    logging.error('exception in scheduler:' + str(e))
                last_report_time = cur_time
                
            # is it time to do patching..
            if cur_time - last_patcher_time > self.patch_interval:
                try:
                    _patcher.do_patch()
                except Exception as e: # catch all exceptions to keep this thread alive
                    logging.error('exception in scheduler:' + str(e))
                last_patcher_time = cur_time
                
            # sleep a while to throttle down CPU usage
            time.sleep(1)
        

if __name__ == '__main__':
    c = {
        "patch_root":"/home/samuel",
        "report_interval": 10,
        "patch_interval":  100,
        "device_id": 160
        }
    s = Scheduler("d:/Test", "d:/Test", c)
    s.startup()
    input('press q to quit')
    s.shutdown()
    pass