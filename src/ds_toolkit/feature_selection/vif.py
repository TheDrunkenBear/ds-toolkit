import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from statsmodels.stats.outliers_influence import variance_inflation_factor

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
        x = dataset.sample[dataset.features]
        x = x.select_dtypes(include="number")

        if x.shape[1] < 2:
            raise ValueError("VIF requires at least two numeric features")

        report = pd.DataFrame({
            "feature": x.columns,
            "vif": [
                variance_inflation_factor(x.values, i)
                for i in range(x.shape[1])
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
