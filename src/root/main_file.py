'''
Created on 18 Ιουν 2018

@author: Solegem
'''
'''
Kwdikas olhs ths baskikhs analhshs. leitourgei anexarthta apo th metafrash pou ginetai stadiaka se allo script
'''
from root.text_functions import get_sentiment_of, text_filter
from root.text_functions import clean_xml_tags
from root.entity_lists import ent_total,ent_list,ent_collumn_names,count_collumn_names,sent_collumn_names
import mysql.connector
from mysql.connector import errorcode

#arithmos phgwn eidhsew kai enoiwn poy elegxoume isws na metrietai diaforetika sto telos
sources_nu=0
entities_nu=len(ent_collumn_names)

#prososrinh apothikeush twn metrisewn ana news source
total_count_list=[]
count_perent_list=[]
sent_perent_list=[]



def init_news_table():
    #TA PEDIA APO TON ENA PINAKA STON ALLO OTAN EXOUN TOUS OROUS POUS MAS ENDIAFEROUN  
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
            joined_text=an_element[1]#an kai leei joined einai mono to title emeine etsi apo prin to onoma
            joined_text=clean_xml_tags(joined_text) 
            feed_id_temp=an_element[3]
            #grammh sto neo pinaka me ta stoixeia tou paliou
            crs2.execute(insert_news.format(int(id_temp),str(joined_text),int(feed_id_temp)))
        cnx.commit()
        crs.close()
        crs2.close()
        cnx.close()


def find_entities():
    #SYMPLHRWSH TWN PEDIWN POU LENE POIA ENTITY EMFANIZONTAI STO KEIMENO
    #STON PINAKA ME TIS SXETIKES EIDHSEIS
    update_entity_fields=("UPDATE news_sentiment SET {} = 1 WHERE {}")
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
        for i,each_entity in enumerate(ent_list):
            crs.execute(update_entity_fields.format(ent_collumn_names[i],each_entity))        
        cnx.commit()
        crs.close()
        cnx.close()
        
def calc_sentiment():
    #YPOLOGISMOS KAI SYMPLHRWSH TOU PEDIOU SENTIMENT GIA OLES TIS SXETIKES EIDHSEIS
    select_for_sentiment=("SELECT id,content_en FROM news_sentiment;")
    update_sentiment=("UPDATE news_sentiment SET sent = {} WHERE id = {};")
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
        crs.execute(select_for_sentiment)
        for each_item in crs:
            cur_tile=each_item[1]
            #diwrthwsh keimenou
            cur_tile=text_filter(cur_tile)
            #sth synexeia ypolog sentiment
            sen_temp=get_sentiment_of(cur_tile)
            id_temp=each_item[0]
            crs2.execute(update_sentiment.format(sen_temp,id_temp))
            cnx.commit()
        crs.close()
        crs2.close()
        

    
def initialize_totals_table():
    #ARXIKOPOIHSH PINAKA ME TIS ATHROISTIKES METRHSEIS ANALOGA ME TA POSA FEED_EXOUME KTLP
    select_fields=("SELECT  id FROM oc_news_feeds")
    update_fields=("INSERT INTO news_totals (feed_id) VALUES ({})")
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
        crs.execute(select_fields)
        for each_item in crs:            
            crs2.execute(update_fields.format(each_item[0]))
        cnx.commit()
        crs.close()
        crs2.close()
        cnx.close() 
      
def calc_lenghts():
    #YPOLOGISMOS MEGETHOUS KAI DHMIOURGIA KENWN LISTWN OPOU THA APOTHKEYTHOUN PROSORINA TA ATHROISTIKA(ANA FEED SOURCE)
    #DEDOMENA (ARITHMOS EID. - SENTIMENT) PRIN MPOYN STON PINAKA TOUS
    #MIPWS DE XREIAZOTAN AN HTAN NA KANOUME APPEND STH calc_total_s (?) mpa kalytera etsi
    calc_size=("SELECT  COUNT(*) FROM news_totals")
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
        crs.execute(calc_size)
        
        for element in crs:
            #poses einai oi phges mia fora ekteleitai alla thelei for gia na paroume th timh
            sources_nu=element[0]
            #initialize apla to megethos tws listwn wste na einai genika dynamiko (px future ergaleio tyxaia db)
            for ind in range(0,sources_nu):
                total_count_list.append(0)
                count_perent_list.append([0]*entities_nu)
                sent_perent_list.append([0]*entities_nu)
        cnx.commit()
        crs.close()
        cnx.close()

def calc_total_s():
    #YPOLOGISMOS TIMWN ATHROISTIKOU SENTIMENT KAI ARITHMOU EIDHSEWN KAI EISGAGWGH STIS PARAPANW PROSORINES LISTES
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
        select_values=("SELECT  * FROM news_sentiment;")    
        #gemisma twn listwn poy ua eisaxthoun ston synoliko pinaka
        crs=cnx.cursor(buffered=True)
        crs.execute(select_values)        
        for each_item in crs:
            total_count_list[each_item[3]-82]+=1
            #try:
            for ind,nu_val in enumerate(each_item):
                if ind >=4 and ind <= entities_nu+3 and nu_val==1:
                    count_perent_list[each_item[3]-82][ind-4]+=1 #to poses fores anaferetai h kathe enoia
                    sent_perent_list[each_item[3]-82][ind-4]+=each_item[16]#ta sentiment athroistika
        cnx.commit()
        crs.close()
        cnx.close() 
        
def totals_to_table():
    #APO TIS PROSORINES LISTES TELIKA STON ATHROISTIKO PINAKA STH DB
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
        #gemisma twn listwn poy ua eisaxthoun ston synoliko pinaka
        crs=cnx.cursor(buffered=True)       
        for ind,total_nu in enumerate(total_count_list):
            #diamorfosh twn swstwn MYSQL queries
            update_counts=("UPDATE news_totals SET ")
            update_sentiments=("UPDATE news_totals SET ")
            update_total_count=("UPDATE news_totals SET total_count= {} WHERE feed_id ={}")
            for ii,name in enumerate(count_collumn_names):
                update_counts+=name+' = '+ str(count_perent_list[ind][ii])+', '
            for ii,name in enumerate(sent_collumn_names):
                update_sentiments+=name+' = '+ str(sent_perent_list[ind][ii])+', '
            update_counts=update_counts[:-2]#koboume teleytaio komma kai keno
            update_counts+=" WHERE feed_id={} ;".format(ind+82)
            update_sentiments=update_sentiments[:-2]#koboume teleytaio komma kai keno
            update_sentiments+=" WHERE feed_id={} ;".format(ind+82)
            #gia to synoliko
            crs.execute(update_counts)
            crs.execute(update_sentiments)
            crs.execute(update_total_count.format(total_nu,ind+82))
        cnx.commit()
        crs.close()
        cnx.close() 
                               
#KYRIA DIADIKASIA
#init_news_table() #mono mia fora xreiazetai
#find_entities() # mono mia fora
#calc_sentiment() #mono mia fora alla exartatai
#initialize_totals_table() #mono mia fora
#calc_lenghts() #kathe fora
#calc_total_s() #kathe fora
#totals_to_table()#mia fora
