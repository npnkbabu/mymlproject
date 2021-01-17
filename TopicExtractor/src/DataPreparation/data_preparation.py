'''
Here we trim features data like rounding tfidf value
'''
import numpy as np
import pandas as pd

from utils.newspipeline import NewsPipeline

class DataPreparation(NewsPipeline):

    def __init__(self,config):
        print('DataPreparation instantiated')
        self.__config = config

    def _process(self,features):
        # id2word, corpus, model = features[0], features[1], features[2]
        # print('rounding tfidf value')
        # corpus_tfidf = model[corpus]
        # print('generated')
        return True

    def fit(self,x,y=None):
        print('DataPreparation.fit')
        return self

    def transform(self,x):
        print('DataPreparation.transform')
        return self
