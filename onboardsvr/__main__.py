'''
Created on Nov 18, 2017

@author: zhenyu
'''
from onboardsvr import devmon
from onboardsvr import reporter
import csv

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
    
    r = reporter.Reporter(10)
    r.do_report()
    
    print(ret)
    
    