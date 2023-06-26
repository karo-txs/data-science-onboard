from skopt.space import Real, Categorical, Integer
from ml.interfaces.model import Model
from sklearn.svm import SVR as SVM


class SVMModel(Model):

    def __init__(self):
        self.params = {
            "C": [0.001, 0.1 ,1,5],
            "kernel":['linear', 'rbf'],
            "gamma": ['scale', 'auto'],
            "shrinking": [True, False],
            "tol": [1e-1, 1e-2, 1e-3, 1e-4],
            "cache_size": [500]
        }
        
        self.model = SVM()
        self.name = self.model.__class__.__name__
        self.simple_name = "SVM"
