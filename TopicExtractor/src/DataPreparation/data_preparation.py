'''
Here we trim features data like rounding tfidf value
'''
import numpy as np
import pandas as pd
import os
from datetime import datetime
from datetime import datetime
import pickle

from utils.newspipeline import NewsPipeline
from DataPreparation.data_preprocessor import DataPreProcessor
from DataPreparation.data_feature_generator import DataFeatureGenerator
from TopicExtractor.src.utils.mlflow.metadatastore import *
from TopicExtractor.src.utils.pipelineconfig import PipelineConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATA_PATH = os.path.join(BASE_DIR,'data')

class DataPreparation(NewsPipeline):

    def __init__(self):
        self.__config = PipelineConfig.getPipelineConfig(self)
        super().__init__()
        print('DataPreparation instantiated')

    @mlflowtimed
    def _process(self,data):
        self.__dataFeatGen = DataFeatureGenerator(self.__config)
        self.__dataPreProc = DataPreProcessor(self.__config)
        retData =  self.__dataFeatGen.process(self.__dataPreProc.process(data))
        
        for file in self.__dataFeatGen.artifactsList:
            self._addMLflowArtifact(file)
        
        self._storeMLflowData()
        return retData

    def fit(self,x,y=None):
        print('DataPreparation.fit')
        # if (self.__config['Storepipeline']):
        #     self.__storePipeline()
        return self

    def transform(self,x):
        print('DataPreparation.transform')
        return self._process(x)

    def __storePipeline(self):
        print('storing pipeline')
        try:
            today = datetime.today().strftime('%Y-%m-%d')
            dataPipelineFile = os.path.join(DATA_PATH, today,'dataPipeline.pkl')
            if os.path.isfile(dataPipelineFile):
                os.remove(dataPipelineFile)
            with open(dataPipelineFile,'wb') as plkfile:
                pickle.dump(self,plkfile)
            return True
        except Exception as ex:
            print(ex)
            return False
