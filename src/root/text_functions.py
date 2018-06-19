'''
Created on 18 Ιουν 2018

@author: Solegem
'''
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def clean_from_xml_tags(sentence_in):
    sentence_out=''
    for each_letter in sentence_in:
        if each_letter == '<':
            do_record=False
        elif each_letter=='>':
            do_record=True
        #de pairnoume tis allages seiras pou den einai entos twn sthlwn 
        if do_record and each_letter != '>' and each_letter!='\n':
            sentence_out+=each_letter
    
    return sentence_out

def translate (text_input):
    #http request sto api
    translation_data={'key':'trnsl.1.1.20180607T210429Z.881c34eb686cb7b5.0619e4f57725199609597265365c2f0777f40cb5',
        'text':text_input,
        'lang':'el-en'
    }
    req=requests.post('https://translate.yandex.net/api/v1.5/tr.json/translate',data=translation_data)
    translated_text=req.json()['text'][0]
    return translated_text

def get_sentiment_of(sentence_in):
    sia =SentimentIntensityAnalyzer()
    scrs=sia.polarity_scores(sentence_in)
    the_important_one=scrs['compound']
    return the_important_one

phrase_ex="You don't need to comment on the scumbag that destroyed Greece. To rejoice the accomplice of the politician, the descendant, Kyriakos Mitsotakis."
