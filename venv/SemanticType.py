#################################################################################################
# usage of the script
# usage: python retrieve-cui-or-code.py -k APIKEY -v VERSION -i IDENTIFIER -s SOURCE
# If you do not provide the -s parameter, the script assumes you are retrieving information for a
# known UMLS CUI
#################################################################################################

from Authentication import *
import requests
import json
import argparse
from collections import defaultdict


version = "current"
source = ""
AuthClient = Authentication("","","")

###################################
#get TGT for our session
###################################
dicSematnicType=defaultdict(list)
tuiList=[]
#
uri = "https://uts-ws.nlm.nih.gov"

def searchSemanticType(identifier,skey):
    try:
        #tgt = AuthClient.getst(skey)
        source
    except NameError:
        source = None

    ##if we don't specify a source vocabulary, assume we're retrieving UMLS CUIs
    if source is None:
        content_endpoint = "/rest/content/"+str(version)+"/CUI/"+str(identifier)

    else:
        content_endpoint = "/rest/content/"+str(version)+"/source/"+str(source)+"/"+str(identifier)

    ##ticket is the only parameter needed for this call - paging does not come into play because we're only asking for one Json object
    query = {'ticket':AuthClient.getst(skey)}
    r = requests.get(uri+content_endpoint,params=query)
    r.encoding = 'utf-8'
    items  = json.loads(r.text)
    jsonData = items["result"]


    ############################
    ### Print out fields ####
    # print("Semantic Types:")
    try:
       concept=jsonData["name"]
       for stys in jsonData["semanticTypes"]:
           semanticType=stys["name"]
           dicSematnicType[concept].append(semanticType)
           tuiList.append(semanticType)


    except:
          pass
