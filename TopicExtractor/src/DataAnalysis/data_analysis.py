#its called from FeatureStore before generating features we get results from this analysis and decide features.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from gensim import corpora, models
from gensim.models import TfidfModel
import gensim
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
import sys
import os

from utils.newspipeline import NewsPipeline
from TopicExtractor.src.utils.pipelineconfig import PipelineConfig

class DataAnalysis(NewsPipeline):
    
    def __init__(self):
        print('DataAnalysis instantiated')

    def _process(self,df_articles):
        try:
            self.__config = PipelineConfig.getPipelineConfig(self)
            if self.__config['Enable']:
                print('EDA by giving word cloud')
                _wordcloud = WordCloud()
                tokens = []
                lst = [[tokens.append(y) for y in x] for x in df_articles['processed_content']]
                longstring = ','.join(tokens)
                _wordcloud.generate(longstring)
                plt.imshow(_wordcloud)
                plt.axis('off')
                plt.show()
            return df_articles
    
        except:
            print(sys.exc_info())
            return False
    
    def fit(self,x,y=None):
        print('DataAnalysis.fit')
        return self

    def transform(self,x):
        print('DataAnalysis.transform')
        return self._process(x)