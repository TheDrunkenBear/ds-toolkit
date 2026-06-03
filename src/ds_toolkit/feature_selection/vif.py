import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

from ds_toolkit import DSToolkit
from ds_toolkit.feature_selection.base import BaseReport


class VIFReport(BaseReport):
    @classmethod
    def report(cls, toolkit: DSToolkit) -> pd.DataFrame:
        X = toolkit.sample[toolkit.features]
        X = X.select_dtypes(include="number")

        if X.shape[1] < 2:
            raise ValueError(
                "VIF requires at least two features selected"
            )

        return pd.DataFrame({
            "feature": X.columns,
            "vif": [
                variance_inflation_factor(X.values, i)
                for i in range(X.shape[1])
            ]
        }).sort_values("vif", ascending=False).reset_index(drop=True)

