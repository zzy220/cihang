'''
Created on Dec 2, 2017

@author: zhenyu
'''
import json
import os
import logging
import datetime

class PatchHistory():
    '''
    a utility class to track successfully applied patches.
    '''
    def __init__(self, workdir, max_hist_list):
        '''
        Constructor
        '''
        self.workdir = workdir
        self.max_hist_list = max_hist_list
        self.hist_list = []
        self.hist_file = os.path.join(self.workdir, 'patch_hist.json')
        #now read from a file
        try:
            if os.path.exists(self.hist_file):
                with open(self.hist_file, 'rt') as histfile:
                    self.hist_list = json.load(histfile)
        except Exception as e:
            logging.error('[patcher_hist]failed to parse patch history file:'+ str(e))
             
    def find_in_history(self, md5ofapatch):
        for x in self.hist_list:
            if x[1]==  md5ofapatch:
                return True
        return False
    
    def add_to_history(self, patch_result):
        '''
        patch_result is a list like [ '2017-12-02 19:11:08.493961', md5, url ]
        '''
        self.hist_list.append(patch_result)
        # sort the list by the timestamp(this first element of a patch result
        self.hist_list.sort(key=lambda i:i[0])
        if len(self.hist_list)>self.max_hist_list:
            self.hist_list = self.hist_list[0:self.max_hist_list-1]
        self.flush_history()
            
    def flush_history(self):
        '''
        flush the history list to a file
        '''      
        if len (self.hist_list)==0:
            return
        
        try:
            with open(self.hist_file, 'wt') as histfile:
                json.dump(self.hist_list, histfile)
        except Exception as e:
            logging.error('failed to flush history file:'+ str(e))
             
# UT code             
if __name__ == '__main__':
        a = [  ]
        a.append( [str(datetime.datetime.now()), '0d6d9c48f9763a377f7c6e709ae3f6d5','ea'])
        a.append( [str(datetime.datetime.now()), '0d6d9c48f9763a377f7c6e709ae3f6d5','db'])
        a.append( [str(datetime.datetime.now()), '0d6d9c48f9763a377f7c6e709ae3f6d5','bc'])
        a.append( [str(datetime.datetime.now()), '0d6d9c48f9763a377f7c6e709ae3f6d5','ad'])
        hist = PatchHistory("d:/", 100)
        for x in a:
            hist.add_to_history(x)
            
        if hist.find_in_history('0d6d9c48f9763a377f7c6e709ae3f6d5'):
            print('found.')