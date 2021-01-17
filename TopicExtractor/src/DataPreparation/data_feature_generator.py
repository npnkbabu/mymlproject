#store features in database
# we get dictionary to store id, word 
# we get tfidf scores for reach document as (id,score) where we map id to dictionary to get word
# so each document or sentence is converted to word and its tfidf score. these are features we store in db

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
import shutil
import json
from datetime import datetime
from utils.newspipeline import NewsPipeline
from utils.database import NewsDatabase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATA_PATH = os.path.join(BASE_DIR,'data')

class DataFeatureGenerator(NewsPipeline):
    
    def __init__(self):
        print('DataFeatureGenerator instantiated')

    def process(self,df_articles):
        try:
            print('Generating features')
                     
            id2word = gensim.corpora.Dictionary(df_articles['processed_content'])
            count=0
            for key, val in id2word.iteritems():
                print(key,'-->', val)
                count +=1
                if count >= 10:
                    break
            print('show top 10 words by count')

            processeddata=df_articles['processed_content']
            corpus = [id2word.doc2bow(text) for text in processeddata]
            print('gensim bag of words (wordid : wordcount) \n',corpus[:10])
            model = gensim.models.TfidfModel(corpus,id2word)
            print('gensim Tfidf data (wordid : Tfidf value) \n')
            corpus_tfidf = model[corpus]
            for doc in corpus_tfidf[:10]:
                print(doc)
            return self.__storeFeatures(id2word,corpus,model,processeddata)
        except:
            print(sys.exc_info())
            return None
    
    def __storeFeatures(self,id2word,corpus,model,processeddata):
        print('storing features file paths into database')
        try:
            #saving features into files
            today = datetime.today().strftime('%Y-%m-%d')
            filepath = os.path.join(DATA_PATH, today)
            if os.path.exists(filepath):
                shutil.rmtree(filepath)
            os.mkdir(filepath)
            strid2wordfile = os.path.join(filepath,'id2word.dic')
            strcorpusfile =  os.path.join(filepath,'corpus.mm')
            strmodelfile = os.path.join(filepath,'tfidfmodel.model')
            processeddatafile = os.path.join(filepath,'processeddata.csv')

            id2word.save(strid2wordfile)
            corpora.MmCorpus.serialize(strcorpusfile,corpus)
            model.save(strmodelfile)
            processeddata.to_csv(processeddatafile)
            NewsDatabase.dumpFeatures([strid2wordfile,strcorpusfile,strmodelfile,processeddatafile])
            return True
        except:
            print(sys.exc_info())
            return False

