import pytest

from mlops.artifacts import write_metrics_artifact
from mlops.contracts import validate_disjoint_ids, validate_feature_labels
from mlops.publish import publish_all_branches


def test_contract_detects_split_leakage():
    with pytest.raises(ValueError, match="overlap"):
        validate_disjoint_ids({"a"}, {"b"}, {"a"})

def test_contract_accepts_aligned_values():
    validate_feature_labels([1, 2], [0, 1])


def test_publish_requires_explicit_confirmation(tmp_path):
    with pytest.raises(ValueError, match="--confirm"):
        publish_all_branches(tmp_path, "origin")


def test_metrics_artifact_is_local_json(tmp_path):
    artifact = write_metrics_artifact({"train_loss": 0.4, "test_f1": 0.8}, tmp_path / "metrics.json")
    assert '"test_f1": 0.8' in artifact.read_text()
