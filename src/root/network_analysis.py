'''
Created on 5 Σεπ 2018

Se ayto to arxeio tha perasoume ta apotelesmata mas se dyktio kai tha prospathhsoume 
na katalhxoume se orismena symperasmata se sxesh me ayto
epishs data visualization

@author: Solegem
'''


import networkx as nx
from networkx.algorithms import bipartite
from root.export_results import sent_perent_table,counts_perent_table
from root.export_results import thresh
from root.export_results import names_table
from root.entity_lists import ent_names
from networkx.algorithms.bipartite.projection import generic_weighted_projected_graph
from networkx.algorithms.community import asyn_lpa_communities 
from networkx.algorithms.community.asyn_fluidc import asyn_fluidc
from networkx.algorithms.community import kernighan_lin_bisection, girvan_newman
from networkx import edge_betweenness_centrality
import itertools
from plotly.offline import plot, offline
from plotly.graph_objs import *
import numpy as np
from builtins import dict

#gia na mhn exoume duplicate -> prepei monadiko onoma node -> ara kolame kai ena id apo th DB
names_table_unique=[str(y)+' - '+x for x, y in zip(names_table, list(range(82,159)))]   

def make_main_graph():
    #KATASKEYH TOY KYRIOU GRAPHIMATOS ME TIS SXESEIS MESWN - POLITIKWN ONTOTHTWN
    #MONO NODES EDW - EDGES KATW TAYTOXRONA ME TON PINAKA
    main_graph =nx.Graph()   
    main_graph.add_nodes_from(names_table_unique,bipartite=0)
    main_graph.add_nodes_from(ent_names,bipartite=1)
    
    #ypolgismos toy pinaka me ta sentiment (epeidh den apothhkeyetai telika an kai xrhsimopoietai) 
    #sto export results)
    mean_sent_table=sent_perent_table
    for xx,each_line in enumerate(mean_sent_table):
        for ii,each_cell in enumerate(each_line):
            co=counts_perent_table[xx][ii]
            #MPOROUME NA BGALOUME TO THRESH KAI NA BALOUME 0 (MHDEN) AN THELOUME TA PANTA
            if co >=thresh:
                #symplhrwsh pinaka            
                mean_sent_table[xx][ii]=each_cell/co
                #kai tautoxrona edge
                main_graph.add_edge(names_table_unique[xx], ent_names[ii],weight=each_cell/co)
            else:
                mean_sent_table[xx][ii]=0                
                #se afth th periptwsh den exoume kai edge
                # SHMANTIKO: AN THEOROUME OTI PROKALEI PROBLHMA H APOUSIA AKMHS NA SKEFTW 
                # NA THN ANTIKATASTHSW ME MIA OYDETERH TIMH PX TO ΤHRESH STO Vader
                #main_graph.add_edge(names_table_unique[xx], ent_names[ii],weight=0.05)
    return main_graph


def my_weight(G,a,b):
#H SYNARTHSH POU THA YPOLOGIZEI TO CUSTOM WEIGHT POU THELOUME GIA TO PROJECTION
#pairnoume duo node kai tous sygkrinoume me kapoio tropo
    ww=0 
    cc=0
    for nbr in set(G[a]) & set(G[b]):
        cc+=1        
        x=G[a][nbr]['weight']
        y=G[b][nbr]['weight']
        sub=correction_factor*abs(x-y)
        if sub >3:sub=3
        ww += 1-sub        
    return (ww/cc)*correction_factor2





   
def run_other_cd_methods(in_graph):
    #enallaktikoi tropoi communty detection από το networkx    
    #asynchronous label propagation
    CD1=asyn_lpa_communities(in_graph,'weight')
    for an_item in CD1:
        print(an_item)
        
    #asynchronous fluid de prepei na einai kai toso kalo alla etsi to balame
    CD2=asyn_fluidc(in_graph,4)
    for an_item in CD2:
        print(an_item)
    
    #kernighan lin bisection   
    CD3=kernighan_lin_bisection(PP,weight='weight')
    print(CD3)


#girvan_newman
#ypologismos pio centar edge kai bash weight
def most_central_edge(G):
    centrality = edge_betweenness_centrality(G, weight='weight')
    return max(centrality, key=centrality.get)

def run_girvan_newman(in_graph,repetitions=9):
    CD4=girvan_newman(in_graph,most_valuable_edge=most_central_edge)
    k=repetitions #arithmos epanalhpsewn
    rep=0 #twrinh epanalhpsh
    comm=[]
    for communities in itertools.islice(CD4, k):
        rep+=1
        comm.append(communities)
    return comm




