"""Local JSON and optional local-MLflow metric artifact logging."""

import json
import math
import os
import tempfile
from collections.abc import Mapping
from pathlib import Path


def write_metrics_artifact(metrics: Mapping[str, float], destination: Path) -> Path:
    if not metrics or any(not math.isfinite(float(value)) for value in metrics.values()):
        raise ValueError("metrics must be non-empty and finite")
    payload = {str(key): float(value) for key, value in metrics.items()}
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=destination.parent, delete=False
    ) as temporary:
        json.dump(payload, temporary, indent=2, sort_keys=True)
        temporary.write("\n")
        temp_path = Path(temporary.name)
    os.replace(temp_path, destination)
    return destination


def log_to_local_mlflow(metrics: Mapping[str, float], tracking_dir: Path) -> str:
    try:
        import mlflow
    except ImportError as exc:
        raise RuntimeError("install MLflow in the project uv environment") from exc
    tracking_dir.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(tracking_dir.resolve().as_uri())
    with mlflow.start_run() as run:
        mlflow.log_metrics({key: float(value) for key, value in metrics.items()})
        return run.info.run_id
