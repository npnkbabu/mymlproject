'''
Data picker : This class extracts data from database and returns collection of articles
This extraction can be done in 2 ways.
offline extract : get a bulk collection of articles data
online extract : return an event for news article. so that it can be subscribed to extract news data
'''

import os
import math
from datetime import datetime, timedelta
from TopicExtractor.src.utils.database import NewsDatabase
from TopicExtractor.src.utils.newspipeline import NewsPipeline
from TopicExtractor.src.utils.pipelineconfig import PipelineConfig

class DataExtractor(NewsPipeline):
    
    def __init__(self):
        print('DataExtractor instantiated')
        
    def _process(self):
        self.__config = PipelineConfig.getPipelineConfig(self)
        print('extracting articles data from database')
        return NewsDatabase.getArticlesData()
    
    def fit(self,x,y=None):
        print('DataExtractor.fit')
        return self

    def transform(self,x):
        print('DataExtractor.transform')
        return self._process()