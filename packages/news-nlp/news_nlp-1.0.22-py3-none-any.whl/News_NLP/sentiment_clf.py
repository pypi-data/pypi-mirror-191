# for sentiment analysis
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


def Sen_Clf(data):
    if type(data) == str:
        return sia.polarity_scores(data)['compound']
    else:
        data['Symantic'] =  data['TDC_Clf_SA'].progress_apply(lambda x : sia.polarity_scores(x)['compound'])
        return data

