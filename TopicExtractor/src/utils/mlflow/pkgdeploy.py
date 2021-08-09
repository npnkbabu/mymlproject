import mlflow

def logModel(model):
    mlflow.pyfunc.log_model(artifact_path="model",python_model=model)
    # mlflow.pyfunc.save_model(
    #     path=model_path,
    #     python_model=model,
    #     code_path=['multi_model.py'],
    #     conda_env={
    #         'channels': ['defaults', 'conda-forge'],
    #         'dependencies': [
    #             'mlflow=1.2.0',
    #             'numpy=1.16.5',
    #             'python=3.6.9',
    #             'scikit-learn=0.21.3',
    #             'cloudpickle==1.2.2'
    #         ],
    #         'name': 'mlflow-env'
    #     }
    # )

def loadModel(model):
    #mlflow.pyfunc.load_model
    pass

# we don't have predefined pkg to save LDA model. so we need to use generic pyfunc
def saveModel(model):
    #mlflow.pyfunc.save_model
    pass


