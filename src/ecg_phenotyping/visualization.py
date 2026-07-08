"""Plotting helpers for phenotype analysis."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


def plot_pca(x_scaled, labels, ax=None):
    """Create a 2-D PCA scatter plot colored by cluster labels."""

    ax = ax or plt.gca()
    points = PCA(n_components=2, random_state=42).fit_transform(x_scaled)
    sns.scatterplot(x=points[:, 0], y=points[:, 1], hue=labels, palette="tab10", ax=ax)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title("PCA visualization of ECG-lifestyle phenotypes")
    return ax


def plot_tsne(x_scaled, labels, perplexity: int = 20, ax=None):
    """Create a 2-D t-SNE scatter plot colored by cluster labels."""

    ax = ax or plt.gca()
    points = TSNE(n_components=2, perplexity=perplexity, init="pca", learning_rate="auto").fit_transform(x_scaled)
    sns.scatterplot(x=points[:, 0], y=points[:, 1], hue=labels, palette="tab10", ax=ax)
    ax.set_xlabel("t-SNE 1")
    ax.set_ylabel("t-SNE 2")
    ax.set_title("t-SNE visualization of ECG-lifestyle phenotypes")
    return ax


def plot_feature_heatmap(df: pd.DataFrame, feature_cols: list[str], ax=None):
    """Plot a correlation heatmap for selected ECG/lifestyle features."""

    ax = ax or plt.gca()
    corr = df[feature_cols].corr()
    sns.heatmap(corr, cmap="coolwarm", center=0, square=True, ax=ax)
    ax.set_title("Feature correlation heatmap")
    return ax
