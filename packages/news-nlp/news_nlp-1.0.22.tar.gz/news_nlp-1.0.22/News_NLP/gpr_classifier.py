import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from News_NLP.clf_sa import Preprocessing_Clf_SA
import warnings
warnings.filterwarnings('ignore')

import sys
import gdown
import os

# get python system path
path = sys.path
site_package_path = "".join([p for p in path if 'site-packages' in p])
# download pretrained classifier
url = 'https://drive.google.com/file/d/1CL5TeHvZm65BzHoV_ePJme_sjyh-iY99/view?usp=share_link'
model_path= site_package_path+'/news_unified_model_V3.pkl'

# if model does not exist, download
if os.path.isfile(model_path) == False:
    gdown.download(url, output=model_path,quiet=True,fuzzy=True)
else:
    pass

Pkl_Filename = model_path
with open(Pkl_Filename, 'rb') as file:  
        Pickled_MLP_Model = pickle.load(file)

# if training dataset does not exist, download it
url2 = 'https://drive.google.com/file/d/1oAxSyq1T9ZEpaoeBzzfzsXelYph-7IX6/view?usp=share_link'
training_data_path =site_package_path+'/topics_for_classifier_V2.csv'

if os.path.isfile(training_data_path)==False:
    gdown.download(url2, output=training_data_path,quiet=True,fuzzy=True)
else:
    pass

def GPR_Clf(data):

    data_train = pd.read_csv(training_data_path,index_col=0)
    data_train.reset_index(drop=True, inplace=True)
    data_train['TDC'] = data_train['title_description_content'].apply(lambda x: Preprocessing_Clf_SA(x))

    df_train, df_test = train_test_split(data_train, test_size = 0.2,random_state = 42)

    X_train, y_train = df_train['TDC'], df_train['target']
    X_test, y_test = df_test['TDC'], df_test['target']

    Max_Features=5400

    # create the transformation matrix
    vectorizer = TfidfVectorizer(max_features=Max_Features)
    # tokenize and build vocabularies
    vectorizer_idf= vectorizer.fit(df_train['TDC'])
    # vectorizer.vocabulary_
    # vectorizer.idf_
    X_train  = vectorizer_idf.transform(df_train['TDC']).toarray()

    if type(data)== pd.core.frame.DataFrame:
        news_array  = vectorizer_idf.transform(data['TDC_Clf_SA']).toarray()
        df_pred = pd.DataFrame(Pickled_MLP_Model.predict(news_array),columns=['pred_class'])
        clf_news= pd.concat([data, df_pred],axis=1)
        GPR_News = clf_news.query('pred_class != 0')

        return GPR_News
    
    elif type(data) ==str:
        news_array  = vectorizer_idf.transform([data]).toarray()     
        df_pred = pd.DataFrame(Pickled_MLP_Model.predict(news_array),columns=['pred_class'])
        pred_class = df_pred.pred_class

        return pred_class[0]
    else:
         print('Input must be neither string of dataframe')

