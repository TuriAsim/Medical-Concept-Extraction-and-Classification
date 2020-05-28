import argparse
#import Classes.SecondClass as s
from collections import defaultdict


import pandas as pd
import numpy as np
from collections import defaultdict
from statistics import mode
import nltk
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import PunktSentenceTokenizer
# import DatabaseOperation as



import nltk.data

import  re


mylist= ['simple','atheroma','thoracic','he in the there','aorta','are simple','simple atheroma','in the','descending thoracic','there is here','where there','there are simple', 'are simple atheroma'] #'thoracic aorta', 'there are simple', 'are simple atheroma', 'atheroma in the', 'in the descending', 'the descending thoracic', 'descending thoracic aorta', 'there are simple atheroma', 'simple atheroma in the', 'in the descending thoracic', 'the descending thoracic aorta', 'there are simple atheroma in', 'atheroma in the descending thoracic', 'in the descending thoracic aorta']


def stop_word(word_tokens):

    stop_words = set(stopwords.words('english'))
    print("stopwordlist",stop_words)
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


printlist = stop_word(mylist)

print(printlist)