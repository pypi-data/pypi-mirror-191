import numpy as np
import pandas as pd
from cliff.api import Cliff
my_cliff = Cliff('http://0.0.0.0:8080')

from tqdm.notebook import tqdm
tqdm.pandas()

def Location_Type(x:str):

    """
    input: FeatureCode
    output: LocationTypeId
    """

    # political entity, e.g.  UK, US
    if 'PCL' in x:
        return 3 # 'country'
    # state, region, administrative division, e.g. a state of US
    elif 'ADM' in x:
        return 2 #'state'
    # city, town, village
    elif 'PPL' in x:
        return 1 # 'city'
    else:
        return x
    

def CSC_Prob(text:str):
    
    """"
    input: TDC_Geo, which is cleaned news for geolocator
    output: a dataframe contains geocoded details
    """""
    
    # constant probability
    p1, p2, p3, p4, p5 = 0.7325, 0.1581, 0.0458, 0.0103, 0.0037
    px = 1-(p1+p2+p3+p4+p5)

    df_mentions = pd.DataFrame()

    col_order = ['id','name','countryCode','featureCode', 'featureClass',  'countryGeoNameId','stateCode',
                'stateGeoNameId','population','lon', 'lat']

    none_columns=['LocationId', 'LocationName', 'CountryCode', 'FeatureCode','FeatureClass', 'CountryGeoNameId',
                 'StateCode', 'StateGeoNameId','Population', 'Longitude', 'Latitude', 'LocatioTypeId', 'Frequency','Probability']

    country_none = pd.DataFrame(index=[0])
    for i in none_columns:
            country_none[i] = None
    # check empty text
    if not bool(text.strip()):
        return country_none

    else:

        pasered_geo = my_cliff.parse_text(text)
        mentions= pasered_geo['results']['places']['mentions']

        n_mentions = len(mentions)

        if n_mentions == 0:
            return country_none
            
        elif n_mentions == 1 and not mentions[0]['countryCode']:
            return country_none
            
        else:        
            for i in range(n_mentions):
                df_mention = pd.DataFrame.from_dict(mentions[i],orient='index').T
                df_mentions = pd.concat([df_mentions, df_mention],ignore_index=True)   
                        
            df_mentions = df_mentions[col_order]  
            # map featureCode to locationid
            df_mentions['LocationTypeId'] = df_mentions['featureCode'].apply(lambda x : Location_Type(x))
            # rename columns to in line with table NewsArticleLocations in Acarmar
            df_mentions.rename(columns = {'id':'LocationId',
                                            'name':'LocationName',
                                            'lon':'Longitude',
                                            'lat':'Latitude',
                                            'countryCode':'CountryCode',
                                            'featureCode':'FeatureCode',
                                            'featureClass':'FeatureClass', 
                                            'countryGeoNameId':'CountryGeoNameId',
                                            'stateCode':'StateCode',
                                            'stateGeoNameId':'StateGeoNameId',
                                            'population':'Population',
                                            },inplace=True)

            df_mentions_unique = df_mentions.drop_duplicates('LocationId',keep='first')
            df_mentions_unique.reset_index(drop=True, inplace=True)
            
            # df_mentions_unique_copy = df_mentions_unique.copy()

            if len(df_mentions) == 0:
                return country_none
                
            elif len(df_mentions) == 1 and not df_mentions.CountryCode[0]:
                return country_none

            else:
                # calculate LocationId frequency
                dfx = pd.DataFrame(df_mentions.groupby(['CountryCode'])['LocationId'].count()).reset_index()
                dfx = dfx.rename(columns={'LocationId':'Frequency'})
                dfx.replace('', np.nan, inplace=True)
                dfx.dropna(inplace=True)
                dfx.sort_values(by=['Frequency'],ascending=False,inplace=True)
                dfx.reset_index(drop=True, inplace=True)

                # country code freq
                freq_list = list(dfx.CountryCode.values)
                freq_value = list(dfx.Frequency.values)

                n_df_mentions = len(dfx)
                # assign probability 
                if n_df_mentions == 0:
                    return country_none
                    
                elif n_df_mentions == 1: 
                    df_prob = pd.DataFrame([p1],columns=['Probability'])

                elif n_df_mentions == 2:
                    df_prob = pd.DataFrame([p1,p2],columns=['Probability'])
                elif n_df_mentions == 3:
                    df_prob = pd.DataFrame([p1,p2,p3],columns=['Probability'])
                elif n_df_mentions == 4:
                    df_prob = pd.DataFrame([p1,p2,p3,p4],columns=['Probability'])
                elif n_df_mentions == 5:
                    df_prob = pd.DataFrame([p1,p2,p3,p4,p5],columns=['Probability'])
                else:
                    prob_list = [p1,p2,p3,p4,p5]
                    for i in range(n_df_mentions-5):
                        prob_list.append(px)
                        df_prob = pd.DataFrame(prob_list,columns=['Probability'])
                
                df_freq_prob = pd.concat([dfx, df_prob],axis=1)
                # concat unique df_mentions and probability_freq dataframe
                geo_details = pd.merge(df_mentions_unique, df_freq_prob, on='CountryCode',how='outer')
                geo_details.sort_values(by=['Frequency'],ascending=False,inplace=True)
                geo_details.reset_index(drop=True,inplace=True)
    
                return geo_details
            

def Get_CSC_Prob(dataset):
    
    """ To calculate the geo info of multiple news articles and store in a big dataframe"""
    
    
    CSCs = pd.DataFrame()
    for i in tqdm(dataset.index):
        csc_prob = CSC_Prob(dataset.TDC_Geo[i])
        csc_prob['news_id'] = dataset.news_id[i]                    
        CSCs = pd.concat([CSCs, csc_prob],ignore_index=True)
        
    return CSCs