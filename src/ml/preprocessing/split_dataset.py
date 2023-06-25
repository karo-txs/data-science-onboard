from sklearn.model_selection import train_test_split
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class SplitDataset:
    X: pd.DataFrame
    y: pd.DataFrame
    test_size: float = field(default=0.2)
    
    def apply(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=self.test_size, random_state=42)
        return X_train, X_test, y_train, y_test