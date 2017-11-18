'''
Created on Nov 18, 2017

@author: zhenyu
'''
from onboardsvr import devmon

if __name__ == '__main__':
    devm1 = devmon.DevMon()
    devm1.adddev("www.sina.com")    
    devm1.adddev("www.sohu.com")
    ret = devm1.getDevStatus()
    print(ret)
    
    