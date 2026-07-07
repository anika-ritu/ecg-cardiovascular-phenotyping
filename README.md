# ECG-Derived Cardiovascular Phenotyping

This repository contains the cleaned research code for Anika Tasnim Ritu's M.Sc. thesis work on ECG-derived cardiovascular phenotyping and lifestyle-associated cardiovascular profiles in young adults.

The code was cleaned from the original thesis notebook and organized for private review/reproducibility. The related conference manuscripts are not accepted yet, so this repository should remain **private** until the work is accepted or the author decides what can be released publicly.

## Project summary

The analysis uses short-duration resting ECG recordings and lifestyle variables to study cardiovascular phenotypes among young adults. The workflow includes:

- ECG preprocessing using Butterworth bandpass filtering and 50 Hz notch filtering
- ECG signal-quality assessment before and after filtering
- Fiducial point detection and ECG feature extraction
- HRV, amplitude-based, interval-based, and morphology-based feature computation
- Correlation-based feature selection
- Lifestyle variable engineering, including MVPA, BMI, diet score, and sleep quality
- K-means clustering for phenotype discovery
- PCA, t-SNE, elbow, and silhouette analyses for cluster interpretation
- Supervised phenotype prediction using Logistic Regression, LDA, and linear SVM
- SHAP-based explainability for lifestyle-based phenotype prediction
- Statistical comparisons across activity, BMI, sleep, diet, and cluster groups

## Repository structure

```text
.
├── notebooks/
│   └── ECG_MSC_Final_cleaned.ipynb
├── data/
│   └── README.md
├── results/
│   └── README.md
├── CLEANUP_REPORT.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Notebook

The cleaned notebook is:

```text
notebooks/ECG_MSC_Final_cleaned.ipynb
```

Cleaning summary:

- Original notebook: 90 cells, about 29.5 MB
- Cleaned notebook: 49 cells, about 149 KB
- Kept final/relevant code cells: 38
- Removed old/debug/duplicate cells: 52
- Removed embedded notebook outputs for GitHub cleanliness

See `CLEANUP_REPORT.md` for the detailed keep/remove decision for each original cell.

## Data availability

Raw ECG recordings and lifestyle data are not included in this repository because they may contain participant-level research data. To reproduce the analysis, place approved/anonymized data in the `data/` folder following the instructions in `data/README.md`.

The current notebook still contains some original Google Colab/Drive paths such as `/content/drive/...`. Before public release, these paths should be converted to relative paths such as:

```python
DATA_DIR = "../data"
RESULTS_DIR = "../results"
```

## Installation

Create a Python environment and install the required packages:

```bash
pip install -r requirements.txt
```

Recommended Python version: 3.10 or newer.

## Main dependencies

- numpy
- pandas
- scipy
- scikit-learn
- matplotlib
- seaborn
- statsmodels
- shap
- scikit-image
- openpyxl

## Reproducibility notes

The repository currently provides a cleaned notebook. The next recommended step is to refactor the workflow into scripts:

```text
src/preprocessing.py
src/features.py
src/clustering.py
src/classification.py
src/statistics.py
```

This would make the work easier to run, test, and cite.

## Status

Private research repository. Related conference manuscripts are not accepted yet.

## Author

Anika Tasnim Ritu  
Rajshahi University of Engineering & Technology (RUET)  
Website: https://anika-ritu.github.io/  
Google Scholar: https://scholar.google.com/citations?user=vV4l_o4AAAAJ&hl=en  
ORCID: https://orcid.org/0009-0009-7367-4712
