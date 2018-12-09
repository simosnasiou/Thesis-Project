'''
Created on 30 Οκτ 2018

@author: Solegem
'''
'''
Telikoi ypologismoi pou sxetizontai me thn antikeimenikothta (gia to kefalaio 7 dld)
exagwgh kai se arxeia kai grafimata
'''
from root.export_results import total_counts_table,names_table,percentage_table
from root.export_results import mean_sentiment_table,grouped_mean_sentiment_array
from root.main_file import entities_nu
import numpy as np
import plotly as py
import plotly.graph_objs as go

#Kratame listes mono me tis 'megales' phges gia na exoume kalytera pososta
limited_names_table=[]
liminted_percentage_table=[]

def difference_sort (ar):
    return ar[1][0]+ ar[1][1]-(ar[1][2]+ar[1][2])

#OI DIAFORES SYNARTHSEIS GIA TAXINOMISH
def distance_sort (ar):
    return ar[1]

def form_limited_tables ():
    #Ppoly mikres phges exoun endexomenws 'fouskwmena' pososta anaforas
    #Oria panw apo to opoio tha theorountai axiopista ta pososta anaforas stis enoies
    totals_threshold= 90
    
    #prosorinoi pinakes
    lim_nam_table_tmp=[]
    lim_per_table_tmp=[] 

    for i,content in enumerate(total_counts_table):
        if content >=totals_threshold:
            lim_per_table_tmp.append(percentage_table[i])
            lim_nam_table_tmp.append(names_table[i])
    
    return lim_nam_table_tmp,lim_per_table_tmp
            

def selection_based_obj_ranking (in_func):     
    #TAXINWMISH ME BASH DIAFORA BASIKWN ENOIWN - POSOSTO EIDHSEWN  CUSTOM SYNARTHSH   
    names_and_percent=list(zip(limited_names_table,liminted_percentage_table))
    
    #taxinwmisi apo to megalytero sto mirkotero gia kapoia thesh
    names_and_percent.sort(key= in_func,reverse=True)
    #kai exodos
    out_list=[]
    for i in names_and_percent:
        #print(i[0],in_func(i))
        out_list.append([i[0],in_func(i)])
    return out_list

   
def distance_based_obj_ranking ():    
    #TAXINOMISH ME BASH DIAFORA DIANISMATWN - POSOSTO EIDHSEWN
    #array mesou orou posotou eidhsewn ana enoia se ola ta mesa
    avg_array=[0]*entities_nu
    for i in liminted_percentage_table:
        for j,ii in enumerate (i):
            avg_array[j]+=ii
    for i,co in enumerate(avg_array):
        avg_array[i]=co/len(names_table)

    
    #Sto numpy
    avg_vector=np.array(avg_array)
    distance_array=[]
    for i in liminted_percentage_table:
        temp_vector=np.array(i)
        dist_vector=temp_vector-avg_vector
        distance_array.append(np.linalg.norm(dist_vector))
    
    names_and_distance=list(zip(limited_names_table,distance_array))
    
    names_and_distance.sort(key=distance_sort, reverse=True)
    return (names_and_distance) 

def sentiment_based_obj_ranking ():    
    #ANTISTOISH DIADIKASIA ME TO SENTIMENT AYTH TH FORA
    #TAXINOMISH ME BASH DIAFORA DIANISMATWN - SENTIMENT EIDHSEWN
    
    #Sto numpy kateytheian giati edw meso oro exoume
    avg_sent_vector=np.array(grouped_mean_sentiment_array)
    sent_distance_array=[]
    for i in mean_sentiment_table:
        temp_sent_vector=np.array(i)
        sent_dist_vector=temp_sent_vector-avg_sent_vector
        sent_distance_array.append(np.linalg.norm(sent_dist_vector))
    
    names_and_sentiment_distance=list(zip(names_table,sent_distance_array))
    names_and_sentiment_distance.sort(key=distance_sort, reverse=True)
    return (names_and_sentiment_distance)

#TWRA THELOUME 2 MODULAR SYNARTHSEIS. MIA GIA BAR CHART STO PLOTLY KAI MIA GIA TXT
def list_to_file(in_list,file_name='exported_list',title_msg='Τίτλος'):
    #Synarthsh ektypwshs se arxeio keimenou
    try:
        data_file_out =open(file_name+'.txt','w')
    except IOError:
        print("A error occured opening export File")
    else:
        data_file_out.write(title_msg+"\n\n")
        for row in in_list:            
            #EKTYPWSH STO ARXEIO
            temp_string=("{:30.28}: {:6.3f}  \n".format(row[0],row[1]))
            data_file_out.write(temp_string)
        data_file_out.close()

def list_to_bar_chart (in_list,file_name='exported_bar_chart',graph_title='Kάτι προσορινό'):             
    #BAR CHART GIA TH KATHE LISTA ME TO PLOTLY
    names_axis=[]
    data_axis=[]
    for indx,ii in enumerate(in_list):
        names_axis.append(ii[0]+' -  '+str(indx))#gia monadiko onoma
        data_axis.append(ii[1])
    #basiko trace gia to grafhma
    trace_temp = go.Bar(        
        x = names_axis,
        y=data_axis,
       )
        

    data = [trace_temp]
    layout = go.Layout(
    title = graph_title
    )
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename=file_name+'.html')

#EKTELESH
limited_names_table,liminted_percentage_table=form_limited_tables()

sel_r=selection_based_obj_ranking(difference_sort)
list_to_file(sel_r, file_name='selection_ranking', title_msg='Κατάταξη με βάση την αναφορά των ειδήσεων στη κυβέρνηση σε σχέση με την αντιπολίτευση')
list_to_bar_chart(in_list=sel_r, file_name='selection_ranking', graph_title='Αναφορά ειδήσεων σε Κυβέρνηση - Αντιπολίτευση')

dis_r=distance_based_obj_ranking()
list_to_file(dis_r, file_name='distance_ranking', title_msg='Κατάταξη με βάση τη διαφορά από το διάνυσμα του μέσου ποσοσστού των ειδήσεων')
list_to_bar_chart(in_list=dis_r, file_name='distance_ranking', graph_title='Κατάταξη με βάση τη διαφορά από το διάνυσμα του μέσου ποσοσστού των ειδήσεων')

sent_r=sentiment_based_obj_ranking()
list_to_file(sent_r, file_name='sent_ranking', title_msg='Κατάταξη με βάση τη διαφορά από το διάνυσμα του μέσου sentiment των ειδήσεων')
list_to_bar_chart(in_list=sent_r, file_name='sent_ranking', graph_title='Κατάταξη με βάση τη διαφορά από το διάνυσμα του μέσου sentiment των ειδήσεων')



