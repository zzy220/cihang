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
    def __init__(self, workdir, patch_root, report_interval, patcher_interval):
        '''
        Constructor
        workdir: work dir to put working files
        patch_root: the root path to apply patches
        report_interval : the interval to send device report (in seconds)
        patcher_interval : the interval to run the patcher (in seconds)
        '''
        super(Scheduler, self).__init__()

        self.report_interval = report_interval
        self.patcher_interval = patcher_interval
        self.workdir = workdir
        self.patch_root =patch_root
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
        _reporter = reporter.Reporter(self.workdir)
        _patcher = patcher.Patcher(self.workdir, self.patch_root)
    
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
            if cur_time - last_patcher_time > self.patcher_interval:
                try:
                    _patcher.do_patch()
                except Exception as e: # catch all exceptions to keep this thread alive
                    logging.error('exception in scheduler:' + str(e))
                last_patcher_time = cur_time
                
            # sleep a while to throttle down CPU usage
            time.sleep(1)
        

if __name__ == '__main__':
    s = Scheduler("d:/Test", "d:/Test", 100, 100)
    s.startup()
    input('press q to quit')
    s.shutdown()
    pass