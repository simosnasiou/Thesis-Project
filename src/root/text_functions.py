'''
Created on 18 Ιουν 2018

@author: Solegem
'''
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#mallon na ftiaxnoume mia fora antikeimeno mono
sia =SentimentIntensityAnalyzer()

def text_filter(text_in):
    #AYTH H SYNARTHSH THA XRHSIMEYEI STHN DIAMORFOSH TOY KEIMENOYN PRIN TON TPOLOGISMO TOY SENTIMENT
    #WSTE NA GINETAI SOSTOTERA
    text_in=text_in.replace(' SW ','ND')
    text_in=text_in.replace(' SOUTHWEST ','ND')
    text_in=text_in.replace(' southwest ','ND')#an kai panta me kefalaio opws sth prohgoumeh grammh einai
    text_in=text_in.replace('jefferson starship','Mitsotakis') 
    text_in=text_in.replace('COMMUNIST party','ΚΚΕ')
    text_in=text_in.replace('COMMUNIST PARTY','ΚΚΕ')
    text_in=text_in.replace(' party ',' political faction ')
    text_in=text_in.replace(' parties ',' political factions ')
    text_in=text_in.replace(' HA ',' Golden Dawn ')
    text_in=text_in.replace('"',' ')#mallon de bohthaei idiaitera
    return text_in
    
def clean_xml_tags(sentence_in):
    sentence_out=''
    do_record=True
    for each_letter in sentence_in:
        if each_letter == '<':
            do_record=False
        elif each_letter=='>':
            do_record=True
        #de pairnoume tis allages seiras pou den einai entos twn sthlwn 
        if do_record and each_letter != '>' and each_letter!='\n' and each_letter!='\'':
            sentence_out+=each_letter    
    return sentence_out

def translate (text_input="none"):
    #http request sto api
    translation_data={'key':'trnsl.1.1.20180607T210429Z.881c34eb686cb7b5.0619e4f57725199609597265365c2f0777f40cb5',
        'text':text_input,
        'lang':'el-en'
    }
    # periorismoi megethous kai kenou pediou   
    if text_input != "none" and len(text_input)< 5000:
        req=requests.post('https://translate.yandex.net/api/v1.5/tr.json/translate',data=translation_data)
        translated_text=req.json()['text'][0]
    else :
        #spapina periptwsh opou exoume adeio pedio
        translated_text="none"
        print("empty or too large field detected")
    return translated_text

def get_sentiment_of(sentence_in):
    try:
        scrs=sia.polarity_scores(sentence_in)
        the_important_one=scrs['compound']
    except:
        the_important_one=0
    return the_important_one

