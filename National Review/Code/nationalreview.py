from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv
import copy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import spacy
nlp = spacy.load("en_core_web_sm")

score_list = []

nr_url = 'https://www.nationalreview.com/?s=trump&search-submit='
source = requests.get(nr_url).text
soup = BeautifulSoup(source, 'html.parser')

base_soup = soup.find('div', class_='post-list post-list--linear post-list--search-results')
base_lip = base_soup.find_all('h4', class_='post-list-article__title')
base_list = []

for ita in base_lip:
    sta = ita.find('a')
    base_list.append(sta)

link_list = []
title_array = np.array([['Title']])
article_array = np.array([['Article', 'Neutral Score (%)']])

for a in range(len(base_list)):
    beautified_title = np.array([[base_list[a].text.strip()]])
    title_array = np.append(title_array, beautified_title, axis = 0)

    beautified_link = base_list[a]['href']
    link_list.append(beautified_link)

def work(num_ind):
    global title_array
    global article_array
    global link_list
    global base_list
    global nlp
    global score_list

    inp_url = link_list[num_ind]
    mini_source = requests.get(inp_url).text
    mini_soup = BeautifulSoup(mini_source, 'html.parser')

    base_text_soup = mini_soup.find('div', class_='article-content')
    base_text_list = base_text_soup.find_all('p')
    text_list = []

    for b in range(len(base_text_list)):
        beautified_text = base_text_list[b].text.strip()
        text_list.append(beautified_text)

    text_list_combined = ' '.join(text_list)
    text_list_combined_array = np.array([[(text_list_combined)]])

    chunks = []
    testlist = []
    subjlist = []
    objlist = []
    pobjlist = []
    posslist = []
    aptest = []

    opt_subj = "Trump"

    text_input = text_list_combined

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

    scorepos = 0.55*(sentiment_dict2['pos']-sentiment_dict2['neg'])+0.45*(sentiment_dict1['pos']-sentiment_dict1['neg'])

    p_score = round(scorepos*100, 1)
    
    pos_score_ind_array = np.array([[p_score]])

    score_list.append(p_score)

    text_list_combined_array = np.append(text_list_combined_array, pos_score_ind_array, axis = 1)
    article_array = np.append(article_array, text_list_combined_array, axis = 0)

for ni in range(len(base_list)):
    work(ni)


final_array = np.append(title_array, article_array, axis = 1)
final_array = np.delete(final_array, 0, 0)

#print(final_array)

df = pd.DataFrame(final_array, columns = ['Title', 'Article', 'Positivity - Negativity Score (%)'])
print(df)

df.to_csv('Trump_National_Review_Scrape_Mod1_Pos_Neg.csv', mode='w')

average_score = round(sum(score_list)/len(score_list), 2)

print(score_list)
print("Average Score: " + str(average_score))

