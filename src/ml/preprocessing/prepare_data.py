from ml.preprocessing.split_dataset import SplitDataset
from ml.preprocessing.label_encoder import Encoder
from dataclasses import dataclass, field
from ml.preprocessing.tfidf import TFIDF
import pandas as pd
import nltk


@dataclass
class PrepareData:
    data: pd.DataFrame
    target: str
    info_data: dict

    def apply(self):

        nltk.download('punkt')

        updates = list()

        for key in self.info_data:
            if self.info_data[key] == "multi_label":
                self.data[[f"{key}_1", f"{key}_2", f"{key}_3"]] = self.data[key].str.split(pat=",", n=2, expand=True).fillna(value="")
                self.data = self.data.drop([f"{key}_3"], axis=1)
                self.data = self.data.drop(key, axis=1)

                updates.extend([f"{key}_1", f"{key}_2"])
        
        for up in updates:
            self.info_data[up] = "label"
        
        self.data = self.data.dropna(axis=1, how='any')


        y = self.data[self.target]
        X = self.data.filter(self.info_data.keys(), axis=1)

        for key in self.info_data:

            if self.info_data[key] == "label":
                encoder = Encoder(X[key], is_train=True)
                X[key] = encoder.apply()

        split = SplitDataset(X, y)
        X_train, X_test, y_train, y_test = split.apply()

        for key in self.info_data:

            if self.info_data[key] == "text":
                tfidf = TFIDF(X_train, key, is_train=True)
                X_train = tfidf.apply()

                tfidf.is_train = False
                tfidf.data = X_test
                X_test = tfidf.apply()
        
        return X_train, X_test, y_train, y_test
