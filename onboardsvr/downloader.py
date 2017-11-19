'''
Created on Nov 18, 2017

@author: zhenyu
'''

import urllib.request 
import threading
from turtledemo.penrose import star


class DownLoader(threading.Thread):
    '''
    download a file in a separate thread
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.localfile = r'd:\download.txt'
        
    def begin_download(self, theurl, localfile):
        self.localfile = localfile
        self.url_to_down= theurl
        threading.Thread.start()
        
    def finish_download(self):
        threading.Thread.join(self, None);
        
    def run(self):
        path = self.localfile #
        r = urllib.request.urlopen("www.sina.com")
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
