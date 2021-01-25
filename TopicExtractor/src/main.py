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
            self.__dataPrePipeline = Pipeline(steps=[('dataextraction',self.__dataExtractor),\
                                                  ('dataanalysis',self.__dataAnalyzer)])
                                                
            self.__dataPipeline = Pipeline(steps=[('datavalidation',self.__dataValidation),\
                                                  ('datapreparation',self.__dataPreparation)])

            self.__modelPipeline = Pipeline(steps=[('modeltraining',self.__modelTraining),\
                                                   ('modelevaluation',self.__modelEvaluation),\
                                                   ('modelvalidation',self.__modelValidation)])
            
            self.__mainPipeline = Pipeline(steps=[('dataprepipeline',self.__dataPrePipeline),\
                                                  ('datapipeline',self.__dataPipeline),\
                                                  ('modelpipeline',self.__modelPipeline)])
            
            #self.__mainPipeline.fit(1)
            #self.__storeDatapipeline()
            #self.__predictSample()

        
        except Exception as ex:
            print(ex)
        
        input('press any key to stop')
 

    def __storeDatapipeline(self):
        print('storing data pipeline')
        try:
            today = datetime.today().strftime('%Y-%m-%d')
            dataPipelineFile = os.path.join(DATA_PATH, today,'dataPipeline.pkl')
            if os.path.isfile(dataPipelineFile):
                os.remove(dataPipelineFile)
            with open(dataPipelineFile,'wb') as plkfile:
                pickle.dump(self.__dataPipeline,plkfile)
            return True
        except:
            print(sys.exc_info())
            return False
    
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config',
                      help='Absolute path to configuration file.')
    args = parser.parse_args()
    if not args.config:
        print('no config file')
        exit()
    else:
        obj = Process()
