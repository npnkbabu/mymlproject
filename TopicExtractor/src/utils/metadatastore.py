import mlflow
from time import time


def mlflowtimed(fun):
    def wrapper(*args, **kwargs):
        start = time()
        result = fun(*args,**kwargs)
        elapsed = time()-start
        mlflow.log_param('{0}_time'.format(fun.__qualname__),elapsed)
        return result
    return wrapper

def logParam(obj,datadict):
    mlflow.log_params(datadict)

def logMetric(obj,datadict):
    mlflow.log_metrics(datadict)

def logArtifacts(obj,filepaths):
    folder = obj.__class__.__name__
    for path in filepaths:
        mlflow.log_artifact(path,artifact_path=folder)


