from sklearn.feature_extraction.text import TfidfVectorizer
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class TFIDF:
    data: pd.DataFrame
    is_train: bool = field(default=True)
    tfidf_vectorizer: TfidfVectorizer = field(default=None)


    def apply(self):
        if self.is_train:
            self.tfidf_vectorizer = TfidfVectorizer(analyzer='word' , stop_words='english',)
            self.tfidf_vectorizer.fit(self.train)
        
        return self.tfidf_vectorizer.transform(self.data)
