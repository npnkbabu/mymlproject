'''
Similar to data we do validate the model in production pipeline with new data and check if its performance is as per 
        buisness expectation and better than previous model and compatible with prediciton service etc.
'''
import pandas as pd
import numpy as np
from datetime import datetime

from utils.newspipeline import NewsPipeline
from TopicExtractor.src.utils.mlflow.metadatastore import *
from TopicExtractor.src.utils.mlflow.pkgdeploy import *
from TopicExtractor.src.utils.mlflow.pymodel import *
from TopicExtractor.src.utils.pipelineconfig import PipelineConfig

import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATA_PATH = os.path.join(BASE_DIR,'data')

class ModelValidation(NewsPipeline):
    
    def __init__(self):
        super().__init__()
        print('ModelValidation instantiated')
        self.__modelfilename = 'ValidatedModel.pkl'
    
    @mlflowtimed
    def _process(self,model):
        self.__config = PipelineConfig.getPipelineConfig(self)
        self.__model = model
        #check if this model is better than previous model
        if self.__config['Storemodel']:
            self.__savemodel()
        print('ModelValidation done')

        self._storeMLflowData()
        return model

    def __savemodel(self):
        print('storing topic model')
        try:
            today = datetime.today().strftime('%Y-%m-%d')
            topicmodelfile = os.path.join(DATA_PATH, today,self.__modelfilename)
            if os.path.isfile(topicmodelfile):
                os.remove(topicmodelfile)
            with open(topicmodelfile,'wb') as plkfile:
                pickle.dump(self.__model,plkfile)
            
            self.__pymodel = PyModel(self.__model)
            #logModel(self.__pymodel)
            return True
        except Exception as ex:
            print(ex)
            return False

    def fit(self,x,y=None):
        print('ModelValidation.fit')
        return self
    def transform(self,x):
        print('ModelValidation.transform')
        return self._process(x)
