
<!-- ![](/home/jason/Documents/data/newplot.png) -->
# News NLP for Global Geopolitical Risk
=======================================

This is a Python client for the news NLP.

Usage
-----
First install it

```
pip install news-nlp -U
```

Then instantiate and use it like this:

```python
import News_NLP
from News_NLP.GNews import GNews
from News_NLP.preprocessing import Preprocessing_Clf_SA, Preprocessing_GEO,Combine_Col
from News_NLP.gpr_classifier import GPR_Clf
from News_NLP.sentiment_clf import Sen_Clf
from News_NLP.geolocator import Get_CSC_Prob, CSC_Prob
```

* Fetch news articles from Google News API, `from News_NLP.GNews import GNews`
* Preproces news data for sentiment analysis and news type classifier
   `from News_NLP.preprocessing import Preprocessing_Clf_SA`
* Preproces news data for multiple-geolocator
  `from News_NLP.preprocessing import Preprocessing_GEO`
* Implement pretrained deep leanring model to caterise news article 
  `from News_NLP.gpr_classifier import GPR_Clf`
* Perform sentiment classifier `from News_NLP.sentiment_clf import Sen_Clf`
* Implement multiple geolocator `form News_NLP.geolocator import Get_CSC_Prob, CSC_Prob`,

# GitHub
For a demonstration in Jupyter notebook see https://github.com/HigherHoopern/News_NLP/NewsApp.ipynb

download sample news data
https://github.com/HigherHoopern/News_NLP/blob/main/data/SampleNews.csv