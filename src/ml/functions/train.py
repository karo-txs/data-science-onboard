from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import ShuffleSplit
from ml.utils.time_tool import TimeTool
from dataclasses import dataclass, field
from ml.models.svm_model import SVMModel
from ml.models.lr_model import LRModel
from ml.models.et_model import ETModel
from ml.interfaces.model import Model
from typing import List
import pandas as pd
import numpy as np
import warnings
import joblib
import csv
import os


@dataclass
class Train:
    x_train: any
    y_train: any
    model_names: List[str]
    models: List[Model] = field(default_factory=lambda: [])
    results_path: str = field(default = "./results")

    def run(self, iterations: int = 1, folds: int = 4, n_iter: int = 100):
        self.set_models()

        for i in range(0, iterations):
            print("\nInteration "+str(i+1))
            cv = ShuffleSplit(n_splits=folds, test_size=0.1)

            for model in self.models:
                time_tool = TimeTool()
                time_tool.init()
                print(f"\n(Hyperparametrization) Start of the {model.name} algorithm at  {time_tool.getInDateTime()}")

                bs_model = RandomizedSearchCV(estimator=model.model, param_distributions=model.params, n_iter=n_iter, scoring="max_error", cv=cv, n_jobs=2, verbose=2)
                bs_model.fit(self.x_train, self.y_train)
                time_tool.end()

                self.save_results(model, bs_model, time_tool, i)

                print(f"End of the {model.name} algorithm at {time_tool.getInDateTime()}\nTotal run time:{time_tool.getExecuTime()}")

    def set_models(self):
        for model_name in self.model_names:
            if model_name == "svm":
                self.models.append(SVMModel())
            elif model_name == "lr":
                self.models.append(LRModel())
            elif model_name == "et":
                self.models.append(ETModel())
    
    def save_results(self, model, bs_model, time_tool, iteration):
        # Save model
        clf = bs_model.best_estimator_
        filepath = f"{self.results_path}/hyperparametrization/models/data_{str(iteration+1)}/"

        if not os.path.exists(filepath):
            os.makedirs(filepath)

        filename = f"{filepath}{clf.__class__.__name__}.joblib.pkl"
        _ = joblib.dump(clf, filename, compress=9)

        # Save results:
        dt = pd.DataFrame(bs_model.cv_results_)
        linhas = {'Algorithm': model.simple_name,
                'n_inter': bs_model.n_iter, 'n_div': bs_model.n_splits_, 'Initial Date/Hour': time_tool.getInDateTime(), 
                'Final Date/Hour': time_tool.getEnDataTime(), 'Execution time': time_tool.getExecuTime(),
                'RMSE': '{:.0%}'.format(bs_model.best_score_), 'Params': bs_model.best_params_}

        path = f"{self.results_path}/hyperparametrization/data_{str(iteration+1)}"
        if not os.path.exists(path):
            os.makedirs(path)
        
        path = f"{path}/hypeResults{bs_model.__class__.__name__}.csv"

        try:
            open(path, 'r')
            with open(path, 'a') as arq:
                writer = csv.writer(arq)
                writer.writerow(linhas.values())
        except IOError:
            dataF = pd.DataFrame.from_dict(linhas)
            dataF.to_csv(path, index=False)
        
