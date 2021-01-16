'''
Data picker : This class extracts data from database and returns collection of articles
This extraction can be done in 2 ways.
offline extract : get a bulk collection of articles data
online extract : return an event for news article. so that it can be subscribed to extract news data
'''

import os
import math
from datetime import datetime, timedelta
from utils.database import NewsDatabase
from utils.processor import Processor

class DataExtractor(Processor):
    
    def __init__(self,config=None):
        print('DataExtractor instantiated')
        self.__config = config
    
    def process(self):
        print('extracting articles data from database')
        return NewsDatabase.getArticlesData()
    
    def fit(self,x,y=None):
        return self

    def transform(self,x):
        return self