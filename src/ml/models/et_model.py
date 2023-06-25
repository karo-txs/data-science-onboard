from sklearn.ensemble import ExtraTreesRegressor as ET
from skopt.space import Real, Categorical, Integer
from src.ml.interfaces import Model


class ETModel(Model):
    def __post_init__(self):
        self.params = {
            "n_estimators": Integer(150, 1100),
            "criterion": Categorical(['gini', 'entropy']),
            "max_depth": Integer(20, 120),
            "min_samples_split": Integer(2,20),
            "min_samples_leaf": [1],
            "max_features": Categorical(['auto', 'sqrt', 'log2']),
            "max_leaf_nodes": Integer(50, 150),
            "warm_start": [True, False],
            "max_samples": Real(0.01, 0.9)
        }
        
        self.model = ET()
        self.name = self.model.__class__.__name__
        self.simple_name = "ET"