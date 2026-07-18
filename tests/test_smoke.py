"""Smoke tests. The full suite is added in a later change."""


def test_version_is_exposed():
    import ds_toolkit

    assert isinstance(ds_toolkit.__version__, str)
    assert ds_toolkit.__version__


def test_public_api_is_importable():
    from ds_toolkit import (  # noqa: F401
        BaseFeatureSelection,
        Dataset,
        DatasetConfig,
        VarianceInflationFactor,
        split_train_test_oot,
    )
