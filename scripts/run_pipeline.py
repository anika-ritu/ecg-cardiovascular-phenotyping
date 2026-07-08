"""Run the ECG-lifestyle cardiovascular phenotyping pipeline.

Example:
    python scripts/run_pipeline.py --data-dir data --results-dir results
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ecg_phenotyping.config import PipelineConfig
from ecg_phenotyping.pipeline import run_phenotyping_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ECG-lifestyle phenotyping pipeline.")
    parser.add_argument("--data-dir", type=Path, default=Path("data"), help="Local data directory.")
    parser.add_argument("--results-dir", type=Path, default=Path("results"), help="Output directory.")
    parser.add_argument("--n-clusters", type=int, default=2, help="Number of K-means phenotype clusters.")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = PipelineConfig(
        data_dir=args.data_dir,
        results_dir=args.results_dir,
        n_clusters=args.n_clusters,
        random_state=args.random_state,
    )
    outputs = run_phenotyping_pipeline(config)
    print("Pipeline completed. Output tables:")
    for name, table in outputs.items():
        print(f"- {name}: {table.shape[0]} rows x {table.shape[1]} columns")


if __name__ == "__main__":
    main()
