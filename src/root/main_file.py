'''
Created on 18 Ιουν 2018

@author: Solegem
'''
from root.text_functions import get_sentiment_of
from root.entity_lists import *
import mysql.connector
from mysql.connector import errorcode, cursor


query_sample=("SELECT COUNT(*) FROM oc_news_items WHERE {} LIMIT 150")

try:
    cnx = mysql.connector.connect(user='root', password='balalaika',host='127.0.0.1',database='rss')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    #KYRIA DIADIKASIA
    crs=cnx.cursor()
    crs.execute(query_sample.format(ent6_2))
    for an_element in crs:
        print(an_element[0]+4)
    
    crs.close()
    cnx.close()