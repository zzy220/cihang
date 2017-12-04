'''
Created on Nov 18, 2017

@author: zhenyu
'''

import urllib.request 
import threading


class DownLoader(threading.Thread):
    '''
    download a file in a separate thread
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super(DownLoader, self).__init__()         
        self.localfile = r'd:\download.txt'
        
    def begin_download(self, theurl, localfile):
        self.localfile = localfile
        self.url_to_down= theurl
        self.start()
        
    def finish_download(self):
        threading.Thread.join(self, None);
        
    def run(self):
        path = self.localfile #
        r = urllib.request.urlopen(self.url_to_down)
        if r.status == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)

# some UT test code
if __name__=="__main__":
    try :
        
        dlr = DownLoader()
        dlr.begin_download("http://www.sohu.com", r'd:\download.txt')
        dlr.finish_download()
    except :
        print('exce')
    
    print('done')
