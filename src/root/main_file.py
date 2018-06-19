'''
Created on 18 Ιουν 2018

@author: Solegem
'''
'''
Kwdikas olhs ths baskikhs analhshs. leitourgei anexarthta apo th metafrash pou ginetai stadiaka se allo script
'''
from root.text_functions import get_sentiment_of
from root.text_functions import clean_xml_tags
from root.entity_lists import *
import mysql.connector
from mysql.connector import errorcode,cursor

def init_news_table():
    #prwta pedia ston pinaka    
    select_news=("SELECT id,title,body,feed_id FROM oc_news_items WHERE {};")
    insert_news= ("INSERT INTO news_sentiment (id,content_gr,feed_id) VALUES ({},'{}',{});")
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
        crs=cnx.cursor(buffered=True)#poly shmatniko na einai buffered
        crs2=cnx.cursor(buffered=True)
        crs.execute(select_news.format(ent_total))
        for an_element in crs:
            id_temp=an_element[0]
            joined_text=an_element[1]#body kai title mazi
            joined_text=clean_xml_tags(joined_text) 
            feed_id_temp=an_element[3]
            #grammh sto neo pinaka me ta stoixeia tou paliou
            crs2.execute(insert_news.format(int(id_temp),str(joined_text),int(feed_id_temp)))
        cnx.commit()
        crs.close()
        crs2.close()
        cnx.close()

#KYRIA DIADIKASIA
#init_news_table() #mono mia fora xreiazetai
