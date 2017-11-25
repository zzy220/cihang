'''
Created on Nov 18, 2017

@author: zhenyu
'''
import threading
from onboardsvr import downloader
import csv

class Updater():
    '''
    download pactches and do updating...
    '''

    def __init__(self, workdir, interval):
        '''
        Constructor
        '''
        self.interval = interval
        self.timer = threading.Timer(target=self._mainloop)
        self.workdir = workdir
        self.downloader = downloader.DownLoader()
        
    def start(self):
        self.timer.interval = self.interval
        self.timer.start()
        pass
    
    def stop(self):
        self.timer.cancel()
        pass
    
    def get_updater_report(self):
        pass
    
    def get_file_list_dict_reader(self):        
        filelist = self.workdir + "updates.txt"
        self.downloader.begin_download("www.sohu.com", filelist)
        filelist = "d:/down.txt"
        with open(filelist, 'rt') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                print (row)
                
    def get_file_list(self):
        filelist = self.workdir + "updates.txt"
        self.downloader.begin_download("www.sohu.com", filelist)
        filelist = "d:/down.txt"
        with open(filelist, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                print (row)
        
    def _mainloop(self):
        pass

    def check_new_files(self):
        pass


# some UT code
if __name__=="__main__":
    fl = r'd:\list.txt'
    with open(fl, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            print (row)

