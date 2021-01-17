'''
Data extractor : Get features data from db file paths
'''
from DataExtractor.data_collector import DataCollector
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

from utils.newspipeline import NewsPipeline
from utils.database import NewsDatabase

class DataFetcher(NewsPipeline):
    
    def __init__(self,DataCollectionconfig):
        print('DataFetcher instantiated')
        self._dataCollector = DataCollector(DataCollectionconfig)

    def process(self):
        #self._dataCollector.process()
        print('Extracting news data in DataFetcher')
        
        filepaths = NewsDatabase.GetFeatures()
        id2word = gensim.corpora.Dictionary.load(filepaths[0])
        corpus = corpora.MmCorpus(filepaths[1])
        model = gensim.models.TfidfModel.load(filepaths[2])
        processeddata = pd.read_csv(filepaths[3])
        return [id2word,corpus,model,processeddata]


        





    
