#!/usr/bin/python
## 6/16/2017 - remove PyQuery dependency
## 5/19/2016 - update to allow for authentication based on api-key, rather than username/pw
## See https://documentation.uts.nlm.nih.gov/rest/authentication.html for full explanation

import requests
#from pyquery import PyQuery as pq
import lxml.html as lh
from lxml.html import fromstring


uri="https://utslogin.nlm.nih.gov"
#option 1 - username/pw authentication at /cas/v1/tickets
auth_endpoint1 = "/cas/v1/tickets/"
#option 2 - api key authentication at /cas/v1/api-key
auth_endpoint = "/cas/v1/api-key"



class Authentication:
    def __init__(self,username,password,apikey):

        self.username = username
        self.password = password

        self.apikey = apikey
        self.service = "http://umlsks.nlm.nih.gov"
    


    def gettgt(self):
        if self.username != "" and self.password != "":

            params = {'username': self.username,'password': self.password}
            h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
            r = requests.post(uri + auth_endpoint1, data=params, headers=h)
            print("if r", r)
            response = fromstring(r.text)
           
            tgt = str(response.xpath('//form/@action')[0])
            #t = tgt.rsplit('//', 1)[-1]
            print("if tgt:", tgt)
        elif self.apikey != "":
            params = {'apikey': self.apikey}
            h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent": "python"}
            r = requests.post(uri + auth_endpoint, data=params, headers=h)
            print("else r:", r)
            response = fromstring(r.text)
            
            tgt = str(response.xpath('//form/@action')[0])
            #t=tgt.rsplit('//',1)[-1]

            print("else:",tgt)
        return tgt

    def getst(self,tgt):
        params = {'service': self.service}
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
        r = requests.post(tgt,data=params,headers=h)
        st = r.text
        print("ST PRINT:",st)
       
        return st
   
   
   
#auth = Authentication(("asimabbas","Andriod$555"))

