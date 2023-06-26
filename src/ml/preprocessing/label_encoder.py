from dataclasses import dataclass, field
from sklearn import preprocessing
import pandas as pd


@dataclass
class Encoder:
    data: pd.DataFrame
    is_train: bool = field(default=True)
    label_encoder: preprocessing.LabelEncoder = field(default=None)


    def apply(self):
        if self.is_train:
            self.label_encoder = preprocessing.LabelEncoder()
            self.label_encoder.fit(self.data)
        
        return self.label_encoder.transform(self.data)
