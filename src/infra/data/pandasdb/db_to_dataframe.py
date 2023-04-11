from domain.models.movie import Movie
from dataclasses import dataclass
from typing import List
import pandas as pd


@dataclass
class DBToDataframe:

    @staticmethod
    def convert(db: List[Movie]) -> pd.DataFrame:
        return pd.DataFrame.from_records([movie.to_dict() for movie in db])
