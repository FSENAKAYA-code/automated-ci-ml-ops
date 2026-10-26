"""Small data-contract checks safe to run before model training."""

from collections.abc import Sequence


def validate_feature_labels(features: Sequence[object], labels: Sequence[object]) -> None:
    if len(features) == 0 or len(features) != len(labels):
        raise ValueError("features and labels must be non-empty and aligned")
    if any(label is None for label in labels):
        raise ValueError("labels cannot contain null values")


def validate_disjoint_ids(train_ids: set[str], validation_ids: set[str], test_ids: set[str]) -> None:
    if not train_ids or not validation_ids or not test_ids:
        raise ValueError("all data partitions must be non-empty")
    if train_ids & validation_ids or train_ids & test_ids or validation_ids & test_ids:
        raise ValueError("record identifiers overlap across data partitions")
