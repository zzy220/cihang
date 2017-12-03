'''
Created on Nov 18, 2017

@author: zhenyu
'''
from onboardsvr import downloader
import csv
import os
import hashlib
import logging

class Patcher():
    '''
    download pactches and do updating...
    The patcher is driving by a timer
    '''

    def __init__(self, workdir, patchroot):
        '''
        Constructor
        '''
        self.patchroot = patchroot
        self.workdir = workdir
        self.downloader = downloader.DownLoader()        
        
    def download_patchlist(self):
        filelist = os.path.join(self.workdir, "patches.txt")
        patchlist_url = "https://server.chrail.cn/patch/2017/list.txt"
        self.downloader.begin_download(patchlist_url, filelist)
        self.downloader.finish_download() # finish downloading
        if os.path.exists(filelist):
            return True
        return False
                
    def parse_patchlist(self, patchlist):       
        '''
        patch list is a tab separated csv file
        parse the list file and return a patch list
        ''' 
        patchlist = os.path.join(self.workdir, "patches.txt")
        patch_list = []
        with open(patchlist, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                print (row)
                # row format url    md5    cmd0    cmd1    
                if len(row) ==4:
                    p = {}
                    p["url"]=row[0]
                    p["md5"]=row[1]
                    p["cmd0"]=row[2]
                    p["cmd1"]=row[3]
                    patch_list.append(p)
        return patch_list
    
    def mainjob(self):
        if self.stopFlag:
            return
        patchlist = self.get_file_list()
        for p in patchlist:
            self.do_patch(p)
            if self.stopFlag:
                return

    def calc_md5(self, filename):
        md5_returned = ''
        if os.path.exists(filename)==False:
            logging.error('calc_md5 : file does not exist:'+filename)
            return ''
        
        try:
            with open(filename, "rb") as file_to_check:
                # read contents of the file
                data = file_to_check.read()    
                # pipe contents of the file through
                md5_returned = hashlib.md5(data).hexdigest()
        except Exception as e:
            print( e)
            print('fail to calc md5')
            
        return md5_returned;    
        
    def do_patch(self, p):
        # tmpfile to download the patch
        tmpfile = os.path.join(self.workdir, "tmp"+ p['md5'] + ".tar.gz")
        # download the patch file
        try:
            self.downloader.begin_download(p["url"], tmpfile)
            self.downloader.finish_download()
        except IOError as e:
            logging.error('do_patch failed:'+e)
            return
        # do md5 check
        new_md5 = self.calc_md5(tmpfile)
        if new_md5!=p['md5']:
            logging.error('patching failed: md5 error')
            logging.error('url='+p['url'])
            logging.error('md5='+p['md5'])
            logging.error('new md5='+new_md5)
            return False
        # run pre command
        try:
            if len (p['cmd0']):
                os.system(p['cmd0'])
        except Exception as e:
            logging.error('failed to execute command0:'+p['cmd0'])
            return False
        
        # apply the patch file
        tardir = '/d/' # to to root dir
        tarcmd = 'tar -C '+ tardir + '-xvf ' + tmpfile
        try:
            os.system(tarcmd)
        except Exception as e:
            logging.error('failed to execute tar command:' + tarcmd)
            return False    
        
        # run post command
        try:
            if len (p['cmd1']):
                os.system(p['cmd1'])
        except Exception as e:
            logging.error('failed to execute command1:'+p['cmd1'])
            return False

# some UT code
if __name__=="__main__":
    logging.basicConfig(filename='d:/test.log',level=logging.DEBUG)

    fl = r'd:\dinner_1080p30_2m.mp4'
    u = Patcher('d:/', 30)
    md5 = u.calc_md5(fl)
    print('done')
#     with open(fl, 'rt') as csvfile:
#         reader = csv.reader(csvfile, delimiter='\t')
#         for row in reader:
#             print (row)

