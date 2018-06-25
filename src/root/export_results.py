'''
Created on 23 Ιουν 2018

@author: Solegem
'''
import mysql.connector
from mysql.connector import errorcode
from root.entity_lists import ent_names
from root.main_file import entities_nu
import plotly.offline as of
import plotly.graph_objs as go



#THA KRATAEI TA ONOMATA TOU KATHE NEWS SOURCE GIA NA TA EXOUME PROS EMFANISH
names_table=[]
#THA KRATAEI TO SYNOLIKO COUNT EIDHSEWN TOU KATHE SOURCE
total_counts_table=[]
#THA KRATAEI TA EPI MEROUS (ANA ENTITY) COUNT EDISHSEWN
counts_perent_table=[]
#THA KRATAEI TA EPI MEROUS (ANA ENTITY) SENTIMENT EDISHSEWN
sent_perent_table=[]

#SYNARTHSH POU GEMIZEI TON PARAPANW names_table
def fill_names_table():
    #ARXIKOPOIHSH PINAKA ME TIS ATHROISTIKES METRHSEIS ANALOGA ME TA POSA FEED_EXOUME KTLP
    select_names=("SELECT  title FROM oc_news_feeds ORDER BY id;")
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
        crs.execute(select_names)
        for each_item in crs:            
            names_table.append(each_item[0])
        crs.close()
        cnx.close() 

#SYNARTHSH POU GEMIZEI TOUS PINAKES ME TA SENTIMENT KAI COUNT
def fill_data_tables():
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
        select_data=("SELECT * FROM news_totals;")
        crs=cnx.cursor(buffered=True)
        crs.execute(select_data)
        for ii,each_item in enumerate(crs):
            counts_perent_table.append([])
            sent_perent_table.append([])
            #gemisma pinaka me synoliko count eidhsewn
            total_counts_table.append(each_item[len(each_item)-1])
            for ix,content in enumerate(each_item):
                #gemisma pinaka me ta count
                if ix>=1 and ix<=entities_nu:
                    counts_perent_table[ii].append(content)
                #gemisma pinaka me ta sentiment
                elif ix>= entities_nu+1 and ix<= entities_nu*2:
                    sent_perent_table[ii].append(content)
        crs.close()
        cnx.close()
            
            
def print_to_text():
    #EDW EXPORT TWN SYNOLIKWN APOTELESMATWN SE ENA .txt ARXEIO
    try:
        data_file_out =open('end_results.txt','w')
    except IOError:
        print("A error occured opening export File")
    else:
        data_file_out.write("Οδηγίες ανάγνωσης:\n")
        data_file_out.write("M.S= μέσο sentiment (από όλες τις ειδήσεις που αναφέρονται στη κάθε ένοια από το κάθε μέσο)\nαπό -1 για απολύτως αρνητική γνώμη εώς +1 για απολύτως θετική\n")
        data_file_out.write("A.E = αριθμός ειδήσεων που αναφέρονται στην εκάστοτε έννοια δοσμένος και ποσοστιαία σε σχέση με τις συνολικές\n\n")
        for ii,name in enumerate(names_table):
            data_file_out.write('{} - συνολικές ειδήσεις: {}\n\n'.format(name,total_counts_table[ii]))
            temp_string=''
            for ix,nm in enumerate(ent_names):
                ae=counts_perent_table[ii][ix]
                if ae !=0:
                    ms=sent_perent_table[ii][ix]/ae
                else:
                    ms=0
                if total_counts_table[ii] !=0:
                    percent=ae/total_counts_table[ii]*100
                else:
                    percent=0
                temp_string+=("{:15}:     Μ.S: {:6.3f}     A.E: {:5} - {:6.2f}%  \n".format(nm,ms,ae,percent))
            data_file_out.write(temp_string+'\n\n')
        data_file_out.close()
    
def produce_graphs():
    #EDW EXPORT TWN SYNOLIKWN APOTELESMATWN SE HTML GRAFIKES PARASTASEIS ME TO PLOTLY
    
    #ta xrwmata oste na parapempoun sto politiko fasma kai na mhn einai tyxaia
    party_colors=[
        'rgb(249, 192, 117)','rgb(239, 158, 52)',
        'rgb(39, 68, 173)','rgb(48, 48, 255)',
        'rgb(81, 81, 81)','rgb(35, 35, 35)',
        'rgb(76, 165, 69)','rgb(46, 102, 42)',
        'rgb(219, 53, 35)','rgb(168, 28, 28)',
        'rgb(239, 236, 67)','rgb(175, 156, 29)']
    #seitra apo traces gia na prosthethoun sto grafhma
    traces=[]
    for ii,ent in enumerate(ent_names):
        yy=[]
        labels_temp=[]
        for ix,t_co in enumerate(total_counts_table):
            co=counts_perent_table[ix][ii]
            labels_temp.append('αρ.ειδ: '+str(co))
            if co !=0:
                yy.append(sent_perent_table[ix][ii]/co)
            else:
                yy.append(0)
        trace_temp = go.Bar(
            #x=names_table,
            #x=total_counts_table,
            x = [names_table[i] +' - αρ.ειδ: '+ str(total_counts_table[i]) for i in range(len(names_table))],
            y=yy,
            text=labels_temp,
            marker=dict(
                color=party_colors[ii]
            ),        
        name=ent
        )
        
        traces.append(trace_temp)

    data = traces
    layout = go.Layout(
    barmode='group',
    title='Μέσο Sentiment Ανά Ειδησεογραφική Πηγή και Πολ.Αρχηγό - Παράταξη'
    )

    fig = go.Figure(data=data, layout=layout)
    of.plot(fig, filename='median_sentiment_graph.html')

fill_names_table()
fill_data_tables()
print_to_text()
produce_graphs()