def set_positions_and_colors(in_graph,in_comm):
    #initialize theseis kombwn se kyklo kai community opou anikoun
    w=0
    for nd in in_graph.nodes():
        #thesh
        in_graph.add_node(nd,pos=[100*np.cos(360*w/12), 120*np.sin(360*w/12)])
        w+=1
        #xrwma
        for ii,cc in enumerate(in_comm):
            if nd in cc:
                #xrwmatizoume analoga me thn omada
                in_graph.add_node(nd,color=ii) 
                 
#synatarthsh ektypwshs se .txt
def print_communities_to_text(in_comm1,in_comm2):
    #EDW EXPORT TWN SYNOLIKWN APOTELESMATWN SE ENA .txt ARXEIO
    #Prepei na akolouthei meta tis Girvan-newman alliws de tha leitourgei swsta
    try:
        data_file_out =open('networkx_communities_results.txt','w')
    except IOError:
        print("A error occured opening export File")
    else:
        data_file_out.write("Αρχείο με τa communities που παράγει ο αλγόριθμος Girvan-Newman και για τα δυο projection\n")
        data_file_out.write("Φαίνεται η εξέλιξη για διδοχικές εκτελέσεις\n\n")
        
        data_file_out.write("Πολιτικοί αρχηγοί- Κόμματα:\n")       
        for ii,each_result in enumerate(in_comm1):
            data_file_out.write("\nΕκτέλεση - "+str(ii+1)+":\n")
            for each_element in each_result:
                data_file_out.write(str(each_element)+'\n')
       
        data_file_out.write("\n\nΕιδησεογραφικές Πηγές:\n")       
        for ii,each_result in enumerate(in_comm2):
            data_file_out.write("\nΕκτέλεση - "+str(ii+1)+":\n")
            for each_element in each_result:
                data_file_out.write(str(each_element)+'\n')
       
        data_file_out.close()  

#PLOTLY VISUALIZATION

def render_proj_graph(in_graph,graph_file_name):
    #komboi
    node_trace = Scatter(
        x=[],
        y=[],
        mode='markers',
        name="Κόμβοι",
        text=[],
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            color=[],
            colorscale='Rainbow',
            size=30,
            colorbar=dict(
                thickness=20,
                title='Ομάδοποίηση',
                xanchor='right',
                titleside='right'
            ),
            line=dict(width=1,color='grey')
            )
        )
    
    #theseis kombwn (ara kai akmwn) epishs katalhla xrwmata
    for nd in in_graph.nodes():
        x, y = in_graph.node[nd]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace['text'].append(nd+' ομάδα: '+str(in_graph.node[nd]['color']+1))
        node_trace['marker']['color'].append(in_graph.node[nd]['color'])
    
    #akmes 
    edge_trace=Scatter(
        x=[],
        y=[],
        text='hey',
        hoverinfo='none',
        mode='lines',
        line=Line(width=0.6,color='black'),
        name="Ακμές",
    )
    
    #swsth thesh grammwn se syndesh me tous combous
    for edge in in_graph.edges():
        x0, y0 = in_graph.node[edge[0]]['pos']
        x1, y1 = in_graph.node[edge[1]]['pos']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]
    
    tadata=[edge_trace,node_trace]
    
    
    tolayout=dict(
        title = 'Projection των πολιτικών οντοτήτων',
        showlegend=True,
        hovermode='closest',
        margin=dict(b=20,l=10,r=10,t=40),
        xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)
    )
    sxedio=dict(data=tadata,layout=tolayout)
    offline.plot(sxedio,filename=graph_file_name+'.html')

#EKTELESH
'''
MG=make_main_graph()

#Gia to projection twn politkwn ontothtwn
correction_factor=11
correction_factor2=1.25

PP=generic_weighted_projected_graph(MG,ent_names,weight_function=my_weight)

pp_comm=run_girvan_newman(PP,repetitions=10)
set_positions_and_colors(PP,pp_comm[4])
render_proj_graph(PP,'politics_entities_connections')
 


#Gia to projection twn eihseografikwn phgwn
correction_factor=8
correction_factor2=1

NP=generic_weighted_projected_graph(MG,names_table_unique,weight_function=my_weight)

np_comm=run_girvan_newman(NP,repetitions=15)
set_positions_and_colors(NP,np_comm[8])
render_proj_graph(NP,'news_sources_connections')

#Ektypwsh se txt
print_communities_to_text(pp_comm,np_comm)
'''
