'''
Similar to data we do validate the model in production pipeline with new data and check if its performance is as per 
        buisness expectation and better than previous model and compatible with prediciton service etc.
'''
import pandas as pd
import numpy as np


from utils.newspipeline import NewsPipeline

class ModelValidation(NewsPipeline):
    
    def __init__(self,config):
        print('ModelValidation instantiated')
        self.__config = config
    
    def _process(self,model):
        print('ModelValidation done')
        return model

    def fit(self,x,y=None):
        print('ModelValidation.fit')
        return self
    def transform(self,x):
        print('ModelValidation.transform')
        return self
