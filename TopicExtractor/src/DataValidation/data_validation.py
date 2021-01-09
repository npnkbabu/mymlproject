'''
Here we trim features data like set min cutoff for tfidf to consider
'''
import numpy as np
import pandas as pd

from utils.processor import Processor

class DataValidation(Processor):

    def __init__(self):
        print('DataValidation instantiated')

    def process(self,data):
        return True