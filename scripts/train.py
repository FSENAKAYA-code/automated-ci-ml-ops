"""Run a small deterministic demo; no external data is fetched."""

from pathlib import Path

from sklearn.datasets import make_classification

from mlops.artifacts import write_metrics_artifact
from mlops.experiment import run_experiment


def main() -> None:
    X, y = make_classification(
        n_samples=500, n_features=12, n_informative=8, random_state=42
    )
    metrics = run_experiment(X, y, random_state=42)
    artifact = write_metrics_artifact(metrics, Path("reports/metrics.json"))
    print(metrics)
    print(f"metrics_artifact={artifact}")


if __name__ == "__main__":
    main()
