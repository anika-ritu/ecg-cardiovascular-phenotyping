# Data folder

This folder is intentionally kept empty in the public repository.

The ECG recordings, lifestyle questionnaire files, merged feature tables, and participant-level analysis outputs are not distributed. If you have approved access to the data, use a local layout such as:

```text
data/
├── raw_ecg/          # raw or segmented ECG files
├── lifestyle/        # lifestyle questionnaire / derived lifestyle variables
├── processed/        # extracted ECG features and merged analysis tables
└── README.md
```

The public `.gitignore` blocks common dataset formats, including `.csv`, `.xlsx`, `.mat`, `.npy`, `.npz`, `.pkl`, `.h5`, and raw signal files, to reduce the risk of accidentally publishing research data.
