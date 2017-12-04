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
if __name__ == '__main__':
#     devm1 = devmon.DevMon()
#     devm1.adddev("www.sina.com")    
#     devm1.adddev("www.sohu.com")
#     ret = devm1.getDevStatus()

    ret = 0
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
    print(b)
    c = sorted(a, key=lambda i:i[1]);
    print(c)
    b = json.dumps(a)
    print(ret)
    

    r = reporter.Reporter(10)
    r.do_report()
