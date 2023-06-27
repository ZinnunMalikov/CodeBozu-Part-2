from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv
import copy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

bbc_url = 'https://www.bbc.com/news/topics/cp7r8vgl2lgt/donald-trump'
source = requests.get(bbc_url).text
soup = BeautifulSoup(source, 'html.parser')

base_list = soup.find_all('a', class_='qa-heading-link lx-stream-post__header-link')
link_list = []
title_array = np.array([['Title']])
article_array = np.array([['Article', 'Positivity Score (%)']])

for a in range(len(base_list)):
    beautified_title = np.array([[base_list[a].text.strip()]])
    title_array = np.append(title_array, beautified_title, axis = 0)

    beautified_link = 'https://bbc.com' + base_list[a]['href']
    link_list.append(beautified_link)

#print(link_list)
#print(title_array)

#print('bbc.com'+link['href'])
def work(num_ind):
    global title_array
    global article_array
    global link_list
    global base_list

    inp_url = link_list[num_ind]
    mini_source = requests.get(inp_url).text
    mini_soup = BeautifulSoup(mini_source, 'html.parser')

    base_text_list = mini_soup.find_all('div', {'data-component' : 'text-block'})
    text_list = []

    for b in range(len(base_text_list)):
        beautified_text = base_text_list[b].text.strip()
        text_list.append(beautified_text)

    text_list_combined = ' '.join(text_list)
    text_list_combined_array = np.array([[(text_list_combined)]])

    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(text_list_combined)
    p_score = round(sentiment_dict['pos']*100, 1)
    pos_score_ind_array = np.array([[p_score]])

    text_list_combined_array = np.append(text_list_combined_array, pos_score_ind_array, axis = 1)
    article_array = np.append(article_array, text_list_combined_array, axis = 0)

for ni in range(len(base_list)):
    work(ni)

final_array = np.append(title_array, article_array, axis = 1)
final_array = np.delete(final_array, 0, 0)

#print(final_array)

df = pd.DataFrame(final_array, columns = ['Title', 'Article', 'Positivity Score (%)'])
print(df)

df.to_csv('Trump_BBC_Scrape.csv', mode='w')
    
