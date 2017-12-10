'''
Created on Nov 18, 2017

@author: zhenyu
'''

import urllib.request 
import threading
import logging

class DownLoader():
    '''
    download a file in a separate thread
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.localfile = r'd:\download.txt'
        self.lastStatus = False;
        self.thread = None
    def begin_download(self, theurl, localfile):
        self.localfile = localfile
        self.url_to_down= theurl
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        self.lastStatus = False;
    def finish_download(self):
        if self.thread ==None:
            return
        threading.Thread.join(self.thread, None);
        self.thread = None
        
    def get_status(self):
        '''
        return True, if download is finished successfully
        '''
        return self.lastStatus;
        
    def run(self):
        path = self.localfile #
        try:
            r = urllib.request.urlopen(self.url_to_down)
            if r.status == 200:
                with open(path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
        except Exception as e:
            logging.error('failed to download:'+ str(e))
        self.lastStatus = True;                    

# some UT test code
if __name__=="__main__":
    try :
        
        dlr = DownLoader()
        dlr.begin_download("http://www.sohu.com", r'd:\download.txt')
        dlr.finish_download()
    except :
        print('exce')
    
    print('done')
