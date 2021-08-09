import argparse
import json
import os
import sys
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from datetime import datetime
import pickle
import pandas as pd
import numpy as np

from DataAnalysis.data_analysis import DataAnalysis
from DataExtractor.data_extractor import DataExtractor
from DataPreparation.data_preparation import DataPreparation
from DataValidation.data_validation import DataValidation
from ModelTraining.model_training import ModelTraining
from ModelEvaluation.model_evaluation import ModelEvaluation
from ModelValidation.model_validation import ModelValidation
from utils.pipelineconfig import PipelineConfig
import mlflow

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR,'config')
DATA_PATH = os.path.join(BASE_DIR,'data')

class Process():
    def __init__(self):
        print('process started')

        #create objects
        self.__dataExtractor = DataExtractor()
        self.__dataAnalyzer = DataAnalysis()   
        self.__dataValidation = DataValidation()
        self.__dataPreparation = DataPreparation()

        self.__modelTraining = ModelTraining()
        self.__modelEvaluation = ModelEvaluation()
        self.__modelValidation = ModelValidation()
        
        self.startProcess()
    
    def startProcess(self):
        try:
            #data pipeline
            self.__dataPipeline = Pipeline(steps=[('dataextraction',self.__dataExtractor),\
                                                  ('dataanalysis',self.__dataAnalyzer),\
                                                  ('datavalidation',self.__dataValidation),\
                                                  ('datapreparation',self.__dataPreparation)\
                                                  ])
            #model pipeline
            self.__modelPipeline = Pipeline(steps=[('modeltraining',self.__modelTraining),\
                                                   ('modelevaluation',self.__modelEvaluation),\
                                                   ('modelvalidation',self.__modelValidation)\
                                                  ])
            #main pipeline
            self.__mainPipeline = Pipeline(steps=[('datapipeline',self.__dataPipeline),\
                                                  ('modelpipeline',self.__modelPipeline)])
            
            #below step is to run pipeline
            _finalModel = self.__mainPipeline.fit_transform(1)

            


        
        except Exception as ex:
            print(ex)
        

    def __predictSample(self):
        try:
            today = datetime.today().strftime('%Y-%m-%d')
            dataPrep = os.path.join(DATA_PATH, today,'dataPipeline.pkl')
            modelfile = os.path.join(DATA_PATH, today,'topicmodel.pkl')
            with open(dataPrep,'rb') as plkfile:
                __prepareData = pickle.load(plkfile)
            with open(modelfile,'rb') as plkfile:
                model = pickle.load(plkfile)
            
            sample = os.path.join(DATA_PATH, today,'sampledata.txt')
            with open(sample) as testfile:
                sampleData = ''.join(testfile.readlines())
            tuples = [[1,sampleData]]
            df = pd.DataFrame(tuples,columns=['article_id','content'])
            processedData = __prepareData.transform(df)
            corpus = processedData[1]
            id2word = processedData[0]
            result = model[corpus]
            print(model.print_topics())
        
        except Exception as ex:
            print(ex)
    

if __name__ == '__main__':

    runname = 'TopicExtractor'
    expID=0
    with mlflow.start_run(run_name=runname,experiment_id=expID) as exp:
        obj = Process()
    
    input('press any key to stop')
    
