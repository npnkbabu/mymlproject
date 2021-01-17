import argparse
import json
import os
import sys
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

from DataAnalysis.data_analysis import DataAnalysis
from DataExtractor.data_extractor import DataExtractor
from DataPreparation.data_preparation import DataPreparation
from DataValidation.data_validation import DataValidation
from ModelTraining.model_training import ModelTraining
from ModelEvaluation.model_evaluation import ModelEvaluation
from ModelValidation.model_validation import ModelValidation

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR,'config')

class Process():
    def __init__(self,config):
        print('process started')

        self.__config = config

        __dataExtractionConfig = self.__config.get('Data')['Extraction']
        __dataAnalysisConfig = self.__config.get('Data')['Analysis']
        __dataValidationConfig = self.__config.get('Data')['Validation']
        __dataPreparationConfig = self.__config.get('Data')['Preparation']

        self.__dataExtractor = DataExtractor(__dataExtractionConfig)
        self.__dataAnalyzer = DataAnalysis(__dataAnalysisConfig)   
        self.__dataValidation = DataValidation(__dataValidationConfig)
        self.__dataPreparation = DataPreparation(__dataPreparationConfig)

        __modelTrainingConfig = self.__config.get('Model')['Training']
        __modelEvaluationConfig = self.__config.get('Model')['Evaluation']
        __modelValidationConfig = self.__config.get('Model')['Validation']
        self.__modelTraining = ModelTraining(__modelTrainingConfig)
        self.__modelValidation = ModelValidation(__modelEvaluationConfig)
        self.__modelEvaluation = ModelEvaluation(__modelValidationConfig)

        self.startProcess()

    def startProcess(self):
        try:
            #pipeline design
            #datapipeline , modelpipeline
            self.__dataPipeline = Pipeline(steps=[('dataextraction',self.__dataExtractor),\
                                                  ('dataanalysis',self.__dataAnalyzer),\
                                                  ('datavalidation',self.__dataValidation),\
                                                  ('datapreparation',self.__dataPreparation)])

            self.__modelPipeline = Pipeline(steps=[('modeltraining',self.__modelTraining),\
                                                   ('modelevaluation',self.__modelEvaluation),\
                                                   ('modelvalidation',self.__modelValidation)])
            self.__mainPipeline = Pipeline(steps=[('datapipeline',self.__dataPipeline),\
                                                  ('modelpipeline',self.__modelPipeline)])
            
            #Data extractor is common for both Experiment and Prod
            self.__mainPipeline.fit_transform(1)
        
        except Exception as ex:
            print(ex)
        
        input('press any key to stop')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config',
                      help='Absolute path to configuration file.')
    args = parser.parse_args()
    if not args.config:
        print('no config file')
        exit()
    else:
        with open(os.path.join(CONFIG_PATH,args.config), 'r') as file:
            config = json.load(file)
    
    obj = Process(config)
