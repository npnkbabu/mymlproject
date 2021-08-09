import pandas as pd
import numpy as np
from gensim.models import LdaMulticore
from gensim.models import CoherenceModel
from tqdm import trange
import tqdm
import gensim
import pickle
import os
import shutil
from datetime import datetime
import sys

from utils.newspipeline import NewsPipeline
from TopicExtractor.src.utils.mlflow.metadatastore import *
from TopicExtractor.src.utils.pipelineconfig import PipelineConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATA_PATH = os.path.join(BASE_DIR,'data')

class ModelTraining(NewsPipeline):
    
    def __init__(self):
        super().__init__()
        self.__modelfilename = 'BaseModel.pkl'
        print('ModelTraining instantiated')

    @mlflowtimed
    def _process(self,features):
        self.__config = PipelineConfig.getPipelineConfig(self)
        self.id2word, self.gensim_bow, self.tfidfmodel,self.processeddata = features[0], features[1], features[2], features[3]
        self.corpus_tfidf = self.tfidfmodel[self.gensim_bow]
        self.__createbasemodel()

        self._storeMLflowData()
        return features

    def __createbasemodel(self):
        print('Creating base model')
        #Topics	Alpha	Beta	Coherence
        #6	asymmetric	symmetric	0.723863804

        self.__model = LdaMulticore(corpus=self.corpus_tfidf, id2word=self.id2word,num_topics=6,
                                    alpha='asymmetric',eta='symmetric',
                                    workers=2,random_state=100,chunksize=100,passes=10,per_word_topics=True)
        if self.__config['Storemodel']:
            self.__savemodel()
        print(self.__model.print_topics())
        print(self.__model[self.gensim_bow])
        print('calculating coherence')
        #__cohe_model = CoherenceModel(model=self.__model,texts=self.processeddata,dictionary=self.id2word,coherence='c_v')
        __cohe_model = CoherenceModel(model=self.__model, corpus=self.corpus_tfidf, coherence='u_mass') 
        __cohe = __cohe_model.get_coherence()
        print('coherence :',__cohe)

        self._addMLflowMetric('BaseModel.Coherence',__cohe)
        return self.__model
    
    def fit(self,x,y=None):
        print('ModelTraining.fit')
        return self
    def transform(self,x):
        print('ModelTraining.transform')
        return self._process(x)

    def __savemodel(self):
        print('storing topic model')
        try:
            today = datetime.today().strftime('%Y-%m-%d')
            topicmodelfile = os.path.join(DATA_PATH, today,self.__modelfilename)
            if os.path.isfile(topicmodelfile):
                os.remove(topicmodelfile)
            with open(topicmodelfile,'wb') as plkfile:
                pickle.dump(self.__model,plkfile)
            
            return True
        except Exception as ex:
            print(ex)
            return False
    
        
    
        