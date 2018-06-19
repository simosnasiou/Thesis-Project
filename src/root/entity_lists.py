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
ent1_1="title LIKE '%Τσίπρα%' OR title LIKE '%Τσιπρα%' OR title LIKE '%τσίπρα%' OR title LIKE '%τσιπρα%' OR title LIKE '%ΤΣΙΠΡΑ%' OR title LIKE '%ρωθυπουργ%' OR title LIKE '%ΡΩΘΥΠΟΥΡΓ%'"
ent1_2="title LIKE '%Σύριζα%' OR title LIKE '%ΣΥΡΙΖΑ%' OR title LIKE '%συριζα%' OR title LIKE '%σύριζα%' OR title LIKE '%ΣΥ.ΡΙ.ΖΑ%'"
#MITSOTAKIS - ND
ent2_1="title LIKE '%Μητσοτ_κη%' OR title LIKE '%ΜΗΤΣΟΤ_ΚΗ%' OR title LIKE '%μητσοτ_κη%'"
ent2_2="title LIKE '% ΝΔ %' OR title LIKE '% νδ %' OR title LIKE '%Ν_α Δημοκρατ_α%' OR title LIKE '%Ν_ας Δημοκρατ_α%' OR title LIKE '%ν_α δημοκρατ_α%' OR title LIKE '%ν_ας δημοκρατ_α%' OR title LIKE '%Ν_α Δημοκρατ_α%' OR title LIKE '%ΝΕΑ ΔΗΜΟΚΡΑΤΙΑ%' OR title LIKE '%ΝΕΑΣ ΔΗΜΟΚΡΑΤΙΑ%'"
#XRYSH AYGH
ent3_1="title LIKE '%Μιχαλολι_κο%' OR title LIKE '%ΜΙΧΑΛΟΛΙ_ΚΟ%'"
ent3_2="title LIKE '%Χρυσ_ Αυγ%' OR title LIKE '%χρυσ_ αυγ%' OR title LIKE '%ΧΡΥΣ_ ΑΥΓ%' OR title LIKE '% ΧΑ %'"
#KINHMA ALLAGHS
ent4_1="title LIKE '%Γεννηματ%' OR title LIKE '%γεννηματ%'"
ent4_2="title LIKE '%κ_νημα αλλαγ_%' OR title LIKE '%Κ_νημα Αλλαγ_%' OR title LIKE '%ΚΙΝΑΛ%' OR title LIKE '%ΚΙΝ.ΑΛ%'"
#KKE
ent5_1="title LIKE '%Κουτσο_μπα%' OR title LIKE '%ΚΟΥΤΣΟ_ΜΠΑ%' OR title LIKE '%γενικός γραμματέας του%'"
ent5_2="title LIKE '%ΚΚΕ%' OR title LIKE '%κκε%' OR title LIKE '%κομμουνιστικ_ κ_μμα%' OR title LIKE '%Κομμουνιστικ_ Κ_μμα%'"
#ENOSH KENTRWWN
ent6_1="title LIKE '%Λεβ_ντη%' OR title LIKE '%%ΛΕΒ_ΝΤΗ%'"
ent6_2="title LIKE '%νωση _εντρ_ων%' OR title LIKE '%νωσης _εντρ_ων%' OR title LIKE '%ΝΩΣΗ _ΕΝΤΡ_ΩΝ%'"

#synoliko gia katametrhsh
ent_total=ent1_1+" OR "+ent1_2+" OR "+ent2_1+" OR "+ent2_2+" OR "+ent3_1+" OR "+ent3_2+" OR "+ent4_1+" OR "+ent4_2+" OR "+ent5_1+" OR "+ent5_2+" OR "+ent6_1+" OR "+ent6_2
