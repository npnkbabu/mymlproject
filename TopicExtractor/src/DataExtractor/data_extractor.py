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
from TopicExtractor.src.utils.mlflow.metadatastore import *
from TopicExtractor.src.utils.pipelineconfig import PipelineConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATA_PATH = os.path.join(BASE_DIR,'data')

class DataExtractor(NewsPipeline):
    
    def __init__(self):
        print('DataExtractor instantiated')
        self.__articlesDataFileName = 'Articles.csv'
        super().__init__()
        
        
    @mlflowtimed
    def _process(self):
        self.__config = PipelineConfig.getPipelineConfig(self)
        print('extracting articles data from database')
        data = NewsDatabase.getArticlesData()

        #store number of articles and articles data also
        self._addMLflowParam('ArticlesCount',data.shape[0])
        if self.__config['StoreData']:
            today = datetime.today().strftime('%Y-%m-%d')
            filepath = os.path.join(DATA_PATH, today,self.__articlesDataFileName)
            if not os.path.exists(os.path.join(DATA_PATH, today)):
                os.makedirs(os.path.join(DATA_PATH, today))
            data.to_csv(filepath)
            self._addMLflowArtifact(filepath)
        
        #last step to store metadata
        self._storeMLflowData()
        return data
    
    def fit(self,x,y=None):
        print('DataExtractor.fit')
        return self

    def transform(self,x):
        print('DataExtractor.transform')
        return self._process()