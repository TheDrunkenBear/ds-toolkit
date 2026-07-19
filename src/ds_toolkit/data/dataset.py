from dataclasses import dataclass, field

import pandas as pd


@dataclass
class DatasetConfig:
    target_columns: list[str]
    id_column: str | None = None
    date_column: str | None = None
    exclude_columns: list[str] = field(default_factory=list)


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
        if not self.target_columns:
            raise ValueError("target_columns must not be empty")

        columns = set(self.sample.columns)
        available = list(self.sample.columns)

        if self.id_column is not None and self.id_column not in columns:
            raise ValueError(
                f"id_column='{self.id_column}' not found. "
                f"Available columns: {available}"
            )

        if self.date_column is not None and self.date_column not in columns:
            raise ValueError(
                f"date_column='{self.date_column}' not found. "
                f"Available columns: {available}"
            )

        missing_target_columns = [
            col for col in self.target_columns if col not in columns
        ]
        if missing_target_columns:
            raise ValueError(
                f"target_columns not found: {missing_target_columns}. "
                f"Available columns: {available}"
            )

    @property
    def features(self) -> list[str]:
        excluded_columns = set(self.target_columns) | set(self.exclude_columns)

        if self.id_column is not None:
            excluded_columns.add(self.id_column)

        if self.date_column is not None:
            excluded_columns.add(self.date_column)

        return [
            col for col in self.sample.columns if col not in excluded_columns
        ]
