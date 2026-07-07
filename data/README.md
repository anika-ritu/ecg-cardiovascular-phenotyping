# Data instructions

Do not commit participant-level raw ECG or lifestyle data unless it has been approved for sharing and fully anonymized.

Expected inputs used by the cleaned notebook include:

- Raw ECG Excel files
- Extracted ECG feature table, e.g. `advanced_features_1.xlsx`
- Lifestyle table with BMI/MVPA/diet/sleep variables
- Merged lifestyle plus ECG feature table, e.g. `merged_lifestyle_features_n.csv`

Recommended private local structure:

```text
data/
├── raw/
│   └── subject ECG files
├── processed/
│   ├── advanced_features_1.xlsx
│   └── merged_lifestyle_features_n.csv
└── private/
    └── non-shareable source data
```

Before public release, replace absolute Google Drive paths in the notebook with relative paths pointing to this folder.
