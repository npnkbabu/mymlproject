'''
Here we trim features data like set min cutoff for tfidf to consider
'''
import numpy as np
import pandas as pd
import re
from utils.newspipeline import NewsPipeline
from TopicExtractor.src.utils.metadatastore import *
from TopicExtractor.src.utils.pipelineconfig import PipelineConfig
from nltk import word_tokenize

class DataValidation(NewsPipeline):

    def __init__(self):
        print('DataValidation instantiated')
        self.__minWordLen = 3
        super().__init__()

    @mlflowtimed
    def _process(self,data):
        try:
            self.__config = PipelineConfig.getPipelineConfig(self)
            data['content'] = data['content'].map(self.__trimContent)

            self._addMLflowParam('MinWordLength',self.__minWordLen)
            self._storeMLflowData()
            return data
        except Exception as ex:
            print(ex)

    def fit(self,x,y=None):
        print('DataValidation.fit')
        return self

    def transform(self,x):
        print('DataValidation.transform')
        return self._process(x)
    
    def __trimContent(self,line):
        try:
            if line is not None:
                line = re.sub(r'[0-9!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]','',line)
                line = line.strip()
                tokens = word_tokenize(line)
                tokens = [x for x in tokens  if len(x)>self.__minWordLen]
                return ' '.join(tokens)
        except Exception as ex:
            print(ex)

