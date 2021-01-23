from sklearn.base import BaseEstimator, TransformerMixin
from abc import abstractmethod

class NewsPipeline(BaseEstimator,TransformerMixin):

    def __init__(self):
        super.__init__()
    
    @abstractmethod
    def _process(self,data=None):
        pass

    def fit(self,x,y=None):
        return self

    def transform(self,x):
        return self
