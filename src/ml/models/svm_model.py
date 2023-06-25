from skopt.space import Real, Categorical, Integer
from src.ml.interfaces import Model
from sklearn.svm import SVR as SVM


class SVMModel(Model):

    def __post_init__(self):
        self.params = {
            "C": Real(1e-1, 1e1),
            "kernel": Categorical(['linear', 'rbf']),
            "gamma": Categorical(['scale', 'auto']),
            "shrinking": [True, False],
            "probability": [True, False],
            "tol": Real(1e-5, 1e-3).
            "cache_size": [500],
            "decision_function_shape": Categorical(['ovo', 'ovr'])
        }
        
        self.model = SVM()
        self.name = self.model.__class__.__name__
        self.simple_name = "SVM"
