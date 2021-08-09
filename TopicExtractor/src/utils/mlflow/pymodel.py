import numpy as np
from mlflow.pyfunc import PythonModel
from sklearn.base import clone

class PyModel(PythonModel):

    def __init__(self, estimator=None):
        self.estimator = estimator

    def fit(self, X, y=None):
        return self

    def predict(self, context, X):
        return 1