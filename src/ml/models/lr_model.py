from sklearn.linear_model import LogisticRegression as LR
from skopt.space import Real, Categorical, Integer
from ml.interfaces.model import Model


class LRModel(Model):
    def __init__(self):
        self.params = {
            "penalty": Categorical(['none']),
            "tol": Real(1e-5, 1e-3),
            "C": Real(1e-1, 1.2),
            "fit_intercept": [True, False],
            "intercept_scaling": Real(1e-3, 1e3),
            "solver": Categorical(['newton-cg', 'lbfgs', 'sag']),
            "max_iter": Integer(20, 1000),
            "warm_start": [True, False],
            "n_jobs": [-1],
            "l1_ratio": Real(0, 1)
        }
        
        self.model = LR()
        self.name = self.model.__class__.__name__
        self.simple_name = "LR"