from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv

wiki_url = 'http://www.apples4theteacher.com/holidays/presidents-day/president-birth-states.html'
source = requests.get(wiki_url).text
soup = BeautifulSoup(source, 'html.parser')

table_pres = soup.find_all('table')
specific_table_pres = table_pres[11]


#List of Presidents and States

headers = ['President (P)', 'State of Birth (P)', 'Term (P)', 'Birthdate (P)', 'Age of Inauguration (P)', 'Previous Occupation (P)', 'Party (P)', 'Vice President']

#print(headers)

rows = []

data_rows = specific_table_pres.find_all('tr')

pres_2d = []

for a in range(44):
    row = data_rows[a + 1]
    value = row.find_all('td')
    beautified_value = []
    for dp in value:
        beautified_value.append(dp.text.strip())

    pres_2d.append(beautified_value)

pres_2d_array = np.array(pres_2d)
pres_2d_array = np.delete(pres_2d_array, 0, 1)
pres_2d_array = np.append(pres_2d_array, np.array([['Trump, Donald John', 'New York'], ['Biden, Joseph, Robinette', 'Pennsylvania']]), 0)

#print(pres_2d_array)

#List of Presidents' Term Dates, Birth Dates, and Ages at Inauguration
wiki_url2 = 'https://www.loriferber.com/research/presidential-facts-statistics/presidential-birthdates.html'
source2 = requests.get(wiki_url2).text
soup2 = BeautifulSoup(source2, 'html.parser')

table_bd = soup2.find_all('table')
specific_table_bd = table_bd[0]

rows2 = []

data_rows2 = specific_table_bd.find_all('tr')

pres_2d2 = []

for i in range(46):
    row2 = data_rows2[i + 1]
    value2 = row2.find_all('td')
    beautified_value2 = []
    for dsp in value2:
        beautified_value2.append(dsp.text.strip())

    pres_2d2.append(beautified_value2)
    
pres_bd_array = np.array(pres_2d2)
pres_bd_array = np.delete(pres_bd_array, 0, 1)
pres_bd_array = np.delete(pres_bd_array, 0, 1)
pres_bd_array = np.delete(pres_bd_array, 1, 1)
pres_bd_array = np.delete(pres_bd_array, 2, 1)
pres_bd_array = np.delete(pres_bd_array, 3, 1)
pres_bd_array = np.delete(pres_bd_array, 3, 1)
#print(pres_bd_array)

final_array = np.append(pres_2d_array, pres_bd_array, axis=1)

#print(pres_bd_array)

#Presidents' Prior Occupations
wiki_url3 = 'https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States_by_previous_experience'
source3 = requests.get(wiki_url3).text
soup3 = BeautifulSoup(source3, 'html.parser')

table_oc = soup3.find_all('table')
specific_table_oc = table_oc[0]

rows3 = []

data_rows3 = specific_table_oc.find_all('tr')

pres_2d3 = []

for j in range(46):
    row3 = data_rows3[j + 1]
    value3 = row3.find_all('td')
    beautified_value3 = []
    for osp in value3:
        beautified_value3.append(osp.text.strip())

    pres_2d3.append(beautified_value3)
    
pres_op_array = np.array(pres_2d3)
pres_op_array = np.delete(pres_op_array, -1, 1)

for k in range(7):
    pres_op_array = np.delete(pres_op_array, 0, 1)


final_array = np.append(final_array, pres_op_array, axis = 1)

#print(final_array)

#Parties of Presidents
wiki_url4 = 'https://www.thoughtco.com/presidents-and-vice-presidents-chart-4051729'
source4 = requests.get(wiki_url4).text
soup4 = BeautifulSoup(source4, 'html.parser')

table_p = soup4.find_all('table')
specific_table_p = table_p[0]

rows4 = []

data_rows4 = specific_table_p.find_all('tr')

pres_2d4 = []

for l in range(46):
    row4 = data_rows4[l + 1]
    value4 = row4.find_all('td')
    beautified_value4 = []
    for ppp in value4:
        beautified_value4.append(ppp.text.strip())

    pres_2d4.append(beautified_value4)
    
pres_pp_array = np.array(pres_2d4)

pres_vp_array = np.array(pres_2d4)
pres_vp_array = np.delete(pres_vp_array, 0, 1)
pres_vp_array = np.delete(pres_vp_array, 1, 1)
pres_vp_array = np.delete(pres_vp_array, 1, 1)

pres_pp_array = np.delete(pres_pp_array, -1, 1)

for k in range(2):
    pres_pp_array = np.delete(pres_pp_array, 0, 1)

final_array = np.append(final_array, pres_pp_array, axis = 1)

final_array1 = np.append(final_array, pres_vp_array, axis = 1)

#print(final_array1)

df = pd.DataFrame(final_array1, columns = headers)
#print(df)

df.to_csv('Presidents_In_Order_Biodata.csv', mode='w')















#Insights

from collections import Counter

partyp_listf = final_array1[:, 6 ]

for z in range(46):
    partyp=str(partyp_listf[z])

cpartyp = Counter(partyp_listf)
arr_cpartyp_listf = np.array(list(cpartyp.items()))

print(arr_cpartyp_listf)










