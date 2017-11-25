'''
Created on Nov 25, 2017

@author: zhenyu

coding mode:

"AES/ECB/PKCS7Padding"

result is base64 encoded
'''
from Crypto.Cipher import AES
import base64 

def encode (key, data):
    mode = AES.MODE_ECB
    BS = AES.block_size
    
    # padding function
    pkcs7padding = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
    cryptor = AES.new(key, mode)
    
    # do padding
    padded_data = pkcs7padding(data)
    cipher_txt = cryptor.encrypt(padded_data.encode())
    return base64.b64encode(cipher_txt)

def decode (key, b64cipher):
    mode = AES.MODE_ECB
    cryptor = AES.new(key, mode)

    #unpadding function
    pkcs7unpadding = lambda s : s[:-ord(s[len(s)-1:])]   
    
    cipher_txt = base64.b64decode(b64cipher)
    padded_data = cryptor.decrypt(cipher_txt)
    #unpad the text
    return pkcs7unpadding(padded_data);
    
# some UT code
key = '4590auf34567hilm2390noqrst890uyz'.encode()
t = "A really secret message. Not for prying eyes."
cipher_b64 = encode(key, t)
plain = decode(key, cipher_b64)
print (plain)
