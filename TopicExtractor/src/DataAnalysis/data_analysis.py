#its called from FeatureStore before generating features we get results from this analysis and decide features.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from gensim import corpora, models
from gensim.models import TfidfModel
import gensim
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
import sys
import os
from datetime import datetime

from utils.newspipeline import NewsPipeline
from TopicExtractor.src.utils.metadatastore import *
from TopicExtractor.src.utils.pipelineconfig import PipelineConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DATA_PATH = os.path.join(BASE_DIR,'data')

class DataAnalysis(NewsPipeline):
    
    def __init__(self):
        print('DataAnalysis instantiated')
        self.__wordCloudfilename = 'WordCloud.png'
        super().__init__()

    @mlflowtimed
    def _process(self,df_articles):
        try:
            self.__config = PipelineConfig.getPipelineConfig(self)
            if self.__config['Enable']:
                df = pd.DataFrame(df_articles)
                df['index'] = df.index
                nullindex = df[df['content'].isnull()].index
                df.drop(index=nullindex,inplace=True)
                self.__stop_words = set(stopwords.words('english'))
                self.__wordnetLemmatizer = WordNetLemmatizer()
                self.__stemmer = PorterStemmer()
                df['processed_content'] = df['content'].map(self.__preprocess)
                print('EDA by giving word cloud')
                _wordcloud = WordCloud()
                tokens = []
                lst = [[tokens.append(y) for y in x] for x in df['processed_content']]
                longstring = ','.join(tokens)
                _wordcloud.generate(longstring)
                plt.imshow(_wordcloud)
                plt.axis('off')
                #plt.show()
                today = datetime.today().strftime('%Y-%m-%d')
                filepath = os.path.join(DATA_PATH, today,self.__wordCloudfilename)
                plt.savefig(filepath)
                self._addMLflowArtifact(filepath)
                self._storeMLflowData()

            return df_articles
    
        except:
            print(sys.exc_info())
            return False
    
    def fit(self,x,y=None):
        print('DataAnalysis.fit')
        return self

    def transform(self,x):
        print('DataAnalysis.transform')
        return self._process(x)

    def __preprocess(self,line):
        result=[]
        tokens=[]
        line = re.sub(r'[0-9!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]','',line)
        line = line.strip()
        tokens = word_tokenize(line)
        tokens = [x for x in tokens if len(x)>2]
        tokens = list(map(lambda x : x.lower(),tokens))
        tokens = [x for x in tokens if x not in self.__stop_words]
        tokens = list(map(lambda x : self.__stemmer.stem(x),tokens))
        pos_tags = nltk.pos_tag(tokens)
        for token,postag in pos_tags:    
            pos = self.__getPosTagDef(postag)
            if pos != '':
                result.append(self.__wordnetLemmatizer.lemmatize(token,pos))
            else:
                result.append(self.__wordnetLemmatizer.lemmatize(token))
        return result

    def __getPosTagDef(self,postag):
        try:
            if postag.startswith('J'):
                return wordnet.ADJ
            if postag.startswith('V'):
                return wordnet.VERB
            if postag.startswith('N'):
                return wordnet.NOUN
            if postag.startswith('R'):
                return wordnet.ADV
            else:
                return ''
        except:
            print(sys.exc_info()[0])