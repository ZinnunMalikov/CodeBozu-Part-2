from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv

politico_url = 'https://www.politico.com/news/magazine/2021/01/18/trump-presidency-administration-biggest-impact-policy-analysis-451479'
source = requests.get(politico_url).text
soup = BeautifulSoup(source, 'html.parser')

things_list = soup.find_all('h3')
things_array = np.array([['Things']])

for a in range(len(things_list)):
    things_list[a] = things_list[a].text.strip()
    things_array = np.append(things_array, np.array([[things_list[a]]]), axis = 0)

#print(things_array)

story_div_identifier = soup.find_all('div', class_='story-text')
story_p_identifier = soup.find_all('p', class_='story-text__paragraph')

semifinal_array = np.array([['Move', 'Impact', 'Upshot']])

def no_div_extract():
    global semifinal_array

    takeaway = story_p_identifier[66:69]

    for a in range(len(takeaway)):
        takeaway[a] = takeaway[a].text.strip()

        bad_chars = ['The move:', 'The impact:', 'The upshot:']

        for b in range(3):
            if takeaway[a].find(bad_chars[b]) != -1:
                takeaway[a]=takeaway[a].replace(bad_chars[b], '')

    row_take = np.array([takeaway])
    #print(row_take)
    semifinal_array = np.append(semifinal_array, row_take, 0)
    #print(semifinal_array)
    #print(semifinal_array.shape)

def single_extract(div_index):
    global semifinal_array
    
    mini_soup = story_div_identifier[div_index]
    story_p = mini_soup.find_all('p')

    takeaway = story_p[1:4]

    for a in range(len(takeaway)):
        takeaway[a] = takeaway[a].text.strip()

        bad_chars = ['The move:', 'The impact:', 'The upshot:']

        for b in range(3):
            if takeaway[a].find(bad_chars[b]) != -1:
                takeaway[a]=takeaway[a].replace(bad_chars[b], '')

    row_take = np.array([takeaway])
    #print(row_take)
    semifinal_array = np.append(semifinal_array, row_take, 0)
    #print(semifinal_array)
    #print(semifinal_array.shape)
    
def double_extract(div_index):
    global semifinal_array
    
    mini_soup = story_div_identifier[div_index]
    story_p = mini_soup.find_all('p')

    takeaway = story_p[1:4]
    takeaway2 = story_p[6:9]

    for a in range(len(takeaway)):
        takeaway[a] = takeaway[a].text.strip()
        takeaway2[a] = takeaway2[a].text.strip()
        
        bad_chars = ['The move:', 'The impact:', 'The upshot:']

        for b in range(3):
            if takeaway[a].find(bad_chars[b]) != -1:
                takeaway[a]=takeaway[a].replace(bad_chars[b], '')
            if takeaway2[a].find(bad_chars[b]) != -1:
                takeaway2[a]=takeaway2[a].replace(bad_chars[b], '')


    row_take = np.array([takeaway])
    row_take2 = np.array([takeaway2])
    #print(row_take)
    semifinal_array = np.append(semifinal_array, row_take, 0)
    semifinal_array = np.append(semifinal_array, row_take2, 0)
    #print(semifinal_array)
    #print(semifinal_array.shape)

