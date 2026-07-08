"""Unsupervised ECG-lifestyle phenotype discovery."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler


def scale_features(df: pd.DataFrame, feature_cols: list[str]) -> tuple[np.ndarray, StandardScaler]:
    """Standardize selected features for clustering or linear modeling."""

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(df[feature_cols])
    return x_scaled, scaler


def run_kmeans(
    df: pd.DataFrame,
    feature_cols: list[str],
    n_clusters: int = 2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, KMeans, StandardScaler]:
    """Run K-means clustering and append cluster labels."""

    x_scaled, scaler = scale_features(df, feature_cols)
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=20)
    labels = model.fit_predict(x_scaled)

    out = df.copy()
    out["cluster"] = labels
    return out, model, scaler


def clustering_diagnostics(
    x_scaled: np.ndarray,
    min_k: int = 2,
    max_k: int = 8,
    random_state: int = 42,
) -> pd.DataFrame:
    """Compute elbow, silhouette, and Davies-Bouldin diagnostics."""

    rows = []
    for k in range(min_k, max_k + 1):
        model = KMeans(n_clusters=k, random_state=random_state, n_init=20)
        labels = model.fit_predict(x_scaled)
        rows.append(
            {
                "k": k,
                "inertia": float(model.inertia_),
                "silhouette": float(silhouette_score(x_scaled, labels)),
                "davies_bouldin": float(davies_bouldin_score(x_scaled, labels)),
            }
        )
    return pd.DataFrame(rows)
