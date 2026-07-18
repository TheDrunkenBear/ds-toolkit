from abc import ABC, abstractmethod

import pandas as pd
from matplotlib.axes import Axes

from ds_toolkit.data import Dataset


class BaseFeatureSelection(ABC):
    """Common interface for feature-selection diagnostics."""

    @classmethod
    @abstractmethod
    def report(cls, dataset: Dataset) -> pd.DataFrame:
        """Return a per-feature diagnostic report."""

    @classmethod
    @abstractmethod
    def visualization(cls, dataset: Dataset) -> Axes:
        """Render the diagnostic as a matplotlib Axes."""
