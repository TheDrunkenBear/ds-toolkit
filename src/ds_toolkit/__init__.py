"""ds-toolkit: tools for data analytics, scoring modeling and model validation."""

from ds_toolkit.data import Dataset, DatasetConfig, split_train_test_oot
from ds_toolkit.feature_selection import (
    BaseFeatureSelection,
    VarianceInflationFactor,
)

__version__ = "0.1.0"

__all__ = (
    "Dataset",
    "DatasetConfig",
    "split_train_test_oot",
    "BaseFeatureSelection",
    "VarianceInflationFactor",
    "__version__",
)
