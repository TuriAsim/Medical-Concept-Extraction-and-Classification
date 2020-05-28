

from __future__ import print_function
from Authentication import *
import requests
import json
import argparse
import SearchTerms as t
import SemanticType as st
import EntityTypeClass as et
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from collections import defaultdict
from nltk.corpus import wordnet
import pandas as pd
from collections import Counter
import re
import string

print(__name__)
value=[]









conceptList=[]
termdic=defaultdict(list);
medicallist=[]



dicProblem=["Disease or Syndrome","Sign or Symptom","Finding","Pathologic Function","Mental or Behavioral Dysfunction","Injury or Poisoning","Cell or Molecular Dysfunction","Congenital Abnormality","Acquired Abnormality","Neoplastic Process","Anatomic Abnormality","virus/becterium"]
dicTreatment=["Therapeutic or Preventive Procedure","Organic Chemical", "Pharmacologic Substance", "Biomedical and Dental material" , "Antibiotic" , "Clinical Drug", " Steroid","Drug Delivery Device", "Medical Device"]
dicTest=["Tissue","Cell","Laboratory or Test Result","Laboratory Procedure" , "Diagnostic procedure","Clinical Attribute",'Body Substance' ]




def process_content():
    #upload file here
    sent=readTextFile("Clinical Notes/record-13.txt")
    print("sent",sent)
    custom_sent_tokenizer = PunktSentenceTokenizer()
    tokenized = custom_sent_tokenizer.tokenize(sent)
    try:
        for i in tokenized:
            words =  nltk.word_tokenize(i)
            words=[word.lower() for word in words]
            print("words:", words)
            st_word=stop_word(words)
            print("stop word:", st_word)
            #list_of_words = filter(lambda x: not re.match('[0-9]{2}[\/,:-][0-9]{2}[\/,:-][0-9]{2,4}', x),st_word)
            list_of_words = filter(lambda x: not re.match('[0-9]{2}[\/,:-][0-9]{1,2}[\/,:-][0-9]{1,2}', x), st_word)
            print("list of words:", list_of_words)
            st_word1 = stop_word(list_of_words)
            print("stop word1:", st_word1)
            removenum=removeNumber(st_word1)
            print("remove number:",removenum)
            st_word2 = stop_word(removenum)
            print("stop word2:", st_word2)
            lemtize_word = wordLemmatization(st_word2)
            print("lemmatize word:", lemtize_word)
            # ngramword = NgramReturner(words)
            # print("word ngram:", ngramword)
            # st_word = stop_word(ngramword)
            # print("stop word:", st_word)
            # remove_duplicate=removeDuplicate(st_word)
            # print("remove duplicate:", remove_duplicate)
            # tagged=termChunk(remove_duplicate)
            # print("chunked", tagged)
            print("words:",words)
            print("stop word:",st_word)
            print("lemmatize word:", lemtize_word)
            print("word ngram:", ngramword)
            print("remove duplicate:",remove_duplicate)
            print("chunked",tagged)

        return tagged
    except Exception as e:
        print(str(e))




#read text file
def readTextFile(path):
    # open file
    with open(path, 'r') as f:

        #read each line of file and store it in rows lis
        #data = f.read().replace("\r", "").replace("\n", '').replace('Â',' ')
        #data = f.read().split("\n") # this is for structure
        data = f.read().replace('Â', ' ').replace('»','').replace('¿','').replace('ï','') # this for unstructured
        print("data",data)

    return data

##### word boundary detection

def wordBoundary(word_tokens):

    stop_words = set(stopwords.words('english'))
    print("stopwordlist",stop_words)
    filter_sentence=[]
    wordset = set()
    filter_sentence = []
    for w in word_tokens:

        if w != '':
            for w1 in w.split():
                print("w is", w, "w1 is", w1)
                if w1 in stop_words:
                    wordset.add(w1)
                print("wordset",len(wordset)," : ", "w",len(w.split()))
            if len(wordset) != len(w.split()):
                filter_sentence.append(w)
            wordset.clear()

    return filter_sentence


#chunkging method
def termChunk(wordlist):
    filterlist=[]
    tagged = nltk.pos_tag(wordlist)
   #regular expression to retreive just specific words
    chunk_expression = r"""
                        Term:{<NN.*>}
                        {<JJ.*>}
                        {<RB.*>}
                        """
    chunkParser = nltk.RegexpParser(chunk_expression)
    chunked = chunkParser.parse(tagged)
    print(chunked)
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Term'):
        #print(subtree)

        tree = nltk.Tree.fromstring(str(subtree), read_leaf=lambda x: x.split("/")[0]).leaves()
        makeitstring=' '.join(map(str,tree))
        print("tree is:", tree)
        filterlist.append(makeitstring)

    return filterlist



#  pos tagging treebank to wordnet
def get_wordnet_pos(treebank_tag):

    print("getpos",treebank_tag)
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV

    else:
        return None # for easy if-statement

