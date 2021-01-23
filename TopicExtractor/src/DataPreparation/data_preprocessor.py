'''
DataPreProcessor : This class cleans the picked data from database
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
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
import sys
import os

class DataPreProcessor():
    
    def __init__(self,config):
        print('DataPreProcessor instantiated ')
        self.__config = config
    
    def process(self,data):
        try:
            print('Preprocessing articles data')
            self.df_articles = data
            self.df_articles['index'] = self.df_articles.index
            nullindex = self.df_articles[self.df_articles['content'].isnull()].index
            self.df_articles.drop(index=nullindex,inplace=True)
            self.__stop_words = set(stopwords.words('english'))
            self.__wordnetLemmatizer = WordNetLemmatizer()
            self.__stemmer = PorterStemmer()
            self.df_articles['processed_content'] = self.df_articles['content'].map(self.__preprocess)
            return self.df_articles
        except:
            print(sys.exc_info()[0])
        finally:
            print('Preprocessing completed')
        return False
        
    
    def __preprocess(self,line):
        result=[]
        tokens=[]
        line = re.sub(r'[0-9!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]','',line)
        line = line.strip()
        tokens = word_tokenize(line)
        tokens = [x for x in tokens if len(x)>2]
        tokens = list(map(lambda x : x.lower(),tokens))
        tokens = [x for x in tokens if x not in self.__stop_words]
        tokens = list(map(lambda x : self.__stemmer.stem(x),tokens))
        pos_tags = nltk.pos_tag(tokens)
        for token,postag in pos_tags:    
            pos = self.__getPosTagDef(postag)
            if pos != '':
                result.append(self.__wordnetLemmatizer.lemmatize(token,pos))
            else:
                result.append(self.__wordnetLemmatizer.lemmatize(token))
        return result

    def __getPosTagDef(self,postag):
        try:
            if postag.startswith('J'):
                return wordnet.ADJ
            if postag.startswith('V'):
                return wordnet.VERB
            if postag.startswith('N'):
                return wordnet.NOUN
            if postag.startswith('R'):
                return wordnet.ADV
            else:
                return ''
        except:
            print(sys.exc_info()[0])
