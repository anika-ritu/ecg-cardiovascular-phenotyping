"""Supervised phenotype prediction models."""

from __future__ import annotations

import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def linear_model_suite(random_state: int = 42) -> dict[str, Pipeline]:
    """Return the linear classifiers used for lifestyle-based prediction."""

    return {
        "logistic_regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=5000, random_state=random_state)),
            ]
        ),
        "lda": Pipeline([("scaler", StandardScaler()), ("model", LinearDiscriminantAnalysis())]),
        "linear_svm": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", SVC(kernel="linear", probability=True, random_state=random_state)),
            ]
        ),
    }


def train_linear_models(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str = "cluster",
    n_splits: int = 5,
    random_state: int = 42,
) -> pd.DataFrame:
    """Evaluate linear phenotype-prediction models with stratified CV."""

    x = df[feature_cols]
    y = df[target_col]
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    rows = []
    for name, model in linear_model_suite(random_state).items():
        pred = cross_val_predict(model, x, y, cv=cv)
        row = {
            "model": name,
            "accuracy": float(accuracy_score(y, pred)),
            "f1_macro": float(f1_score(y, pred, average="macro")),
        }
        if len(set(y)) == 2:
            proba = cross_val_predict(model, x, y, cv=cv, method="predict_proba")[:, 1]
            row["roc_auc"] = float(roc_auc_score(y, proba))
        rows.append(row)

    return pd.DataFrame(rows)
