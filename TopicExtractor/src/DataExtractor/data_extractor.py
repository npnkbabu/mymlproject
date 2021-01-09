'''
Data extractor : Get features data from db file paths
'''
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

from utils.processor import Processor
from utils.database import NewsDatabase

class DataExtractor(Processor):
    
    def __init__(self):
        print('DataExtractor instantiated')

    def process(self):
        print('Extracting features data in DataExtractor')
        filepaths = NewsDatabase.GetFeatures()
        id2word = gensim.corpora.Dictionary.load(filepaths[0])
        corpus = corpora.MmCorpus(filepaths[1])
        model = gensim.models.TfidfModel.load(filepaths[2])
        processeddata = pd.read_csv(filepaths[3])
        return [id2word,corpus,model,processeddata]


        





    