def triple_extract():
    global semifinal_array
    
    mini_soup = story_div_identifier[19]
    story_p = mini_soup.find_all('p')

    takeaway = story_p[1:4]
    takeaway2 = story_p[6:9]
    takeaway3 = story_p[11:14]

    for a in range(len(takeaway)):
        takeaway[a] = takeaway[a].text.strip()
        takeaway2[a] = takeaway2[a].text.strip()
        takeaway3[a] = takeaway3[a].text.strip()
        
        bad_chars = ['The move:', 'The impact:', 'The upshot:']

        for b in range(3):
            if takeaway[a].find(bad_chars[b]) != -1:
                takeaway[a]=takeaway[a].replace(bad_chars[b], '')
            if takeaway2[a].find(bad_chars[b]) != -1:
                takeaway2[a]=takeaway2[a].replace(bad_chars[b], '')
            if takeaway3[a].find(bad_chars[b]) != -1:
                takeaway3[a]=takeaway3[a].replace(bad_chars[b], '')


    row_take = np.array([takeaway])
    row_take2 = np.array([takeaway2])
    row_take3 = np.array([takeaway3])
    #print(row_take)
    semifinal_array = np.append(semifinal_array, row_take, 0)
    semifinal_array = np.append(semifinal_array, row_take2, 0)
    semifinal_array = np.append(semifinal_array, row_take3, 0)
    #print(semifinal_array)
    #print(semifinal_array.shape)

def move_only_extract():
    global semifinal_array

    mini_soup = story_div_identifier[5]
    story_p = mini_soup.find_all('p')

    takeaway = story_p[1:5]

    for a in range(len(takeaway)):
        takeaway[a] = takeaway[a].text.strip()

        bad_chars = ['The move:', 'The impact:', 'The upshot:']

        for b in range(3):
            if takeaway[a].find(bad_chars[b]) != -1:
                takeaway[a]=takeaway[a].replace(bad_chars[b], '')

    takeaway[1] = takeaway[0]+' '+takeaway[1]
    del takeaway[0]
    combined_move = '   '.join(takeaway)
    takeaway = [combined_move, '','']

    row_take = np.array([takeaway])
    #print(row_take)
    semifinal_array = np.append(semifinal_array, row_take, 0)
    #print(semifinal_array)
    #print(semifinal_array.shape)

for n in range(3, 5+1):
    single_extract(n-1)
    
move_only_extract()

single_extract(7-1)
double_extract(8-1)
single_extract(9-1)
double_extract(10-1)
single_extract(11-1)
single_extract(12-1)

no_div_extract()

double_extract(13-1)
single_extract(14-1)
double_extract(15-1)
single_extract(16-1)
single_extract(17-1)
double_extract(18-1)
single_extract(19-1)

triple_extract()

for n in range(21, 24+1):
    single_extract(n-1)

#print(semifinal_array.shape)

final_array = np.append(things_array, semifinal_array, axis=1)
final_array = np.delete(final_array, 0, 0)

#print(final_array.shape)

df = pd.DataFrame(final_array, columns = ['Things', 'Move', 'Impact', 'Upshot'])

print(df)

df.to_csv('Trump_Politico_Scrape_Text_Only.csv', mode='w')




#VADER
import copy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

positive_array = None
neutral_array = None
negative_array = None

