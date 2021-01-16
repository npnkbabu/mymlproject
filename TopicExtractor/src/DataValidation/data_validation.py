'''
Here we trim features data like set min cutoff for tfidf to consider
'''
import numpy as np
import pandas as pd

from utils.processor import Processor

class DataValidation(Processor):

    def __init__(self,config=None):
        print('DataValidation instantiated')
        self.__config = config

    def process(self,data):
        return True

    def fit(self,x,y=None):
        return self

    def transform(self,x):
        return self