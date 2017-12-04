'''
Created on Dec 2, 2017

@author: zhenyu
'''
import threading
import logging

from onboardsvr import downloader
from onboardsvr import reporter
from onboardsvr import patcher

class ReportRunner(threading.Thread):
    def __init__(self, workdir):
        self.workdir = workdir
        self.stopFlag = False
    def run(self):
        print('run once')
        
class PatcherRunner(threading.Thread):
    def __init__(self, workdir):
        self.workdir = workdir
        self.stopFlag = False
    def run(self):
        print('PatcherRunner run once')
            
class Scheduler():
    def __init__(self, workdir, interval):
        '''
        Constructor
        '''
        self.interval = interval
        self.workdir = workdir
        # setup the report runner
        self.report_runner = ReportRunner(workdir)
        self.report_timer = threading.Timer(interval, self.report_runner.run) 
        
        # setup the pathcer runner
        self.patcher_runner = PatcherRunner(workdir)
        self.patcher_timer  = threading.Timer(interval * 2, self.patcher_runner.run) 
        
    def startReporter(self):
        self.report_timer
        self.report_timer.start()
        pass
    
    def stopReporter(self):
        self.report_runner.stopFlag = True # if the timer thread is doing job, we have opportunity to check this flag in the job function
        self.report_timer.cancel(); # stop wait
        self.report_timer.join(); # wait for the thread to exit
        pass

if __name__ == '__main__':
    s = Scheduler("d:/", 1)
    s.startReporter()
    input('press q to quit')
    s.stopReporter()
    pass