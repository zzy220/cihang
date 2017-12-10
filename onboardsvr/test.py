'''
Created on Dec 4, 2017

@author: zhenyu
'''
from onboardsvr import devmon
from onboardsvr import reporter
from onboardsvr import downloader

import csv
from Crypto.Cipher import AES
import json
import datetime
import logging
if __name__ == '__main__':
#     devm1 = devmon.DevMon()
#     devm1.adddev("www.sina.com")    
#     devm1.adddev("www.sohu.com")
#     ret = devm1.getDevStatus()

#     filelist = r"d:/lists.txt"
#     with open(filelist, 'rt') as csvfile:
#         reader = csv.reader(csvfile, delimiter='\t')
#         for row in reader:
#             print (row)
    
#     r = reporter.Reporter(10)
#     r.testAES()

#     d = downloader.DownLoader()
#     d.begin_download("https://dl.360safe.com/inst.exe", r"d:\inst.exe")
#     d.finish_download()
    a = [  ]
    a.append( [str(datetime.datetime.now()), 'ea'])
    a.append( [str(datetime.datetime.now()), 'db'])
    a.append( [str(datetime.datetime.now()), 'bc'])
    a.append( [str(datetime.datetime.now()), 'ad'])
    b = sorted(a, key=lambda i:i[0]);
    #print(b)
    c = sorted(a, key=lambda i:i[1]);
    #print(c)
    b = json.dumps(a)
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.warn('this is a warning')
    logging.info('this is a info')
    logging.error('this is a error')
    logging.debug('this is a debug')
    while True:
        print('press h for help')
        inchr = input("press q to quit")
        if inchr == 'q':
            break
        elif inchr == 'h':
            print('please read the README.txt for reference.')
    
def __parse_patchlist_cvs(self, patchlistfile):       
    '''
    patch list is a tab separated csv file:
        patch_url    md5    cmd0    cmd1
        ...
    parse the list file and return a patch list        
    ''' 
    patch_list = []
    with open(patchlistfile, 'rt') as csvfile:
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