import spacy
import pandas as pd
import string
import re
# python -m spacy download en_core_web_lg
import en_core_web_lg
# nlp_lg = spacy.load('en_core_web_lg', disable=['parser', 'ner','tok2vec','tagger','attribute_ruler','senter'])
nlp_lg = spacy.load('en_core_web_lg',disable=['ner','parser','tok2vec','tagger','senter','lemmatizer','attribute_ruler'])
# nlp_lg = spacy.load('en_core_web_lg',disable=["parser", "ner"] )
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import nltk
nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from collections import defaultdict


def covert_nan(x):
    
    if pd.isna(x):
        return ""
    else:
        return str(x)
    
def Combine_Col(dataset, col_1, col_2):
    
    df_col_1_2 = pd.DataFrame(dataset[col_1]+ '. ' + dataset[col_2].map(covert_nan),columns=[col_1+'_'+col_2])
    new_dataset = pd.concat([df_col_1_2,dataset],axis=1)
    
    return new_dataset


def Preprocessing_GEO(text:str):
    
    """
    input: text in string
    output: cleaned text in string
    """
    # the max length of spacy input string is 100,0000
    text = text[:999999]
    # manuanlly identified non informative words
    non_informative_word =['copyright',"All rights reserved","Twitter at","Getty",\
        "Our Standards: The Thomson Reuters Trust Principles",\
        "Register now for FREE unlimited access to","- Reuters",] 
    
    for i in non_informative_word:
        text = text.replace("{i}".format(i=i)," ") 

    # punctuations to be kept    
    remained_punc = ['.',',','-']
    doc = nlp_lg(text)
    # lemmatization and select alphabetic tokens and keep . , -
    # text = " ".join([ l for l in  LEMMA(text) if (l in remained_punc or l.isalpha())])
    text = " ".join([i.text for i in doc if (i.text in remained_punc or i.text.isalpha())])
    # clean by replacing , . -
    text = text.replace('US', 'U.S.').replace(' ,',',').replace(' .',',').replace(' - ','-').replace(' -',' ').replace(' Reuters-','. ')
    
    return text



# for general use
def Preprocessing_Clf_SA(text:str):
    # split into tokens by white space
    lemmatizer = WordNetLemmatizer()

    # text = text[:999999]
    # manuanlly identified non informative words
    non_informative_word =['copyright',"All rights reserved","Twitter at","Getty",\
        "Our Standards: The Thomson Reuters Trust Principles",\
        "Register now for FREE unlimited access to"] 

    for i in non_informative_word:
        text = text.replace("{i}".format(i=i)," ") 

    tokens = text.split()
    # prepare regex for char filtering
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    # remove punctuation from each word
    tokens = [re_punc.sub('', w) for w in tokens]
    # remove remaining tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    # filter out short tokens
    tokens = [word for word in tokens if len(word) > 2]

    # lemma = [lemmatizer.lemmatize("{tok}".format(tok=tok),get_wordnet_pos(tok)) for tok in tokens ]
    lemma = [lemmatizer.lemmatize("{tok}".format(tok=tok)) for tok in tokens ]
    
    words = " ".join(lemma).lower()

    return words