def sentiment_analyze(obj, num):
    global positive_array
    global neutral_array
    global negative_array
 
    sid_obj = SentimentIntensityAnalyzer()
 
    #sentiment_dict = sid_obj.polarity_scores(sentence)

    if num == 1:
        positive_array = copy.deepcopy(obj)
        for rw in range(np.shape(obj)[0]-1):
            for cl in range(np.shape(obj)[1]):
                sentiment_dict = sid_obj.polarity_scores(obj[rw+1][cl])
                pos_score = round(sentiment_dict['pos']*100, 3)
                
                positive_array[rw+1][cl] = pos_score

        move_pos=0
        for rw in range(np.shape(positive_array)[0]-1):
            move_pos = move_pos + float(positive_array[rw+1][0])/(np.shape(positive_array)[0]-1)

        col_pos=0
        for rw in range(np.shape(positive_array)[0]-1):
            col_pos = col_pos + float(positive_array[rw+1][1])/(np.shape(positive_array)[0]-2)

        ups_pos=0
        for rw in range(np.shape(positive_array)[0]-1):
            ups_pos = ups_pos + float(positive_array[rw+1][2])/(np.shape(positive_array)[0]-2)

        avgs_pos = np.array([['Average', round(move_pos, 3), round(col_pos, 3), round(ups_pos, 3)]])

        positive_array = np.append(things_array, positive_array, axis=1)

        positive_array = np.append(positive_array, avgs_pos, axis=0)

        positive_array = np.delete(positive_array, 0, 0)

        pos_df = pd.DataFrame(positive_array, columns = ['Things', 'Move (Positive %)', 'Impact (Positive %)', 'Upshot (Positive %)'])

        print(pos_df)

        pos_df.to_csv('Trump_Politico_Scrape_Positive_Percent.csv', mode='w')

    if num == 0:
        neutral_array = copy.deepcopy(obj)
        for rw in range(np.shape(obj)[0]-1):
            for cl in range(np.shape(obj)[1]):
                sentiment_dict = sid_obj.polarity_scores(obj[rw+1][cl])
                neu_score = round(sentiment_dict['neu']*100, 3)
            
                neutral_array[rw+1][cl] = neu_score

        move_neu=0
        for rw in range(np.shape(neutral_array)[0]-1):
            move_neu = move_neu + float(neutral_array[rw+1][0])/(np.shape(neutral_array)[0]-1)

        col_neu=0
        for rw in range(np.shape(neutral_array)[0]-1):
            col_neu = col_neu + float(neutral_array[rw+1][1])/(np.shape(neutral_array)[0]-2)

        ups_neu=0
        for rw in range(np.shape(neutral_array)[0]-1):
            ups_neu = ups_neu + float(neutral_array[rw+1][2])/(np.shape(neutral_array)[0]-2)

        avgs_neu = np.array([['Average', round(move_neu, 3), round(col_neu, 3), round(ups_neu, 3)]])

        neutral_array = np.append(things_array, neutral_array, axis=1)

        neutral_array = np.append(neutral_array, avgs_neu, axis=0)

        neutral_array = np.delete(neutral_array, 0, 0)

        neu_df = pd.DataFrame(neutral_array, columns = ['Things', 'Move (Neutral %)', 'Impact (Neutral %)', 'Upshot (Neutral %)'])

        print(neu_df)

        neu_df.to_csv('Trump_Politico_Scrape_Neutral_Percent.csv', mode='w')
        
    if num == -1:
        negative_array = copy.deepcopy(obj)
        for rw in range(np.shape(obj)[0]-1):
            for cl in range(np.shape(obj)[1]):
                sentiment_dict = sid_obj.polarity_scores(obj[rw+1][cl])
                neg_score = round(sentiment_dict['neg']*100, 3)
            
                negative_array[rw+1][cl] = neg_score

        move_neg=0
        for rw in range(np.shape(negative_array)[0]-1):
            move_neg = move_neg + float(negative_array[rw+1][0])/(np.shape(negative_array)[0]-1)

        col_neg=0
        for rw in range(np.shape(negative_array)[0]-1):
            col_neg = col_neg + float(negative_array[rw+1][1])/(np.shape(negative_array)[0]-2)

        ups_neg=0
        for rw in range(np.shape(negative_array)[0]-1):
            ups_neg = ups_neg + float(negative_array[rw+1][2])/(np.shape(negative_array)[0]-2)

        avgs_neg = np.array([['Average', round(move_neg, 3), round(col_neg, 3), round(ups_neg, 3)]])

        negative_array = np.append(things_array, negative_array, axis=1)

        negative_array = np.append(negative_array, avgs_neg, axis=0)

        negative_array = np.delete(negative_array, 0, 0)

        neg_df = pd.DataFrame(negative_array, columns = ['Things', 'Move (Negative %)', 'Impact (Negative %)', 'Upshot (Negative %)'])

        print(neg_df)

        neg_df.to_csv('Trump_Politico_Scrape_Negative_Percent.csv', mode='w')
        
    #print("Overall sentiment dictionary is : ", sentiment_dict)

sentiment_analyze(semifinal_array, 1)
sentiment_analyze(semifinal_array, 0)
sentiment_analyze(semifinal_array, -1)



