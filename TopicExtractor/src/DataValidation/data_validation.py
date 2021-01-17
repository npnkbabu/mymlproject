'''
Here we trim features data like set min cutoff for tfidf to consider
'''
import numpy as np
import pandas as pd

from utils.newspipeline import NewsPipeline

class DataValidation(NewsPipeline):

    def __init__(self,config=None):
        print('DataValidation instantiated')
        self.__config = config

    def _process(self,data):
        return True

    def fit(self,x,y=None):
        print('DataValidation.fit')
        return self

    def transform(self,x):
        print('DataValidation.transform')
        return self