from time import time
from newsapi import NewsApiClient
from IPython.display import clear_output
import pandas as pd
# import string
# import random
import uuid
from tqdm.notebook import trange, tqdm
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


KEY_WORDS = ['conflict','protest']

newsparams = [KEY_WORDS,'2023-02-02','2022-02-03',10,'relevancy']

newsapi = NewsApiClient(api_key='498e28bd1e2e4b5596287d87f6f37500')

def Extract_Google_News(topics, 
                        date_from:str, 
                        date_to:str, 
                        n_page:int, 
                        sort_by:str,**kwargs):
    
    # sort_by belongs to 'relevancy', 'popularity', 'publishedAt'
    
#     date_rng = pd.date_range(date_from, date_to,freq='1D')
#     date_list = date_rng.strftime("%Y-%m-%d").tolist()
    
    df_all_articles = pd.DataFrame()

    if n_page <=99:
        if type(KEY_WORDS)==list: 
            for j in tqdm(topics):           
                    for i in range(1,n_page+1,1):
                        articles_page = newsapi.get_everything(
                                                                q=j,
                                                                from_param= date_from,
                                                                to= date_to,
                                                                page_size = 10,
                                                                language='en',
                                                                sort_by= sort_by,
                                                                page=i)

                        #clear_output(wait=True)
                        print("Retrieved news topic '{topic}', page {page} ".format(topic=j,page=i))
                        df_articles_page = pd.DataFrame(articles_page['articles'])
                        df_articles_page['search_term'] = '{search_term}'.format(search_term = j) 

                        df_all_articles = df_all_articles.append(df_articles_page,ignore_index=True)

        elif type(KEY_WORDS)==str:

            for i in range(1,n_page+1,1):
                articles_page = newsapi.get_everything(q=KEY_WORDS,
                                                      from_param= date_from,
                                                      to= date_to,
                                                      page_size = 1,
                                                      language='en',
                                                      sort_by= sort_by,
                                                      page=i)

                print("Retrieved page {page}".format(page=i))

                df_articles_page = pd.DataFrame(articles_page['articles'])
                df_all_articles = df_all_articles.append(df_articles_page,ignore_index=True)

    else:
      print('ERROR: Max number of pages is 99.')
                
    return df_all_articles


def Transform_G_News(dataset):

    source_list = [list(eval(str(dataset.source[i])).values()) for i in range(len(dataset['source']))]

    source_df = pd.DataFrame(source_list,
                             columns=['source_id','source_name'],
                             index = dataset.index)

    dataset = pd.concat([source_df,dataset],axis=1)

    # drop duplicate title   
    n_duplicates = (len(dataset.title)-len(dataset.title.unique()))
    if n_duplicates > 0:        
        print('{n} duplicate news articles are dropped '.format(n=n_duplicates))
        print('-'*80)
    
    dataset = dataset.drop_duplicates(subset='title',keep='first')

    # drop empty news content
    # dataset = dataset.dropna(subset=['content'])
    # dataset = dataset.query('content==content')

    news_id = []
    for i in range(len(dataset)):    
        digit = uuid.uuid4().hex    
        # n = (ran_gen(16, "AEIOSUMA23"))   
        news_id.append(digit)

    df_news_id = pd.DataFrame(news_id, index = dataset.index, columns = ['news_id'])
    dataset = pd.concat([df_news_id,dataset],axis=1)

    dataset.set_index('news_id',inplace=True)


    if type(KEY_WORDS)==list:

      col_order = ['source_name', 'author', 'title', 'publishedAt',\
                    'search_term','url' ]  # 'source','urlToImage','source_id'

    elif type(KEY_WORDS)==str:

      col_order = ['source_name', 'author', 'title','publishedAt','url']

    dataset = dataset[col_order]
    
    return dataset

def GNews():

    start = time()
    df_News = Extract_Google_News(*newsparams)
    print('-'*80)
    print(f'Extracting News takes {time() - start:.2f} secs')  
    print('-'*80)
    
    start = time()
    df_News.to_excel('./original_news.xlsx')
    print(f'Saving Orginal News takes {time() - start:.2f} secs')  
    print('-'*80)
    
    start = time()
    df_News_transformed = Transform_G_News(dataset = df_News)
    print(f'Transforming News takes {time() - start:.2f} secs')  
    print('-'*80)

    start = time()
    df_News_transformed.to_excel('./transformed_news.xlsx')
    print(f'Saving Transformed News takes {time() - start:.2f} secs')  
    print('-'*80)
    
    return df_News_transformed

