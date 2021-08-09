'''
hyper param tuning
'''
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

class ModelEvaluation(NewsPipeline):
    
    def __init__(self):
        super().__init__()
        self.__modelfilename = 'EvaluatedModel.pkl'
        print('ModelEvaluation instantiated')
    
    @mlflowtimed
    def _process(self,features):
        self.__config = PipelineConfig.getPipelineConfig(self)
        self.id2word, self.gensim_bow, self.tfidfmodel,self.processeddata = features[0], features[1], features[2], features[3]
        self.corpus_tfidf = self.tfidfmodel[self.gensim_bow]
        print('tunning model')
        self.__model = self.__hyperparamtunning()
        if self.__config['Storemodel']:
            self.__savemodel()
        
        self._storeMLflowData()
        return self.__model
   
    def __getcoh(self,corpus, dictionary, k, a, b):
        __model = LdaMulticore(corpus=corpus, 
                               id2word=dictionary,
                               num_topics=k,
                               alpha=a,
                               eta=b,
                               workers=2,
                               random_state=100,
                               chunksize=100,
                               passes=10,
                               per_word_topics=True)
        
        __cohe_model = CoherenceModel(model=__model,corpus=corpus, coherence='u_mass')
        
        return __cohe_model.get_coherence()
    
    def __hyperparamtunning(self):
        print('hyper param tuning')

        topics_range = list(np.arange(9,10,1))
        alpha_range = list(np.arange(0.1,0.5,0.3))
        beta_range = list(np.arange(0.1,0.5,0.3))

        # alpha_range.extend(['asymmetric'])
        # beta_range.extend(['symmetric'])
        
        noofdocs = len(self.processeddata)
        corpus = self.corpus_tfidf
        print('no of docs : ',noofdocs)
        print('dividing corpus  0.25, 0.5, 0.75, 1 shares for testing ')
        corpus_sets = [#gensim.utils.ClippedCorpus(corpus,noofdocs* 0.25),
                      #gensim.utils.ClippedCorpus(corpus,noofdocs* 0.5),
                      #gensim.utils.ClippedCorpus(corpus,noofdocs* 0.75),
                      corpus]
        corpus_title = [ '100% corpus']
        model_results = {'Validation_Set': [],
                         'Topics': [],
                         'Alpha': [],
                         'Beta': [],
                         'Coherence': []
                        }
        if 1==1:
            pbar = tqdm.tqdm(total=540)
            for i in range(len(corpus_sets)):
                for k in topics_range:
                    for a in alpha_range:
                        for b in beta_range:
                            cv = self.__getcoh(corpus_sets[i],self.id2word,k,a,b)
                            model_results['Validation_Set'].append(corpus_title[i])
                            model_results['Topics'].append(k)
                            model_results['Alpha'].append(a)
                            model_results['Beta'].append(b)
                            model_results['Coherence'].append(cv)
                            print('Topics - {0}, Alpha - {1}, Beta - {2}, Coherence - {3}'.format(k,a,b,cv))
                            pbar.update(1)
                            
            results = pd.DataFrame(model_results)
            today = datetime.today().strftime('%Y-%m-%d')
            filepath = os.path.join(DATA_PATH, today)
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            processeddatafile = os.path.join(filepath,'lda_tuning_results.csv')
            if os.path.exists(processeddatafile):
                os.remove(processeddatafile)
            results.to_csv(processeddatafile)
            print(results)
            pbar.close()
            goodvals = results.loc[results['Coherence'].idxmax()]
            __model = LdaMulticore(corpus=corpus, 
                               id2word=self.id2word,
                               num_topics=goodvals['Topics'],
                               alpha=goodvals['Alpha'],
                               eta=goodvals['Beta'],
                               workers=2,
                               random_state=100,
                               chunksize=100,
                               passes=10,
                               per_word_topics=True)
            
            self._addMLflowMetric('num_topics',goodvals['Topics'])
            self._addMLflowMetric('alpha',goodvals['Alpha'])
            self._addMLflowMetric('eta',goodvals['Beta'])

            return __model

    def fit(self,x,y=None):
        print('ModelEvaluation.fit')
        return self
    def transform(self,x):
        print('ModelEvaluation.transform')
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

