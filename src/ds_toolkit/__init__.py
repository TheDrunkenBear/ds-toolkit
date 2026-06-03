from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class DatasetConfig:
    target_columns: List[str]
    id_column: str | None = None
    date_column: str | None = None


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

        self._validate_input()

    def _validate_input(self) -> None:
        """Validate the input data."""
        if (
            self.id_column is not None
            and self.id_column not in self.df.columns
        ):
            raise ValueError(
                f"id_column='{self.id_column}' not found"
            )

        if (
            self.date_column is not None
            and self.date_column not in self.df.columns
        ):
            raise ValueError(
                f"date_column='{self.date_column}' not found"
            )

        missing_target_columns = [
            col
            for col in self.target_columns
            if col not in self.df.columns
        ]

        if missing_target_columns:
            raise ValueError(
                f"target_columns not found: {missing_target_columns}"
            )

        if not self.target_columns:
            raise ValueError(
                "target_columns must not be empty"
            )

    @property
    def features(self) -> List[str]:

        excluded_columns = list(self.target_columns)

        if self.id_column is not None:
            excluded_columns.append(self.id_column)

        if self.date_column is not None:
            excluded_columns.append(self.date_column)

        return [
            col
            for col in self.df.columns
            if col not in excluded_columns
        ]
