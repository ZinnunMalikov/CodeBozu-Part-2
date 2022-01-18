from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv
import copy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import spacy
nlp = spacy.load("en_core_web_sm")

testtext = 'Jeff is an AMAZING, Wonderful, and kind person, but Bob is horrible, rude, and disgusting.'


chunks = []
testlist = []
subjlist = []
objlist = []
pobjlist = []
posslist = []
aptest = []

def analyzer_split(text_input, opt_subj):
    global nlp
    #global testtext
    global chunks
    global testlist
    global subjlist
    global aptest
    global objlist
    global pobjlist
    global posslist

    sent = copy.deepcopy(text_input)


    doc = nlp(sent)

    seen = set() # keep track of covered words

    for sent in doc.sents:
        heads = [cc for cc in sent.root.children if cc.dep_ == 'conj']

        for head in heads:
            words = [ww for ww in head.subtree]
            for word in words:
                seen.add(word)
            chunk = (' '.join([ww.text for ww in words]))
            chunks.append( (head.i, chunk) )

        unseen = [ww for ww in sent if ww not in seen]
        chunk = ' '.join([ww.text for ww in unseen])
        chunks.append( (sent.root.i, chunk) )

    chunks = sorted(chunks, key=lambda x: x[0])

    for ii, chunk in chunks:
        testlist.append(chunk)

    for item in testlist:
        doc2 = nlp(item)
        sub_toks = [tok for tok in doc2 if (tok.dep_ == "nsubj")]
        obj_toks = [tok for tok in doc2 if (tok.dep_ == "dobj")]
        pobj_toks = [tok for tok in doc2 if (tok.dep_ == "pobj")]
        poss_toks = [tok for tok in doc2 if (tok.dep_ == "nmod")]
        poss_toks2 = [tok for tok in doc2 if (tok.dep_ == "poss")]
        
        subjlist.extend(sub_toks)
        objlist.extend(obj_toks)
        pobjlist.extend(pobj_toks)
        posslist.extend(poss_toks)
        posslist.extend(poss_toks2)

        for subject in sub_toks:
            if str(subject).find(opt_subj) != -1:
                aptest.extend([item])

        for obje in obj_toks:
            if str(obje).find(opt_subj) != -1:
                if item not in aptest:
                    aptest.extend([item])

        for pobje in pobj_toks:
            if str(pobje).find(opt_subj) != -1:
                if item not in aptest:
                    aptest.extend([item])

        for posse in poss_toks:
            if str(posse).find(opt_subj) != -1:
                if (item not in aptest):
                    aptest.extend([item])
                
        
    #print(testlist)
    #print(subjlist)
    #print(objlist)
    #print(pobjlist)
    #print(posslist)
    aptestc = ' '.join(aptest)
    #print(aptest)

    sid_obj = SentimentIntensityAnalyzer()
    
    #print("Original")
    
    sentiment_dict1 = sid_obj.polarity_scores(str(' '.join(testlist)))

    #print(sentiment_dict1)

    #print("New")
    
    sentiment_dict2 = sid_obj.polarity_scores(aptestc)

    #print(sentiment_dict2)

    scorepos = 0.7*sentiment_dict2['pos']+0.3*sentiment_dict1['pos']

    print("New: " + str(scorepos))
sid_obj = SentimentIntensityAnalyzer()
origin = sid_obj.polarity_scores(testtext)

print("Your Input: " + testtext)
print("Original Score: " + str(origin['pos']*100))
analyzer_split(testtext, "Bob")
print("Referring to: Bob")



