"""Statistical comparison helpers for ECG-lifestyle analyses."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, ttest_ind
from statsmodels.stats.multitest import multipletests


def cohens_d(group_a: pd.Series, group_b: pd.Series) -> float:
    """Compute Cohen's d for two independent groups."""

    a = pd.Series(group_a).dropna().astype(float)
    b = pd.Series(group_b).dropna().astype(float)
    pooled_n = len(a) + len(b) - 2
    if pooled_n <= 0:
        return np.nan
    pooled_sd = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / pooled_n)
    return float((a.mean() - b.mean()) / pooled_sd) if pooled_sd else np.nan


def compare_two_groups(
    df: pd.DataFrame,
    group_col: str,
    feature_cols: list[str],
    group_a,
    group_b,
    method: str = "mannwhitney",
    correction: str = "fdr_bh",
) -> pd.DataFrame:
    """Compare numeric features between two groups with multiple-test correction."""

    rows = []
    a_df = df[df[group_col] == group_a]
    b_df = df[df[group_col] == group_b]

    for col in feature_cols:
        a = a_df[col].dropna()
        b = b_df[col].dropna()
        if method == "ttest":
            stat, p_value = ttest_ind(a, b, equal_var=False)
        else:
            stat, p_value = mannwhitneyu(a, b, alternative="two-sided")
        rows.append(
            {
                "feature": col,
                "group_a": group_a,
                "group_b": group_b,
                "statistic": float(stat),
                "p_value": float(p_value),
                "cohens_d": cohens_d(a, b),
            }
        )

    result = pd.DataFrame(rows)
    if not result.empty:
        result["p_adjusted"] = multipletests(result["p_value"], method=correction)[1]
    return result
