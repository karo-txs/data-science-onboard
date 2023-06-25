from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error
from dataclasses import dataclass, field
from ml.models.svm_model import SVMModel
from ml.models.lr_model import LRModel
from ml.models.et_model import ETModel
from src.ml.interfaces import Model
import pandas as pd
import numpy as np
import warnings
import joblib
import csv


@dataclass
class Test:
    x_test: any
    y_test: any
    model_names: List[str]
    models: List[Model] = field(defaulf=[])
    results_path: str = field(default = "../../../results/")

    def run(self, iterations: int = 1, folds: int = 6, n_splits: int = 6, n_iter: int = 150):
        self.set_models()
        cv_mean = get_structure_results()

        for i in range(0, iterations):
            for j in range(0, folds):
                print("\nInteration "+str(i+1), "Fold "+str(j+1))
                for model in self.models:

                    print(f"\nTest of the {model.name} algorithm")
                    filename = f"{self.results_path}/hyperparametrization/models/data_{str(i+1)}/{clf.__class__.__name__}{str(j+1)}.joblib.pkl"
                    clf = joblib.load(filename)

                    y_pred = clf.predict(self.x_test)

                    r2, mae, rmse = self.get_results(y_pred, y_test)

                    score = {'Algoritmo': model.name, 'interaction': str(i+1), 'R2': r2, 'MAE': mae, 'RMSE': rmse}
                    path = f"{self.results_path}/evaluation/data_{str(index + 1)}/score.csv"
                    self.save_csv(path, score)

                    cv_mean[model.name]['R2'] += r2
                    cv_mean[model.name]['MAE'] += mae
                    cv_mean[model.name]['RMSE'] += rmse
                
            
            cv_mean = self.mean_calculate(folds, cv_mean)
            for clf in cv_mean:
                r2 = cv_mean[clf]['R2']
                mae = cv_mean[clf]['MAE']
                rmse = cv_mean[clf]['RMSE']

                final_mean[clf]['R2'] += r2
                final_mean[clf]['MAE'] += mae
                final_mean[clf]['RMSE'] += rmse

                helper_cv_mean = {'Algoritmo': clf, 'R2': r2, 'MAE': mae, 'RMSE': rmse}
                helper_general_cv_mean = {'Algoritmo': clf, 'Interaction': index+1, 'R2': r2, 'MAE': mae, 'RMSE': rmse}

                path = f"{self.results_path}/evaluation/data_{str(index + 1)}/cv_mean.csv"
                self.save_csv(path, helper_cv_mean)
                path = f"{self.results_path}/evaluation/general_cv_mean.csv"
                self.save_csv(path, helper_general_cv_mean)

        final_mean = self.mean_calculate(iterations, final_mean)
        path = f"{self.results_path}/evaluation/final_mean.csv"
        for clf in final_mean:
            r2 = final_mean[clf]['R2']
            mae = final_mean[clf]['MAE']
            rmse = final_mean[clf]['RMSE']

            helper_final_mean = {'Algoritmo': clf, 'R2': r2, 'MAE': mae, 'RMSE': rmse}
            self.save_csv(path, helper_final_mean)

    def set_models(self):
        for model_name in self.model_names:
            if model_name == "svm":
                self.models.append(SVMModel())
            elif model_name == "lr":
                self.models.append(LRModel())
            elif model_name == "et":
                self.models.append(ETModel())
    
    def save_csv(path, dictionary):
        try:
            open(path, 'r')
            with open(path, 'a') as arq:
                writer = csv.writer(arq)
                writer.writerow(dictionary.values())
        except IOError:
            dataF = pd.DataFrame(columns=dictionary.keys())
            dataF = dataF.append(dictionary, ignore_index=True)
            dataF.to_csv(path, index=False)


    def mean_calculate(self, div, dictionary):
        for algorithm in dictionary:
            for metric in dictionary[algorithm]:
                dictionary[algorithm][metric] = dictionary[algorithm][metric] / div
        return dictionary


    def get_structure_results(self):
        return {'ET': {'R2': 0.0, 'MAE': 0.0, 'RMSE': 0.0,},
                'LR': {'R2': 0.0, 'MAE': 0.0, 'RMSE': 0.0,},
                'SVM': {'R2': 0.0, 'MAE': 0.0, 'RMSE': 0.0,}}
    
    def get_results(self, y_pred, y_test):
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test,y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        return r2, mae, rmse


    def remove(self, dictionary, key_remove):
        new_dict = {}
        for key, value in dictionary.items():
            if key is not key_remove:
                new_dict[key] = value

        return new_dict
