from sklearn.base import BaseEstimator, TransformerMixin

class Processor(BaseEstimator,TransformerMixin):

    def __init__(self,config=None):
        super.__init__()

    def process(self,data=None):
        pass

    def fit(self,x,y=None):
        return self

    def transform(self,x):
        return self
