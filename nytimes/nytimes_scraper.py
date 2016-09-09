# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 13:19:43 2015

@author: aditya
"""


# Import all the important packages which we must use with this program
import nytimesarticle
from nytimesarticle import articleAPI

import csv
import time
import pandas as pd

# Import some particular modules from the packages



# Create access to the API

api = articleAPI('32d8376f8a1745528959a1b43251238d')


#Run a simple query
articles = api.search( q = 'Obama',
     fq = {'headline':'Obama', 'source':['Reuters','AP', 'The New York Times']},
     begin_date = 20111231 )



     
# View the created object
articles


# Create a function to clean the articles and parse only some of the relevant elements
def parse_articles(articles):
    '''
    This function takes in a response to the NYT api and parses
    the articles into a list of dictionaries
    '''
    news = []
    print(articles)
    for i in articles['response']['docs']:
        dic = {}
        dic['id'] = i['_id']
        if i['abstract'] is not None:
            dic['abstract'] = i['abstract'].encode("utf8")
        dic['headline'] = i['headline']['main'].encode("utf8")
        dic['desk'] = i['news_desk']
        dic['date'] = i['pub_date'][0:10] # cutting time of day.
        dic['section'] = i['section_name']
        if i['snippet'] is not None:
            dic['snippet'] = i['snippet'].encode("utf8")
        dic['source'] = i['source']
        dic['type'] = i['type_of_material']
        dic['url'] = i['web_url']
        dic['word_count'] = i['word_count']
        # locations
        locations = []
        for x in range(0,len(i['keywords'])):
            if 'glocations' in i['keywords'][x]['name']:
                locations.append(i['keywords'][x]['value'])
        dic['locations'] = locations
        # subject
        subjects = []
        for x in range(0,len(i['keywords'])):
            if 'subject' in i['keywords'][x]['name']:
                subjects.append(i['keywords'][x]['value'])
        dic['subjects'] = subjects   
        news.append(dic)
    return(news) 

# View the parsed article which is much clearer to view
articles_parsed = parse_articles(articles)
# Print as Json format
#print("Printing parsed article here:  ",articles_parsed)




# write a function to extract data for any query search string and date

def get_articles(date,query):
    '''
    This function accepts a year in string format (e.g.'2008')
    and a query (e.g.'Amnesty International') and it will 
    return a list of parsed articles (in dictionaries)
    for that year.
    '''
    all_articles = []
    for i in range(0,50): #NYT limits pager to first 50 pages. But rarely will you find over 
    #50 pages of results anyway.
        articles = api.search(q = query,
               fq = {'source':['Reuters','AP', 'The New York Times']},
               begin_date = date + '0101',
               end_date = date + '1231',
              # sort='oldest',
               page = str(i))
        articles = parse_articles(articles)
        all_articles = all_articles + articles
    return(all_articles)



 
# Create an empty list to which we will keep on adding extracted articles
    
Amnesty_all = []

# Create the complete list by extracting all URLs for each year

for i in range(2008,2014):
    print('Processing' + str(i) + '...')
    Amnesty_year =  get_articles(str(i),'Amnesty International')
    Amnesty_all = Amnesty_all + Amnesty_year
    time.sleep(60)
    

    
# Create a structure for the csv file
keys = ['headline',
 'abstract',
 'desk',
 'locations',
 'word_count',
 'snippet',
 'source',
 'subjects',
 'url',
 'section',
 'date',
 '_id',
 'type',
 'id']

# Create the csv file

with open('amnesty-related.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(Amnesty_all)
    
# Retrieve the data stored in MongoDB into pandas dataframe 
    
#input_data = db.amnesty
#data = pd.DataFrame(list(input_data.find()))


# Retrieve the data stored in csv files into pandas dataframe

#import pandas as pd
df = pd.read_csv('amnesty-related.csv')
#####################################################
#import pymongo
#from pymongo import MongoClient
#from nytimesarticle import articleAPI

# Connect to the MongoDB
#connection = MongoClient('localhost', 27017)

# Connect to the nytimes database
#db = connection.nytimes_amnesty

# Create a collection which will hold all the documents
#amnesty_art=db.amnesty_art

# Insert the entire data into MongoDB
#amnesty_art.insert(Amnesty_all)