#ayta edw einai proxeira gia na doume ti paizei kai me to body
#an symperilaboume telika to body tha mpei kai kana extra filtro stis parapanw synsrthseis (px gia megala ----)
a=(""" <a target="_blank" rel="noreferrer" href="http://www.defence-point.gr/news/wp-content/uploads/2018/05/To-Jason-Antigoni.jpg"><img alt= src="http://www.defence-point.gr/news/wp-content/uploads/2018/05/To-Jason-Antigoni.jpg" /></a><blockquote>Πού ακούστηκε ευρωπαϊκή συντηρητική παράταξη να ευλογεί διά της πλαγίας σύμφωνα συμβίωσης μουστακαλήδων και αναδοχή παιδιών από Κοντσίτες;</blockquote>Σήμερα, λοιπόν, έχω να καταθέσω κάποιες απορίες. Πρώτον και καλύτερον, δεν ξέρω τι και γιατί ψηφίζουν οι 155.000 «εγγεγραμμένοι» της Ν.Δ.... Το μόνο βέβαιο είναι ότι μετά και τον διασυρμό της περασμένης Τετάρτης, θα έπρεπε να το σκεφτούν δύο φορές.<br />Ελάχιστη σημασία έχει, μια και μιλούμε για το 2,5% του εκλογικού σώματος, μπορεί να σκεφτείτε. Ορθό, αλλά υπό μία έννοια αυτή η πληθυσμιακή υποκατηγορία αποτελεί τον στενό κομματικό πυρήνα της σημερινής Ν.Δ. Με 26.000 νέα μέλη, μάλιστα, που προσήλθαν να καταθέσουν τον οβολό τους βλέποντας προφανώς κάτι άλλο, που δυσκολευόμαστε να δούμε εμείς εδώ, στη «δημοκρατία»...<br />Και ωραία όλα αυτά, αλλά ιδού μια δεύτερη απορία: Εχουν καταλάβει όλοι αυτοί σε ποιον Θεό πιστεύει ο αρχηγός τους; Τι είναι, στα αλήθεια, ακριβώς η σημερινή Ν.Δ., που διαρκώς κλείνει το μάτι στη ΛΟΑΤΚΙ κοινότητα και άλλους περιθωριακούς του κοινωνικού φάσματος, περιφρονώντας τη βούληση μιας συντριπτικής πλειονότητας των έως σήμερα ψηφοφόρων της; Πού ακούστηκε ευρωπαϊκή συντηρητική παράταξη να ευλογεί διά της πλαγίας σύμφωνα συμβίωσης μουστακαλήδων και αναδοχή παιδιών από Κοντσίτες; Πού ακούστηκε δεξιά αντιπολίτευση που σέβεται τον εαυτό της να μην έχει αναδείξει σε μείζον ζήτημα δημόσιας αντιπαράθεσης τη σκόπιμη διάβρωση πατροπαράδοτων οικογενειακών δομών που προωθούν ενσυνείδητα αριστεροί εθνομηδενιστές; Και, τέλος, πού ακούστηκε να διαγράφεται βουλευτής, επειδή τόλμησε απλώς να εκφράσει την άποψή της σε ζητήματα νομοσχεδίου για την εθνική άμυνα και να καταψηφίζει την (υποτιθέμενη, έστω) κομματική γραμμή η... εισηγήτρια νομοσχεδίου, προερχόμενη από μετεγγραφή από άλλον πολιτικό χώρο χωρίς να υφίσταται την παραμικρή συνέπεια;<br />Είναι εικόνα δεξιάς κοινοβουλευτικής παράταξης σε προθάλαμο εξουσίας αυτή; Οχι, αγαπητοί. Εικόνα καρνάβαλου είναι. Του κλουβιού με τις τρελές...<br />Εχω, όμως, και ακόμη μία απορία: Αυτός ο «γκαλοπατζής» με το... σπινθηροβόλο βλέμμα, που μας νανούριζε κάποτε με τις αφόρητες κοινοτοπίες του στον Πρετεντέρη και σήμερα συστήνεται ως σύμβουλος «παρά τω προέδρω», μετράει τίποτα ή τα βγάζει από την κοιλιά του; Μήπως να ρωτήσει κανέναν συνάδελφό του; Δεν έχει δει ότι η αναδοχή από ομόφυλα ζευγάρια βρίσκει αντίθετη την ελληνική κοινωνία σε ποσοστό που γράφει «7» μπροστά; Και δεν έχει δει ότι το «70» γίνεται «90» στους μέχρι σήμερα ψηφοφόρους της Νέας Δημοκρατίας; Ή μήπως θεωρεί ότι ήρθε η ώρα να αλλάξουμε εκλογική βάση; Και να παίξουμε μπαλίτσα στον προνομιακό χώρο του ΣΥΡΙΖΑ και της Πασοκάρας;<br />Δυστυχώς, κάτι τέτοια καταλαβαίνω ότι έχουν μεταλαμπαδευτεί στο μυαλό του κακομοίρη του Κυριάκου. Γιατί αλλιώς δεν εξηγείται ότι κάθισε και είδε τον σύγχρονο ολετήρα της χώρας, τον Γιωργάκη Παπανδρέου, μία ημέρα αφότου τον κάλεσε στο Μαξίμου ο Τσίπρας! Για να τον ενημερώσει (άκουσον άκουσον) επί εθνικών θεμάτων. Ποιος; Ο τουρίστας των δύο ακτών του Βοσπόρου, που χόρευε χασαποσέρβικο στην επέτειο του Καστελόριζου!<br />Και ο μεν Τσίπρας τη δουλειά του κάνει, χωρίς αμφιβολία. Πλάκα, δηλαδή, στους τελειωμένους της Πασοκάρας με ένα μακιαβελικό «διαίρει και βασίλευε». Ο Κυριάκος τι ακριβώς κάνει υφιστάμενος τον εξευτελισμό από την «ενημέρωση» του Τζέφρυ; Διδάσκει πολιτικό πολιτισμό στη δεξιά παράταξη; Γιατί μπορεί να ακούσουμε και κάτι τέτοιο...<br />Να με συγχωρείτε, αλλά τέτοιου είδους άγαρμπη πολιτική και ιδεολογική μετάλλαξη σε ιστορικό κόμμα εξουσίας δεν έχω ξαναδεί. Αυτές οι στροφές (στην περίπτωσή μας περί στραβοτιμονιάς πρόκειται...) γίνονται μόνο από υπερχαρισματικές προσωπικότητες με υψηλή δημοφιλία και μέσα από διαδικασίες-ορόσημα, όπως τα συνέδρια επανίδρυσης. Οχι από... Θεοδωρικάκους. Και στα μουλωχτά...<br />Καλοτάξιδη, λοιπόν, η σημερινή ψήφος σε όσους αποφασίσουν να τη δώσουν, αλλά ξεχάστε τη Νέα Δημοκρατία που ξέρατε. Εδώ μιλάμε για κάτι άλλο. Ενα υβριδικό, μεταλλαγμένο πολιτικό σχήμα, σε πλήρη ιδεολογική σύγχυση, νεοφιλελεύθερο στην οικονομία, «προοδευτικούλι» στα κοινωνικά, «χαλαρούλι» στα θέματα λαθρομετανάστευσης και έννομης τάξης (που έπρεπε να είναι πρώτα στην ατζέντα του), αδιάφορο επιεικώς για τη διατήρηση παράδοσης και θρησκείας, και ασφαλώς... ευρωγερμανικό.Μα γίνονται όλα αυτά μαζί σε ένα; Και με ταμπέλα «κεντροδεξιός»; Ολα γίνονται, αγαπητοί μου, σε τούτο τον ντουνιά. Δείτε το Jason-Αντιγόνη. Σε λίγο η Νέα Δημοκρατία θα αποτελεί την κομματική εκδοχή του... """)
a=clean_x-ml_tags(a)
print(a)
a=translate(a)
a=text_filter(a)
b=get_sentiment_of(a)
print(a)
print(b)
