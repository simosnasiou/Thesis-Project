'''
Created on 18 Ιουν 2018

@author: Solegem
'''
'''
Edw briskontai diafores listes me entity pou xreiazontai gia ton yoloipo kwdika wste na mhn ton gemisoume 
Einai me ellhnikous xarakthres giati me ellhnikous xarakthres ginetai to arxiko search prin th metafrash
Se afth th fash aforoun apokelistika ta kommata kai tous arxigous tous
Exoun morfh LIKE ... OR LIKE... pou epitrepei ap eytheias xrhsh apo mySQL query
H xrisimothta tous exei elexthei me entoles SELECT COUNT(*)
'''
#TSIPRAS - SYRIZA
ent1_1="{0} LIKE '%Τσίπρα%' OR {0} LIKE '%Τσιπρα%' OR {0} LIKE '%τσίπρα%' OR {0} LIKE '%τσιπρα%' OR {0} LIKE '%ΤΣΙΠΡΑ%' OR {0} LIKE '%ρωθυπουργ%' OR {0} LIKE '%ΡΩΘΥΠΟΥΡΓ%'"
ent1_2="{0} LIKE '%Σύριζα%' OR {0} LIKE '%ΣΥΡΙΖΑ%' OR {0} LIKE '%συριζα%' OR {0} LIKE '%σύριζα%' OR {0} LIKE '%ΣΥ.ΡΙ.ΖΑ%'"
#MITSOTAKIS - ND
ent2_1="{0} LIKE '%Μητσοτ_κη%' OR {0} LIKE '%ΜΗΤΣΟΤ_ΚΗ%' OR {0} LIKE '%μητσοτ_κη%'"
ent2_2="{0} LIKE '% ΝΔ %' OR {0} LIKE '% νδ %' OR {0} LIKE '%Ν_α Δημοκρατ_α%' OR {0} LIKE '%Ν_ας Δημοκρατ_α%' OR {0} LIKE '%ν_α δημοκρατ_α%' OR {0} LIKE '%ν_ας δημοκρατ_α%' OR {0} LIKE '%Ν_α Δημοκρατ_α%' OR {0} LIKE '%ΝΕΑ ΔΗΜΟΚΡΑΤΙΑ%' OR {0} LIKE '%ΝΕΑΣ ΔΗΜΟΚΡΑΤΙΑ%'"
#XRYSH AYGH
ent3_1="{0} LIKE '%Μιχαλολι_κο%' OR {0} LIKE '%ΜΙΧΑΛΟΛΙ_ΚΟ%'"
ent3_2="{0} LIKE '%Χρυσ_ Αυγ%' OR {0} LIKE '%χρυσ_ αυγ%' OR {0} LIKE '%ΧΡΥΣ_ ΑΥΓ%' OR {0} LIKE '% ΧΑ %'"
#KINHMA ALLAGHS
ent4_1="{0} LIKE '%Γεννηματ%' OR {0} LIKE '%γεννηματ%'"
ent4_2="{0} LIKE '%κ_νημα αλλαγ_%' OR {0} LIKE '%Κ_νημα Αλλαγ_%' OR {0} LIKE '%ΚΙΝΑΛ%' OR {0} LIKE '%ΚΙΝ.ΑΛ%'"
#KKE
ent5_1="{0} LIKE '%Κουτσο_μπα%' OR {0} LIKE '%ΚΟΥΤΣΟ_ΜΠΑ%' OR {0} LIKE '%γενικός γραμματέας του%'"
ent5_2="{0} LIKE '%ΚΚΕ%' OR {0} LIKE '%κκε%' OR {0} LIKE '%κομμουνιστικ_ κ_μμα%' OR {0} LIKE '%Κομμουνιστικ_ Κ_μμα%'"
#ENOSH KENTRWWN
ent6_1="{0} LIKE '%Λεβ_ντη%' OR {0} LIKE '%%ΛΕΒ_ΝΤΗ%'"
ent6_2="{0} LIKE '%νωση _εντρ_ων%' OR {0} LIKE '%νωσης _εντρ_ων%' OR {0} LIKE '%ΝΩΣΗ _ΕΝΤΡ_ΩΝ%'"

ent_names=["Τσίπρας","Σύριζα","Μιτσοτάκης","Νέα Δημοκρατία","Μηχαλολιάκος","Χυσή Αυγή","Γεννηματά","Κίνημα Αλλαγής","Κουτσούμπας","ΚΚΕ","Λεβέντης","Ένωση Κεντρώων"]
#synoliko string gia katametrhsh
ent_total_temp=ent1_1+" OR "+ent1_2+" OR "+ent2_1+" OR "+ent2_2+" OR "+ent3_1+" OR "+ent3_2+" OR "+ent4_1+" OR "+ent4_2+" OR "+ent5_1+" OR "+ent5_2+" OR "+ent6_1+" OR "+ent6_2
ent_total=ent_total_temp.format('title')
#Ola ta epimerous se mia lista
ent_list_temp=[ent1_1,ent1_2,ent2_1,ent2_2,ent3_1,ent3_2,ent4_1,ent4_2,ent5_1,ent5_2,ent6_1,ent6_2]
ent_list=[aa.format('content_gr') for aa in ent_list_temp]
#ta onomata twn sthlwn boolean gia to an yparxei kathe entity sth bash
ent_collumn_names=['incl1_1','incl1_2','incl2_1','incl2_2','incl3_1','incl3_2','incl4_1','incl4_2','incl5_1','incl5_2','incl6_1','incl6_2']
#ta onomata twn sthlw gia ta athroistiko COUNT ana source kai enoia ston athroistiko pinaka
count_collumn_names=['g1_1_count','g1_2_count','g2_1_count','g2_2_count','g3_1_count','g3_2_count','g4_1_count','g4_2_count','g5_1_count','g5_2_count','g6_1_count','g6_2_count']
#ta onomata twn sthlw gia ta athroistiko SENTIMENT ana source kai enoia ston athroistiko pinaka
sent_collumn_names=['g1_1_sent','g1_2_sent','g2_1_sent','g2_2_sent','g3_1_sent','g3_2_sent','g4_1_sent','g4_2_sent','g5_1_sent','g5_2_sent','g6_1_sent','g6_2_sent']