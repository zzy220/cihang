'''
Created on Nov 18, 2017

@author: zhenyu
'''

import csv
import json
import os
import hashlib
import logging
import urllib
import datetime

from onboardsvr import downloader
from onboardsvr import patchhistory

class Patcher():
    '''
    download pactches and do updating...
    The patcher is driving by the scheduler
    '''

    def __init__(self, workdir, patchroot):
        '''
        Constructor
        '''
        self.patchroot = patchroot
        self.workdir = workdir
        self.downloader = downloader.DownLoader()        
        self.history = patchhistory.PatchHistory(workdir, 100)
        
    def do_patch(self):
        '''
        this is the main function of this patcher.
        This function downloads the patch list,
        and check if new there are new patches need to apply.
        after apply new patches, a report will also be sent to server
        '''
        patchlist_file = os.path.join(self.workdir, 'patch_list.json')
    
        self._download_patchlist(patchlist_file)
        patchlist = self._parse_patchlist_json(patchlist_file)
        
        patch_report = [];
        '''
        [
        {"url":"https://server.chrail.cn/patch/2017/patch1.tar.gz","md5":"7cc1df8e7027b1243d77dd4f8f7159e7","status":0},
        {"url":"https://server.chrail.cn/patch/2017/patch2.tar.gz","md5":"f88b3de4e2cc779d99de5ae0a887512f","status":1}
        ]
        '''
        for p in patchlist:
            if self.history.find_in_history(p['md5'])==False:
                print('[patcher] now applying patch:')
                print(p)
                ret = self._apply_patch(p)
                # only set success patches to the history
                if ret ==0:
                    hist_result =  [str(datetime.datetime.now()), p['md5'], p['url']];
                    self.history.add_to_history(hist_result)
                patch_report.append({"url":p['url'], "md5":p['md5'], "status":ret});
            else:
                print('[patcher] this patch already in the hostory list:')
                print(p)
                    
        if len(patch_report)>0:
            self._send_patch_report(patch_report)

    def _download_patchlist(self, patchlistfile):
        patchlist_url = "https://server.chrail.cn/patch/2017/list.json"
        self.downloader.begin_download(patchlist_url, patchlistfile)
        self.downloader.finish_download() # finish downloading
        if os.path.exists(patchlistfile):
            return True
        return False
    
    def _parse_patchlist_json(self, jsonfile):
        '''
        This function parse the list file and return a patch list object   
        patch list json format:
        [
           {"url":"patch_url", "md5":"patch_md5",  "cmd0":"cmd before patch",  "cmd1":"cmd before patch"}
            ...
        ]
        ''' 
        patch_list = []
        try:
            with open(jsonfile, 'rt') as fp:
                patch_list = json.load(fp)
        except Exception as e:
            logging.error('failed to parse patch list file:'+ str(e))
        return patch_list
    
    def _send_patch_report(self, patch_report): 
        print(json.dumps(patch_report))
        req = urllib.request.Request("https://server.chrail.cn/equipment!request.action")
        req.add_header('Accept', '*/*')  
        req.add_header("Access-Control-Allow-Origin", "*")
        json_data = json.dumps(patch_report)
        formdata = {'data': json_data}
        formdata_enc = urllib.parse.urlencode(formdata)
        # now post the data
        result=''
        try:
            req.data = formdata_enc.encode();
            resp = urllib.request.urlopen(req)
            if resp.status == 200:
                bytes = b''
                for chunck in resp:
                    bytes += chunck
                pass
            #result = resp.read();
            result = bytes.decode("utf-8") 
        except Exception as e:
            logging.error('report data failed:' + str(e))
        print(result)
        pass
            
    
    def _calc_md5(self, filename):
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

    def _run_cmd (self, cmd):
        if len(cmd) ==0: # empty command, treat as right case
            return True
        r = False
        try:
            r = os.system(cmd) == 0 # we assume the cmd return 0 on SUCCESS
        except Exception as e:
            logging.error('failed to execute command0:'+ cmd)
            return False
        return r;
        
    def _apply_patch(self, p):
        '''
        apply the patch to the system:
        return value
            0: 表示成功
            1: 文件下载失败
            2: md5验证失败
            3: 补丁前命令cmd0失败
            4: 打补丁(tar 解压)失败
            5: 补丁后命令cmd1失败
        '''
        # tmpfile to download the patch
        tmpfile = os.path.join(self.workdir, "tmp"+ p['md5'] + ".tar.gz")
        # download the patch file
        try:
            self.downloader.begin_download(p["url"], tmpfile)
            self.downloader.finish_download()
        except IOError as e:
            logging.error('do_patch failed:'+e)
            return 1
        
        # do md5 check
        new_md5 = self._calc_md5(tmpfile)
        if new_md5!=p['md5']:
            logging.error('patching failed: md5 error')
            logging.error('url='+p['url'])
            logging.error('md5='+p['md5'])
            logging.error('new md5='+new_md5)
            return 2
        
        # run pre command
        if self._run_cmd(p['cmd0'])==False:
            logging.error('failed to execute command0:'+p['cmd0'])
            return 3
                
        # apply the patch file
        tardir = self.patchroot # to to root dir
        tarcmd = 'tar -C '+ tardir + ' -xvf ' + tmpfile
        if self._run_cmd(tarcmd)==False:
            logging.error('failed to execute tar command:' + tarcmd)
            return 4    
        
        # run post command
        if self._run_cmd(p['cmd1'])==False:
            logging.error('failed to execute command1:'+p['cmd1'])
            return 5
        
        # finally, we've done
        return 0


# some UT code
if __name__=="__main__":

    u = Patcher("d:/Test", "d:/Test/out")
    u.do_patch()
    
    
    fl = r'd:\dinner_1080p30_2m.mp4'
    #md5 = u._calc_md5(fl)
    print('done')
#     with open(fl, 'rt') as csvfile:
#         reader = csv.reader(csvfile, delimiter='\t')
#         for row in reader:
#             print (row)


