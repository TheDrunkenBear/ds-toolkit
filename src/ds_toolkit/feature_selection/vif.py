import warnings

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

from ds_toolkit.data import Dataset
from ds_toolkit.feature_selection.base import BaseFeatureSelection


class VarianceInflationFactor(BaseFeatureSelection):

    STATUS_COLORS = {
        "ok": "#457b9d",
        "warning": "#f4a261",
        "high": "#e76f51",
    }

    @classmethod
    def report(cls, dataset: Dataset) -> pd.DataFrame:
        features = dataset.features
        numeric = dataset.sample[features].select_dtypes(include="number")

        skipped = [col for col in features if col not in numeric.columns]
        if skipped:
            warnings.warn(
                f"VIF skips non-numeric features: {skipped}",
                stacklevel=2,
            )

        if numeric.shape[1] < 2:
            raise ValueError("VIF requires at least two numeric features")

        # variance_inflation_factor cannot handle missing values, so drop any
        # row that is not complete across the numeric features.
        clean = numeric.dropna()
        dropped_rows = len(numeric) - len(clean)
        if dropped_rows:
            warnings.warn(
                f"VIF drops {dropped_rows} row(s) with missing values",
                stacklevel=2,
            )
        if clean.empty:
            raise ValueError("No complete rows left to compute VIF")

        # variance_inflation_factor expects a design matrix that includes a
        # constant; without an intercept the VIF values are distorted.
        design = add_constant(clean, has_constant="add")

        report = pd.DataFrame({
            "feature": clean.columns,
            "vif": [
                variance_inflation_factor(
                    design.values, design.columns.get_loc(col)
                )
                for col in clean.columns
            ],
        })

        report["status"] = pd.cut(
            report["vif"],
            bins=[-float("inf"), 5, 10, float("inf")],
            labels=["ok", "warning", "high"],
        )

        return report.sort_values("vif", ascending=False).reset_index(drop=True)

    @classmethod
    def visualization(cls, dataset: Dataset) -> Axes:
        report = cls.report(dataset).sort_values("vif")

        fig, ax = plt.subplots(
            figsize=(10, 4)
        )

        ax.barh(
            report["feature"],
            report["vif"],
            color=report["status"].astype(str).map(cls.STATUS_COLORS),
            alpha=0.5,
            linewidth=1,
        )

        ax.axvline(5, color="#f4a261", ls="--", linewidth=1.25)
        ax.axvline(10, color="#e76f51", ls="--", linewidth=1.25)

        ax.set_title("Variance Inflation Factor")
        ax.set_xlabel("VIF")
        ax.set_ylabel("Feature")

        plt.tight_layout()

        return ax
