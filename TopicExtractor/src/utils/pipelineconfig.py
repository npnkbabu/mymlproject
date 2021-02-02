
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
CONFIG_PATH = os.path.join(BASE_DIR,'config')
CONFIG_FILE = 'topicextractor.json'

class PipelineConfig:
  
    @staticmethod
    def getPipelineConfig(obj):
        with open(os.path.join(os.path.join(CONFIG_PATH,CONFIG_FILE)), 'r') as file:
            config= json.load(file)
        
        if obj.__class__.__name__ == 'DataExtractor':
            return config['Pipeline'].get('Data')['Extraction']
        elif obj.__class__.__name__ == 'DataAnalysis':
            return config['Pipeline'].get('Data')['Analysis']
        elif obj.__class__.__name__ == 'DataValidation':
            return config['Pipeline'].get('Data')['Validation']
        elif obj.__class__.__name__ == 'DataPreparation':
            return config['Pipeline'].get('Data')['Preparation']
        elif obj.__class__.__name__ == 'ModelTraining':
            return config['Pipeline'].get('Model')['Training']
        elif obj.__class__.__name__ == 'ModelEvaluation':
            return config['Pipeline'].get('Model')['Evaluation']
        elif obj.__class__.__name__ == 'ModelValidation':
            return config['Pipeline'].get('Model')['Validation']

        return None
