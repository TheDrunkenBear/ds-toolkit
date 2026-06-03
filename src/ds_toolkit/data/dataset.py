from dataclasses import dataclass, field
from typing import List
import pandas as pd


@dataclass
class DatasetConfig:
    target_columns: List[str]
    id_column: str | None = None
    date_column: str | None = None
    exclude_columns: List[str] = field(default_factory=list)


class Dataset:
    def __init__(
            self,
            sample: pd.DataFrame,
            config: DatasetConfig,
    ):
        self.sample = sample.copy()
        self.config = config

        self.id_column = config.id_column
        self.date_column = config.date_column
        self.target_columns = config.target_columns
        self.exclude_columns = list(config.exclude_columns)

        if "sample_type" not in self.exclude_columns:
            self.exclude_columns.append("sample_type")

        self._validate_input()

    def _validate_input(self) -> None:
        """Validate the input data."""
        if (
            self.id_column is not None
            and self.id_column not in self.sample.columns
        ):
            raise ValueError(
                f"id_column='{self.id_column}' not found"
            )

        if (
            self.date_column is not None
            and self.date_column not in self.sample.columns
        ):
            raise ValueError(
                f"date_column='{self.date_column}' not found"
            )

        missing_target_columns = [
            col
            for col in self.target_columns
            if col not in self.sample.columns
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

        if self.exclude_columns is not None:
            excluded_columns.extend(self.exclude_columns)

        return [
            col
            for col in self.sample.columns
            if col not in excluded_columns
        ]