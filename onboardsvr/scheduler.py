'''
Created on Dec 2, 2017

@author: zhenyu
'''
import threading
from onboardsvr import downloader

class Scheduler():
    def __init__(self, workdir, interval):
        '''
        Constructor
        '''
        self.interval = interval
        self.timer = threading.Timer(interval, self.mainjob)
        self.workdir = workdir
        self.stopFlag = False
        
    def start(self):
        self.timer.interval = self.interval
        self.timer.start()
        pass
    
    def stop(self):
        self.stopFlag = True # if the timer thread is doing job, we have opportunity to check this flag in the job function
        self.timer.cancel(); # stop wait
        self.timer.join(); # wait for the thread to exit
        pass
    def mainjob(self):
        pass

if __name__ == '__main__':
    pass