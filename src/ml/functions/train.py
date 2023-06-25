from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import ShuffleSplit
from src.ml.utils.time_tool import TimeTool
from dataclasses import dataclass, field
from ml.models.svm_model import SVMModel
from ml.models.lr_model import LRModel
from ml.models.et_model import ETModel
from src.ml.interfaces import Model
from skopt import BayesSearchCV
import pandas as pd
import numpy as np
import warnings
import joblib
import csv


@dataclass
class Train:
    x_train: any
    y_train: any
    model_names: List[str]
    models: List[Model] = field(defaulf=[])
    results_path: str = field(default = "../../../results/")

    def run(self, iterations: int = 1, folds: int = 6, n_splits: int = 6, n_iter: int = 150):
        self.set_models()

        for i in range(0, iterations):
            for j in range(0, folds):
                print("\nInteration "+str(i+1), "Fold "+str(j+1))
                cv = ShuffleSplit(n_splits=n_splits, test_size=0.1)

                for model in self.models:
                    time_tool = TimeTool()
                    time_tool.init()
                    print(f"\n(Hyperparametrization) Start of the {model.name} algorithm at  {time_tool.getInDateTime()}")
                    bs_model = BayesSearchCV(estimator=model.name, search_spaces=model.params, n_iter=n_iter, scoring='rmse', cv=cv, refit=True, return_train_score=False, n_jobs=3, n_points=3, pre_dispatch=3)
                    bs_model.fit(self.x_train, self.y_train)
                    time_tool.end()

                    self.save_results(model, bs_model, time_tool)

                    print(f"End of the {model.name} algorithm at {time_tool.getInDateTime()}\nTotal run time:{time_tool.getExecuTime()}")

    def set_models(self):
        for model_name in self.model_names:
            if model_name == "svm":
                self.models.append(SVMModel())
            elif model_name == "lr":
                self.models.append(LRModel())
            elif model_name == "et":
                self.models.append(ETModel())
    
    def save_results(self, model, bs_model, time_tool):
        # Save model
        clf = bs_model.best_estimator_
        filename = f"{self.results_path}/hyperparametrization/models/data_{str(i+1)}/{clf.__class__.__name__}{str(j+1)}.joblib.pkl"
        _ = joblib.dump(clf, filename, compress=9)

        # Save results:
        dt = pd.DataFrame(bs_model.cv_results_)
        linhas = {'Algorithm': model.simple_name,
                'n_inter': bs_model.n_iter, 'n_div': bs_model.n_splits_, 'Initial Date/Hour': time_tool.getInDateTime(), 
                'Final Date/Hour': time_tool.getEnDataTime(), 'Execution time': time_tool.getExecuTime(),
                'RMSE': '{:.0%}'.format(bs_model.best_score_), 'Params': bs_model.best_params_}
        path = f"{self.results_path}/hyperparametrization/data_{str(i+1)}/hypeResults{bs_model.__class__.__name__}({NomeClf[modelName]}).csv"

        try:
            open(path, 'r')
            with open(path, 'a') as arq:
                writer = csv.writer(arq)
                writer.writerow(linhas.values())
        except IOError:
            dataF = pd.DataFrame(columns=linhas.keys())
            dataF = dataF.append(linhas, ignore_index=True)
            dataF.to_csv(path, index=False)
        
