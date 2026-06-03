from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class DatasetConfig:
    date_column: str
    target_columns: List[str]


class DSToolkit:
    def __init__(
            self,
            df: pd.DataFrame,
            config: DatasetConfig,
    ):
        self.df = df.copy()
        self.date_column = config.date_column
        self.target_columns = config.target_columns

    @property
    def features(self) -> List[str]:

        excluded = [self.date_column] + self.target_columns

        return [
            col
            for col in self.df.columns
            if col not in excluded
        ]
