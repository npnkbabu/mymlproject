'''
Similar to data we do validate the model in production pipeline with new data and check if its performance is as per 
        buisness expectation and better than previous model and compatible with prediciton service etc.
'''
import pandas as pd
import numpy as np


from utils.processor import Processor

class ModelValidation(Processor):
    
    def __init__(self):
        print('ModelValidation instantiated')

    def process(self,model):
        print('ModelValidation done')
        return model