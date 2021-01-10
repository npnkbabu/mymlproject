import argparse
import json
import os
import sys

from FeatureStore.data_collector import DataCollector
from FeatureStore.data_picker import DataPicker
from FeatureStore.data_preprocessor import DataPreProcessor
from FeatureStore.data_feature_generator import DataFeatureGenerator
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
        self.config = config
        self._dataCollector= DataCollector()
        self._dataPicker = DataPicker()
        self._dataPreProcessor = DataPreProcessor()
        self._dataFeatureGenerator = DataFeatureGenerator()
        self._dataAnalyzer = DataAnalysis()

        self._dataExtractor = DataExtractor()
        self._dataPreparation = DataPreparation()
        self._dataValidation = DataValidation()

        self._modelTraining = ModelTraining()
        self._modelValidation = ModelValidation()
        self._modelEvaluation = ModelEvaluation()

        self.startProcess()

    def startProcess(self):
        try:
            #collect the data from news API ?
            DataCollectionconfig = self.config.get('Data')['Collection']
            if DataCollectionconfig.get('Collect'):
                if self._dataCollector.process(DataCollectionconfig) == False:
                    print('Not able to get data from newsAPI')
                    return
            
            #get data from database
            df_articles =  self._dataPicker.process()
            if df_articles is None:
                print('Not able to retrieve articles data')
                return
            
            #start preprocessing and insert data into feature store
            elif self._dataPreProcessor.process(df_articles) == False:
                print('Preprocessing failed')
                return
            elif self._dataAnalyzer.process(df_articles) == False:
                print('Data analyzer error')
                return
            elif self._dataFeatureGenerator.process(df_articles):
                print('Features genearated. so starting extracting data')

            #collect features and prepare model
            features  = self._dataExtractor.process()
            # if not features:
            #     print('error in data extractor')
            #     return
            # if self._dataPreparation.process(features) == False:
            #     print('error in data preparation')
            #     return
            # elif self._dataValidation.process(features) == False:
            #     print('error in data validation')
            #     return
            # else:
            modelTrainingObj = self._modelTraining.process(features)
            if not modelTrainingObj:
                print('error in model training')
                return
            model = self._modelEvaluation.process(modelTrainingObj)
            if not model:
                print('error in model evaluation ')
                return
            elif self._modelValidation.process(model) == False:
                print('error in model validation')
                return

         
        except:
            print(sys.exc_info()[0])


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
