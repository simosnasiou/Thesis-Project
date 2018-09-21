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



#KATASKEYH TOY KYRIOU GRAPHIMATOS ME TIS SXESEIS MESWN - POLITIKWN ONTOTHTWN
#MONO NODES EDW - EDGES KATW TAYTOXRONA ME TON PINAKA
main_graph =nx.Graph()
#gia na mhn exoume duplicate -> prepei monadiko onoma node -> ara kolame kai ena id apo th DB
names_table_unique=[str(y)+' - '+x for x, y in zip(names_table, list(range(82,159)))]   
main_graph.add_nodes_from(names_table_unique,bipartite=0)
main_graph.add_nodes_from(ent_names,bipartite=1)

#ypolgismos toy pinaka me ta sentiment (epeidh den apothhkeyetai telika an kai xrhsimopoietai 
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
'''
doyleyei alla visualization kai ta loipa - kai vs weighted
'''
#H SYNARTHSH POU THA YPOLOGIZEI TO CUSTOM WEIGHT POU THELOUME GIA TO PROJECTION
#pairnoume doy node kai tous sygkrinoume me kapoio tropo
def my_weight(G,a,b):
    ww=0;    
    for nbr in set(G[a]) & set(G[b]):
        #edw theloume na baloume to baros ths akmhs anti gia 1
        #abs giati ta barh einai genikai kai arnhtika alla ayto de symainei mh omoiothta
        ww += abs(G[a][nbr]['weight'] + G[b][nbr]['weight'])
    return ww


PP=generic_weighted_projected_graph(main_graph,ent_names,weight_function=my_weight)


   
'''
#enallaktikoi tropoi communty detection από το network

#asynchronous label propagation
CC1=asyn_lpa_communities(PP,'weight')
for an_item in CC1:
    print(an_item)
    
#asynchronous fluid de prepei na einai kai toso kalo alla etsi to balame
CC2=asyn_fluidc(PP,4)
for an_item in CC2:
    print(an_item)

#kernighan lin bisection   
CC3=kernighan_lin_bisection(PP,weight='weight')
print(CC3)
'''

#girvan_newman
#ypologismos pio centar edge kai bash weight
def most_central_edge(G):
    centrality = edge_betweenness_centrality(G, weight='weight')
    return max(centrality, key=centrality.get)


CC4=girvan_newman(PP,most_valuable_edge=most_central_edge)
k=9 #arithmos epanalhpsewn
keep=5 #epanalhpsh pou theloume na kraththei
rep=0 #twrinh epanalhpsh
for communities in itertools.islice(CC4, k):
    rep+=1
    if rep==keep:
        communities_snapshot=communities
    print(tuple(c for c in communities))

#initialize theseis kombwn se kyklo kai community opou anikoun
w=0
for nd in PP.nodes():
    #thesh
    PP.add_node(nd,pos=[100*np.cos(360*w/12), 120*np.sin(360*w/12)])
    w+=1
    #xrwma
    for ii,cc in enumerate(communities_snapshot):
        if nd in cc:
            #xrwmatizoume analoga me thn omada
            PP.add_node(nd,color=ii)  
    
#PLOTLY VISUALIZATION

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
        #colorscale='Magendas',
        size=30,
        colorbar=dict(
            thickness=20,
            title='Άχρηστο τώρα',
            xanchor='right',
            titleside='right'
        ),
        line=dict(width=1,color='grey')
        )
    )

#theseis kombwn (ara kai akmwn)
for nd in PP.nodes():
    x, y = PP.node[nd]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)
    node_trace['text'].append(nd)
    node_trace['marker']['color'].append(np.random.randint(100))
print(node_trace['x'])
print(node_trace['y'])

#akmes 
edge_trace=Scatter(
    x=[],
    y=[],
    text='hey',
    hovertext='cool man',
    mode='lines',
    line=Line(width=0.7,color='black'),
    name="Ακμές",
)

#swsth thesh grammwn se syndesh me tous combous
for edge in PP.edges():
    x0, y0 = PP.node[edge[0]]['pos']
    x1, y1 = PP.node[edge[1]]['pos']
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
offline.plot(sxedio,filename='political_entities_connection.html')