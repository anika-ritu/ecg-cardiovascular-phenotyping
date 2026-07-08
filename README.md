# ECG-Lifestyle Cardiovascular Phenotyping

Code for ECG-derived cardiovascular phenotype analysis and lifestyle-based phenotype prediction in young adults.

This repository supports the following conference manuscripts which are under review:

1. **Interpretable Lifestyle-Based Prediction of ECG-Derived Cardiovascular Phenotypes**  
   IEEE International Conference on Signal Processing, Information, Communication and Systems (SPICSCON), 2026

2. **Unsupervised ECG-Lifestyle Clustering for Early Cardiovascular Phenotyping in Young Adults**  
   IEEE International Conference on Signal Processing, Information, Communication and Systems (SPICSCON), 2026

The repository is a **code-only release**. Raw ECG recordings, lifestyle questionnaire data, intermediate spreadsheets, and participant-level outputs are not included.

## What this code does

The workflow combines short-duration resting ECG recordings with lifestyle variables to study early cardiovascular phenotypes among young adults. It includes:

- ECG filtering with Butterworth bandpass and 50 Hz notch filters
- signal-quality metrics before and after filtering
- R-peak and fiducial-point based ECG feature extraction
- HRV, amplitude, interval, and morphology features
- lifestyle feature preparation, including MVPA, BMI, diet, and sleep indicators
- correlation-based feature screening
- K-means clustering for phenotype discovery
- PCA, t-SNE, elbow, and silhouette diagnostics
- supervised phenotype prediction with Logistic Regression, LDA, and linear SVM
- SHAP-based interpretation of lifestyle-driven phenotype prediction
- statistical comparison of ECG-derived phenotypes across lifestyle groups

## Repository structure

```text
.
|-- src/
|   `-- ecg_phenotyping/
|       |-- __init__.py
|       |-- config.py
|       |-- preprocessing.py
|       |-- features.py
|       |-- lifestyle.py
|       |-- clustering.py
|       |-- modeling.py
|       |-- pipeline.py
|       |-- statistics.py
|       `-- visualization.py
|-- scripts/
|   `-- run_pipeline.py
|-- notebooks/
|   `-- ECG_MSC_Final_cleaned.ipynb
|-- data/
|   `-- README.md
|-- results/
|   `-- README.md
|-- docs/
|   `-- publication_notes.md
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Data availability

No dataset is distributed with this repository.

To reproduce the full analyses, place approved anonymized files locally under `data/` using the layout described in [`data/README.md`](data/README.md). The `.gitignore` file is configured to prevent accidental publication of common data formats such as `.csv`, `.xlsx`, `.mat`, `.npy`, and raw signal files.

## Installation

```bash
git clone https://github.com/anika-ritu/ecg-cardiovascular-phenotyping.git
cd ecg-cardiovascular-phenotyping
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Recommended Python version: 3.10 or newer.

## Usage

The repository provides two complementary entry points.

### 1. Modular pipeline

```text
scripts/run_pipeline.py
```

This script gives a clean public-facing pipeline for approved local data:

```bash
python scripts/run_pipeline.py --data-dir data --results-dir results
```

It expects local, non-public input files under `data/processed/` and writes generated outputs under `results/`. Because the participant-level dataset is not distributed, the script is intentionally data-path driven rather than bundled with example participant files.

### 2. Cleaned research notebook

```text
notebooks/ECG_MSC_Final_cleaned.ipynb
```

The notebook preserves the fuller thesis/conference workflow for transparency, including preprocessing, feature extraction, lifestyle integration, clustering, explainability, supervised prediction, visualization, and statistical analyses.

Reusable functions are organized under `src/ecg_phenotyping/`. Example imports:

```python
from ecg_phenotyping.preprocessing import preprocess_ecg
from ecg_phenotyping.features import extract_ecg_features
from ecg_phenotyping.pipeline import run_phenotyping_pipeline
from ecg_phenotyping.clustering import run_kmeans
from ecg_phenotyping.modeling import train_linear_models
```

Because the research data are not public, the repository does not include a one-command reproduction script with bundled inputs. The modules are written so approved local data can be connected without changing the public code release.

## Citation

If you use this repository, please cite the associated SPICSCON 2026 manuscripts once the final citation details are available.

## Author

Anika Tasnim Ritu  
Rajshahi University of Engineering & Technology (RUET)  
Website: https://anika-ritu.github.io/  
Google Scholar: https://scholar.google.com/citations?user=vV4l_o4AAAAJ&hl=en  
ORCID: https://orcid.org/0009-0009-7367-4712
