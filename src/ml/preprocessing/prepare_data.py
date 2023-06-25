from ml.preprocessing.split_dataset import SplitDataset
from ml.preprocessing.label_encoder import Encoder
from dataclasses import dataclass, field
from ml.preprocessing.tfidf import TFIDF
import pandas as pd


@dataclass
class PrepareData:
    data: pd.DataFrame
    targed: str
    info_data: dict

    def apply(self):

        y = self.data[target]
        X = self.data.filter(self.info_data.keys(), axis=1)

        for key in self.info_data:
            if self.info_data[key] == "multi_label":
                X[[f"{key}_1", f"{key}_2"]] = X[key].str.split(',', 2, expand=True).fillna(value="")
                X[f"{key}_2"]=X[f"{key}_2"].fillna(X[f"{key}_1"], inplace=True)
        
        print(X.head())

        split = SplitDataset(X, y)
        X_train, X_test, y_train, y_test = split.apply()

        for key in self.info_data:

            if self.info_data[key] == "text":
                tfidf = TFIDF(X_train[key], is_train=True)
                X_train[key] = tfidf.apply()

                tfidf = TFIDF(X_test[key], is_train=False)
                X_test[key] = tfidf.apply()

            elif self.info_data[key] == "label" or self.info_data[key] == "multi_label":
                encoder = Encoder(X_train[key], is_train=True)
                X_train[key] = encoder.apply()

                encoder = Encoder(X_test[key], is_train=False)
                X_test[key] = encoder.apply()
        
        return X_train, X_test, y_train, y_test
