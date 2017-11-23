'''
Created on Nov 18, 2017

@author: zhenyu
'''
from onboardsvr import devmon
from onboardsvr import reporter
from onboardsvr import downloader

import csv
from Crypto.Cipher import AES

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
    key = '4590auf34567hilm2390noqrst890uyz'.encode()
    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode)
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
    unpad = lambda s : s[:-ord(s[len(s)-1:])]   
    t = pad ("A really secret message. Not for prying eyes.") 
    cipher_text = encryptor.encrypt(t.encode())
    # Decryption
    decryptor = AES.new(key, mode)
    plain_text = decryptor.decrypt(cipher_text)
#     d = downloader.DownLoader()
#     d.begin_download("https://dl.360safe.com/inst.exe", r"d:\inst.exe")
#     d.finish_download()
    
    print(ret)
    
    