#stop word removing
def stop_word(word_tokens):
    stop_words = set(stopwords.words('english'))
    print("stopwordlist",stop_words)
    filter_sentence=[]
    for w in word_tokens:
        if w !='':
            print("w is", w)
            if w not in stop_words:
                print("token", w)
                filter_sentence.append(w)

    return filter_sentence


# Remove Duplicate
def removeDuplicate(tokenlist):
    order_tokens = set()
    result=[]
    for word in tokenlist:
        if word not in order_tokens:
            order_tokens.add(word)
            result.append(word)
    return  result
# Lemmatization

def wordLemmatization(s_word):
    lzr=WordNetLemmatizer()
    lem_word=[]
    tagged=nltk.pos_tag(s_word)
    for ww,tt  in tagged:
        print("lemz",ww,tt)
        wntag = get_wordnet_pos(tt)
        if wntag is None:  # not supply tag in case of None
            lem_word.append(lzr.lemmatize(ww))
        else:
            lem_word.append(lzr.lemmatize(ww, pos=wntag))

    return lem_word

#N-gram
def NgramReturner(ngramString):
    bigram_vector=[]
    for i in range(1,6):
        for item in nltk.ngrams(ngramString,i):
            bigram_vector.append(' '.join(item))

    return bigram_vector

#check for reduntent semantic type
def duplicateSemanticType(typelist):
    order_type = set()
    result=[]
    for word in typelist:
        if word not in order_type:
            order_type.add(word)
            result.append(word)
    return  result

# return max Medical concept

def MaxConcept(MyList):
    
    dic = Counter(MyList)
    maxx = max(dic.values())
    
    keys = [x for x, y in dic.items() if y == maxx]
    if len(keys) > 1:
        maxv=keys[0]
    else:
        maxv=keys
    return maxv

#removing Number from list
def removeNumber(rlist):
    listq=[]
    for a in rlist:
        if len(a) >0:
            result = ''.join(i for i in a if not i.isdigit())
            listq.append(result)

    print("listq:",listq)
    return listq

# main method

def extractConcept():


    for term in value:
        conceptList=t.dicConcept[term]
        #print("concept lent: ",len(conceptList))
        if len(conceptList) <=0:
            print("",end='')
        else:
            print(term," : |", end='')
            for concept in conceptList:
                if len(st.dicSematnicType[concept]) >1:
                    for semantictype in duplicateSemanticType(st.dicSematnicType[concept]):  #####st.dicSematnicType[concept]
                        #entity=et.dicEntityType[semantictype]
                        if semantictype in dicProblem:
                            print("Semantic Type : ",semantictype," :" ,"Medical Concept:", "Problem")
                            #medicallist.append("problem")
                            termdic[term].append("problem");
                        elif semantictype in dicTreatment:
                            print("Semantic Type : ", semantictype, " :", "Medical Concept:", "Treatment")
                            #medicallist.append("treatment")
                            termdic[term].append("treatment");
                        elif semantictype in dicTest:
                            print("Semantic Type : ", semantictype, " :", "Medical Concept:", "Test")
                            #medicallist.append("test")
                            termdic[term].append("test");

                        else:
                            print("Semantic Type : ", semantictype, ":", "Medical Concept: ", "NONE")
                else:
                    stt=''.join(map(str,st.dicSematnicType[concept]))
                    #en=et.dicEntityType[stt]
                    if stt in dicProblem:
                        print("Semantic Type : ", stt, ":" ,"Medical Concept: ", "Problem")
                        #medicallist.append("problem")
                        termdic[term].append("problem");
                    elif stt in dicTreatment:
                        print("Semantic Type : ", stt, ":", "Medical Concept: ", "Treatment")
                       # medicallist.append("treatment")
                        termdic[term].append("treatment");
                    elif stt in dicTest:
                        print("Semantic Type : ", stt, ":", "Medical Concept: ", "Test")
                        #medicallist.append("test")
                        termdic[term].append("test");
                    else:
                        print("Semantic Type : ", stt, ":", "Medical Concept: ", "NONE")

            print("")


    print(medicallist)
    print(termdic)
    print("*********")
    for ttt in value:
        if len(termdic[ttt]) >0:
            print(ttt,": \t ", MaxConcept(termdic[ttt]))

if __name__ =='__main__':


    #value=readTextFile("Clinical Notes/Partnter Annoted.txt")  # this was for unstructured
    value=process_content()
    print('value',value)
    auth = Authentication("username","password","key") # put credential used for UMLS Browser
    apikey = auth.gettgt()
    print("main class",apikey)

#  Search Concept
    for w in value:
        print("value is", w)
        t.searchTerm(w,apikey)

# Search Semantic Type
    for cui in t.cuiList:
        st.searchSemanticType(cui,apikey)


    extractConcept()

# Search Entity Type
#     for tui in st.tuiList:
#         et.searchEntityType(tui,apikey)
# 
# 

