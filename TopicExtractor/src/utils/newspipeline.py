from sklearn.base import BaseEstimator, TransformerMixin
from abc import abstractmethod
from utils.metadatastore import *

class NewsPipeline(BaseEstimator,TransformerMixin):

    def __init__(self):
        self.__paramDict = {}
        self.__metricDict = {}
        self.__artifactList = []
    
    @abstractmethod
    def _process(self,data=None):
        pass

    def fit(self,x,y=None):
        return self

    def transform(self,x):
        return self

    def _storeMLflowData(self):
        logParam(self,self.__paramDict)
        logMetric(self,self.__metricDict)
        logArtifacts(self,self.__artifactList)

    def _addMLflowParam(self,name,value):
        self.__paramDict[self.__class__.__name__+'.'+name]=value

    def _addMLflowMetric(self,name,value):
        self.__metricDict[self.__class__.__name__+'.'+name]=value

    def _addMLflowArtifact(self,filepath):
        self.__artifactList.append(filepath)
