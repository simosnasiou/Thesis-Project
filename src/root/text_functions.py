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
