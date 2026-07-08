"""Lifestyle feature engineering helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd


def add_bmi_category(
    df: pd.DataFrame,
    bmi_col: str = "BMI",
    output_col: str = "bmi_category",
) -> pd.DataFrame:
    """Add WHO-style BMI categories."""

    out = df.copy()
    bins = [-np.inf, 18.5, 25.0, 30.0, np.inf]
    labels = ["underweight", "normal", "overweight", "obese"]
    out[output_col] = pd.cut(out[bmi_col], bins=bins, labels=labels)
    return out


def add_mvpa_category(
    df: pd.DataFrame,
    mvpa_col: str = "mvpa_minutes",
    threshold: float = 150.0,
    output_col: str = "activity_group",
) -> pd.DataFrame:
    """Classify subjects by weekly moderate-to-vigorous physical activity."""

    out = df.copy()
    out[output_col] = np.where(out[mvpa_col] >= threshold, "active", "inactive")
    return out


def merge_ecg_lifestyle(
    ecg_features: pd.DataFrame,
    lifestyle: pd.DataFrame,
    subject_col: str = "File Name",
) -> pd.DataFrame:
    """Merge ECG-derived features with lifestyle variables."""

    return pd.merge(ecg_features, lifestyle, on=subject_col, how="inner")
