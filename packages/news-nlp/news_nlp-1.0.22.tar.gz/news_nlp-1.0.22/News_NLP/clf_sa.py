import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from collections import defaultdict
import re
import string



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