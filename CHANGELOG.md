# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-07-19

### Added
- `Dataset` and `DatasetConfig` for wrapping a scoring sample with target, id
  and date metadata, input validation and automatic feature resolution.
- `split_train_test_oot` for train / test / out-of-time splitting.
- `VarianceInflationFactor` multicollinearity diagnostic with a per-feature
  report and a visualization.
- Public API and `__version__` re-exported from the package root.
- Packaging metadata, runtime dependencies and a build-system section in
  `pyproject.toml`; a `dev` optional-dependencies group (pytest, ruff).
- `.gitattributes` enforcing LF line endings.
- GitHub Actions CI running ruff and pytest on push and pull requests.
- `README.md`, `CHANGELOG.md` and an MIT `LICENSE`.

### Changed
- `BaseFeatureSelection` abstract methods are now classmethods matching the
  concrete `(cls, dataset)` signatures; the empty `__init__` was removed.
- `VarianceInflationFactor` imports `BaseFeatureSelection` directly from the
  `base` module instead of the package root, removing a fragile import order.

### Fixed
- `split_train_test_oot` now resolves the `stratify` column name to a label
  array before delegating to `train_test_split`; previously the column name
  string was passed through, silently breaking stratification.

[Unreleased]: https://github.com/TheDrunkenBear/ds-toolkit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/TheDrunkenBear/ds-toolkit/releases/tag/v0.1.0
