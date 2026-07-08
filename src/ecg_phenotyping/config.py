"""Configuration objects for the public ECG-lifestyle pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    """Local path and analysis settings.

    The repository is code-only, so these paths point to files that must be
    supplied locally by users with approved access to the anonymized data.
    """

    data_dir: Path = Path("data")
    results_dir: Path = Path("results")
    ecg_feature_file: str = "processed/ecg_features.csv"
    lifestyle_file: str = "processed/lifestyle_features.csv"
    merged_file: str = "processed/merged_ecg_lifestyle.csv"
    subject_col: str = "File Name"
    target_col: str = "cluster"
    n_clusters: int = 2
    random_state: int = 42

    @property
    def ecg_feature_path(self) -> Path:
        return self.data_dir / self.ecg_feature_file

    @property
    def lifestyle_path(self) -> Path:
        return self.data_dir / self.lifestyle_file

    @property
    def merged_path(self) -> Path:
        return self.data_dir / self.merged_file

    def ensure_results_dir(self) -> Path:
        self.results_dir.mkdir(parents=True, exist_ok=True)
        return self.results_dir
