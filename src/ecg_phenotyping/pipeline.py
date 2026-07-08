"""Public pipeline wrapper for ECG-lifestyle cardiovascular phenotyping.

This module connects the reusable project functions into a complete analysis
flow while keeping data local. It does not ship any participant-level data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .clustering import clustering_diagnostics, run_kmeans, scale_features
from .config import PipelineConfig
from .lifestyle import merge_ecg_lifestyle
from .modeling import train_linear_models
from .statistics import compare_two_groups


DEFAULT_ECG_FEATURES = [
    "Heart Rate",
    "SDNN",
    "RMSSD",
    "pNN50",
    "RMS Amp.",
    "Mean R Amp.",
    "R-Q Amp. Diff.",
    "R-S Amp. Diff.",
    "QRS Dur.",
]

DEFAULT_LIFESTYLE_FEATURES = [
    "mvpa_minutes",
    "BMI",
    "diet_score",
    "sleep_quality",
]


def _available_columns(df: pd.DataFrame, requested: list[str]) -> list[str]:
    """Return requested columns that are present in a dataframe."""

    return [col for col in requested if col in df.columns]


def load_or_merge_features(config: PipelineConfig) -> pd.DataFrame:
    """Load merged features, or merge ECG and lifestyle feature files locally."""

    if config.merged_path.exists():
        return pd.read_csv(config.merged_path)

    if not config.ecg_feature_path.exists() or not config.lifestyle_path.exists():
        raise FileNotFoundError(
            "No local merged feature table found. Provide either "
            f"{config.merged_path} or both {config.ecg_feature_path} and "
            f"{config.lifestyle_path}. No data files are included in this public repo."
        )

    ecg_features = pd.read_csv(config.ecg_feature_path)
    lifestyle = pd.read_csv(config.lifestyle_path)
    return merge_ecg_lifestyle(ecg_features, lifestyle, subject_col=config.subject_col)


def run_phenotyping_pipeline(
    config: PipelineConfig,
    clustering_features: list[str] | None = None,
    prediction_features: list[str] | None = None,
) -> dict[str, pd.DataFrame]:
    """Run the public ECG-lifestyle phenotype analysis pipeline.

    Returns the main result tables and writes CSV outputs under `results/`.
    """

    results_dir = config.ensure_results_dir()
    data = load_or_merge_features(config)

    clustering_features = clustering_features or _available_columns(data, DEFAULT_ECG_FEATURES + DEFAULT_LIFESTYLE_FEATURES)
    if len(clustering_features) < 2:
        raise ValueError("At least two available clustering features are required.")

    clustered, kmeans_model, scaler = run_kmeans(
        data,
        feature_cols=clustering_features,
        n_clusters=config.n_clusters,
        random_state=config.random_state,
    )
    clustered.to_csv(results_dir / "cluster_assignments.csv", index=False)

    x_scaled, _ = scale_features(data, clustering_features)
    diagnostics = clustering_diagnostics(x_scaled, min_k=2, max_k=8, random_state=config.random_state)
    diagnostics.to_csv(results_dir / "cluster_diagnostics.csv", index=False)

    centers = pd.DataFrame(kmeans_model.cluster_centers_, columns=clustering_features)
    centers.to_csv(results_dir / "cluster_centers_scaled.csv", index=False)

    prediction_features = prediction_features or _available_columns(clustered, DEFAULT_LIFESTYLE_FEATURES)
    model_scores = pd.DataFrame()
    if len(prediction_features) >= 2 and config.target_col in clustered.columns:
        model_scores = train_linear_models(
            clustered,
            feature_cols=prediction_features,
            target_col=config.target_col,
            random_state=config.random_state,
        )
        model_scores.to_csv(results_dir / "phenotype_prediction_scores.csv", index=False)

    stats_tables = []
    if "activity_group" in clustered.columns:
        groups = list(clustered["activity_group"].dropna().unique())
        if len(groups) >= 2:
            stats_tables.append(
                compare_two_groups(
                    clustered,
                    group_col="activity_group",
                    feature_cols=clustering_features,
                    group_a=groups[0],
                    group_b=groups[1],
                )
            )

    statistical_results = pd.concat(stats_tables, ignore_index=True) if stats_tables else pd.DataFrame()
    if not statistical_results.empty:
        statistical_results.to_csv(results_dir / "group_statistical_comparisons.csv", index=False)

    return {
        "clustered_data": clustered,
        "cluster_diagnostics": diagnostics,
        "cluster_centers_scaled": centers,
        "model_scores": model_scores,
        "statistical_results": statistical_results,
    }
