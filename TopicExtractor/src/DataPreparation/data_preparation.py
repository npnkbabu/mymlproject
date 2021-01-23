'''
Here we trim features data like rounding tfidf value
'''
import numpy as np
import pandas as pd

from utils.newspipeline import NewsPipeline
from DataPreparation.data_preprocessor import DataPreProcessor
from DataPreparation.data_feature_generator import DataFeatureGenerator
from TopicExtractor.src.utils.pipelineconfig import PipelineConfig

class DataPreparation(NewsPipeline):

    def __init__(self):
        print('DataPreparation instantiated')

    def _process(self,data):
        self.__config = PipelineConfig.getPipelineConfig(self)
        self.__dataFeatGen = DataFeatureGenerator(self.__config)
        self.__dataPreProc = DataPreProcessor(self.__config)
        # id2word, corpus, model = features[0], features[1], features[2]
        # print('rounding tfidf value')
        # corpus_tfidf = model[corpus]
        # print('generated')
        return self.__dataFeatGen.process(self.__dataPreProc.process(data))

    def fit(self,x,y=None):
        print('DataPreparation.fit')
        return self

    def transform(self,x):
        print('DataPreparation.transform')
        return self._process(x)
