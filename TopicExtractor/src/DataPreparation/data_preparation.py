'''
Here we trim features data like rounding tfidf value
'''
import numpy as np
import pandas as pd

from utils.processor import Processor

class DataPreparation(Processor):

    def __init__(self,config):
        print('DataPreparation instantiated')
        self.__config = config

    def process(self,features):
        # id2word, corpus, model = features[0], features[1], features[2]
        # print('rounding tfidf value')
        # corpus_tfidf = model[corpus]
        # print('generated')
        return True

    def fit(self,x,y=None):
        return self

    def transform(self,x):
        return self
