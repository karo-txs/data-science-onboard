from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class TFIDF:
    data: pd.DataFrame
    key: str
    is_train: bool = field(default=True)
    tfidf_vectorizer: TfidfVectorizer = field(default=None)


    def apply(self):
        self.data[self.key] = self.data[self.key].str.replace('[^\w\s]', '').str.lower()
        self.data["tokens"] = self.data[self.key].apply(word_tokenize)
        docs = self.data["tokens"].apply(lambda tokens: ' '.join(tokens)).tolist()

        if self.is_train:
            self.tfidf_vectorizer = TfidfVectorizer(analyzer='word' , stop_words='english',)
            self.tfidf_vectorizer.fit(docs)
            
        result = self.tfidf_vectorizer.transform(docs)
        new_cols = self.tfidf_vectorizer.get_feature_names_out()

        result = pd.DataFrame(result.toarray(), columns=new_cols).reset_index(drop=True)

        self.data = self.data.drop(self.key, axis=1)
        self.data = self.data.drop("tokens", axis=1)
        self.data = self.data.reset_index(drop=True)
        self.data = pd.concat([self.data, result], axis=1)

        return self.data
