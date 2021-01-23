'''
Here we trim features data like set min cutoff for tfidf to consider
'''
import numpy as np
import pandas as pd

from utils.newspipeline import NewsPipeline
from TopicExtractor.src.utils.pipelineconfig import PipelineConfig

class DataValidation(NewsPipeline):

    def __init__(self):
        print('DataValidation instantiated')

    def _process(self,data):
        self.__config = PipelineConfig.getPipelineConfig(self)
        return True

    def fit(self,x,y=None):
        print('DataValidation.fit')
        return self

    def transform(self,x):
        print('DataValidation.transform')
        return x