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
AuthClient = Authentication("","","")
dicEntityType=defaultdict(list)

###################################
#get TGT for our session
###################################

#
uri = "https://uts-ws.nlm.nih.gov"

def searchEntityType(eidentifier,ekey):


    ##if we don't specify a source vocabulary, assume we're retrieving UMLS CUIs

    content_endpoint = "/rest/semantic-network/"+str(version)+"/TUI/"+str(eidentifier)



    ##ticket is the only parameter needed for this call - paging does not come into play because we're only asking for one Json object
    query = {'ticket':AuthClient.getst(ekey)}
    r = requests.get(uri+content_endpoint,params=query)
    r.encoding = 'utf-8'
    items  = json.loads(r.text)
    jsonData = items["result"]
    print(jsonData)

    ## These data elements may or may not exist depending on what class ('Concept' or 'SourceAtomCluster') you're dealing with so we check for each one.

    #print(jsonData["semanticTypeGroup"])
    semanticType=jsonData["name"]
    entityTypeGroup=jsonData["semanticTypeGroup"]
    entityType=entityTypeGroup["expandedForm"]
    dicEntityType[semanticType]=entityType
    #print (semanticType,":","Entity Type: " + entityType)



