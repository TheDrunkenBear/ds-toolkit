# ds-toolkit

![CI](https://github.com/TheDrunkenBear/ds-toolkit/actions/workflows/ci.yml/badge.svg)

A personal suite of tools for data analytics, scoring modeling, and model
validation.

## Features

- **`Dataset` / `DatasetConfig`** — wrap a scoring sample together with its
  target, id and date metadata, validate the input, and resolve the list of
  feature columns automatically.
- **`split_train_test_oot`** — split a dataset into train / test and an
  optional out-of-time (OOT) hold-out based on a date column.
- **`VarianceInflationFactor`** — multicollinearity diagnostic that produces a
  per-feature VIF report and a ready-to-show visualization.

## Installation

```bash
git clone https://github.com/TheDrunkenBear/ds-toolkit.git
cd ds-toolkit
pip install -e .
```

For development (tests and linter):

```bash
pip install -e ".[dev]"
```

Requires Python 3.10+.

## Quickstart

```python
import pandas as pd
from ds_toolkit import Dataset, DatasetConfig, split_train_test_oot
from ds_toolkit import VarianceInflationFactor

data = pd.read_csv("notebooks/sample_scoring_dataset.csv")
data["date"] = pd.to_datetime(data["date"])

config = DatasetConfig(
    id_column="id",
    date_column="date",
    target_columns=["default"],
)
dataset = Dataset(data, config)

train, test, oot = split_train_test_oot(
    dataset, test_size=0.4, oot_size=0.15, stratify="default"
)

report = VarianceInflationFactor.report(dataset)
print(report)

VarianceInflationFactor.visualization(dataset)
```

See [`notebooks/example.ipynb`](notebooks/example.ipynb) for a full walkthrough.

## Project structure

```
ds-toolkit/
├── src/ds_toolkit/
│   ├── data/                 # Dataset, DatasetConfig, splitter
│   └── feature_selection/    # BaseFeatureSelection, VarianceInflationFactor
├── tests/                    # test suite
├── notebooks/                # usage examples and sample data
├── pyproject.toml            # packaging, dependencies, tooling
├── CHANGELOG.md
└── LICENSE
```

## Development

```bash
ruff check src tests     # lint
pytest                   # run tests
```

## License

Released under the [MIT License](LICENSE).
