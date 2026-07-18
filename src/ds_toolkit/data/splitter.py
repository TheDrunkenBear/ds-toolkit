from typing import Tuple
from sklearn.model_selection import train_test_split

from ds_toolkit.data.dataset import Dataset


def split_train_test_oot(
        dataset: Dataset,
        *,
        train_size: float | None = None,
        test_size: float | None = 0.3,
        oot_size: float | None = None,
        random_state: int = 42,
        shuffle: bool = True,
        stratify: str | None = None,
) -> Tuple[Dataset, Dataset, Dataset | None]:
    sample = dataset.sample.copy()

    oot = None

    if oot_size is not None:
        if dataset.date_column is None:
            raise ValueError("oot_size requires date_column")

        if not 0 < oot_size < 1:
            raise ValueError("oot_size must be between 0 and 1")

        sample = sample.sort_values(by=dataset.date_column, ascending=False)

        oot_index_split = int(len(sample) * oot_size)

        oot_sample = sample.iloc[:oot_index_split].copy()
        sample = sample.iloc[oot_index_split:].copy()

        oot = Dataset(
            oot_sample.assign(sample_type="oot"),
            config=dataset.config,
        )

    if stratify is not None and stratify not in sample.columns:
        raise ValueError(f"stratify column '{stratify}' not found")

    stratify_values = sample[stratify] if stratify is not None else None

    train, test = train_test_split(
        sample,
        test_size=test_size,
        train_size=train_size,
        random_state=random_state,
        shuffle=shuffle,
        stratify=stratify_values,
    )

    return (
        Dataset(train.assign(sample_type="train"), config=dataset.config),
        Dataset(test.assign(sample_type="test"), config=dataset.config),
        oot,
    )
