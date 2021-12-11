import pandas as pd
from PyQt5 import QtWidgets, uic
import sys
import os
import csv
import json

filename = 'nl_words_4data.csv'
df = pd.read_csv(filename,encoding='utf-8')
list =[]

for j in range(1,251): #csv add a colum for level
    for i in range(1,21):
        if i < i*20:
            list.append(j)
df['word_level'] = list

word_id =[]
for i in range(1,5001):#add a colum to csv for word_id
    word_id.append(i)
df['word_id'] = word_id
filename2='nl_words_4datatest.csv'

df.to_csv(filename2,index=None)


# csv to json--simdilik gereksiz

# csvFilePath = 'nl_words_4datatest.csv'
""" jsonFilePath = 'nl_words_4datatest.json'

# read csv file & add to data
data = {}
with open(filename2, encoding='utf-8') as csvFile:
    csvReader = csv.DictReader(csvFile)
    for rows in csvReader:
        id = rows['word_id']
        data[id] = rows
#open json file and write data to json file
with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:

    jsonFile.write(json.dumps(data, indent=4)) """

