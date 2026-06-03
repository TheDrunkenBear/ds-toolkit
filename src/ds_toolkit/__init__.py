from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class DatasetConfig:
    id_column: str
    date_column: str
    target_columns: List[str]


class DSToolkit:
    def __init__(
            self,
            df: pd.DataFrame,
            config: DatasetConfig,
    ):
        self.df = df.copy()
        self.id_column = config.id_column
        self.date_column = config.date_column
        self.target_columns = config.target_columns

    def _validate_input(self) -> None:
        if not isinstance(self.df, pd.DataFrame):
            raise TypeError("df must be a pd.DataFrame")

        if self.date_column not in self.df.columns:
            raise ValueError("date_column must be in df.columns")

        missing_targets = [
            col for col in self.target_columns
            if col not in self.df.columns
        ]

        if missing_targets:
            raise ValueError(f"target_columns must not contain {missing_targets}")

        if len(self.target_columns) == 0:
            raise ValueError("target_columns must not be empty")

    @property
    def features(self) -> List[str]:

        excluded = [
           self.id_column,
           self.date_column
       ] + self.target_columns

        return [
            col
            for col in self.df.columns
            if col not in excluded
        ]
