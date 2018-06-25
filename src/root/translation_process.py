'''
Created on 20 Ιουν 2018

@author: Solegem
'''
'''
Edw anexartita apo ton ypoloipo kwdika trexoume ayto wste na pairnoyme oloena kai megalytero ogo metafrashs
'''

import mysql.connector
from mysql.connector import errorcode
from root.text_functions import translate, clean_xml_tags

def translate_part():
    abs_lower_id_limit=123765
    abs_upper_id_limit=653466
    lower_id_limit=653469
    upper_id_limit=653470
    #symplirwsh twn pediwn pou exoun na kanoun me to poio entity emfanizetai sto keimeno
    select_for_translation=("SELECT content_gr FROM news_sentiment WHERE id = {}")
    update_translation=("UPDATE news_sentiment SET content_en = '{}' WHERE id = {}")
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
        crs=cnx.cursor(buffered=True)
        crs2=cnx.cursor(buffered=True)
        for i in range(lower_id_limit,upper_id_limit):
            crs.execute(select_for_translation.format(i))
            for each_item in crs:
                text_ft=translate(each_item)
                text_ft=clean_xml_tags(text_ft)
                crs2.execute(update_translation.format(text_ft,i))        
        cnx.commit()
        crs.close()
        cnx.close()

#Ektelesh
translate_part()       