#################################################################################
# usage of the script
# usage: python search-terms.py -k APIKEY -v VERSION -s STRING
# see https://documentation.uts.nlm.nih.gov/rest/search/index.html for full docs
# on the /search endpoint
#################################################################################

from __future__ import print_function
from Authentication import *
import requests
import json
import argparse
from collections import defaultdict


version = "current"
#string = "diabetic foot"
uri = "https://uts-ws.nlm.nih.gov"
content_endpoint = "/rest/search/"+version
##get at ticket granting ticket for the session
AuthClient = Authentication(""," "," ")

cuiList=[]
dicConcept=defaultdict(list)


def searchTerm(term,key):
    pageNumber=0
    print("term is",term)
    while True:
        ticket = AuthClient.getst(key)

        pageNumber += 1

        query = {'string':term,'searchType':"exact",'ticket':ticket, 'pageNumber':pageNumber}
        r = requests.get(uri+content_endpoint,params=query)
        r.encoding = 'utf-8'
        items  = json.loads(r.text)
        jsonData = items["result"]

    

        print("Results for page " + str(pageNumber)+"\n")
        vcountlist.clear()
        for result in jsonData["results"]:
            try:
                print("result is",result)
                ui=result["ui"]
                if ui != "NONE":
                    print("ui: " + ui)
                    cuiList.append(ui)
                    dicConcept[term].append(result["name"])
                    break;
            except Exception as err:
                print(err)


            print("\n")
   
        ##Either our search returned nothing, or we're at the end
        #if jsonData["results"][0]["ui"] == "NONE" :
        if pageNumber==1:
            print("*")
            break
        print("*********")
    ###return cuiList
    
    
    
    
    

