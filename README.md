# Akkadian-to-English Machine Translation Project

## Overview

This project aims to build a machine learning system capable of translating Akkadian transliterations into English.

The task is inspired by the Deep Past Initiative Machine Translation Kaggle competition. The dataset consists of paired examples, where each input is a line of Akkadian text (in Latin transliteration) and each output is its corresponding English translation.

This is a challenging problem due to:
- the low-resource nature of Akkadian
- inconsistent and noisy transliterations
- multiple valid translations for a single input

---

## Objective

The goal of this project is not to build a model from scratch, but to:
- fine-tune pretrained transformer models on a specialized dataset  
- compare different modeling approaches  
- understand how preprocessing and model design affect translation quality  

---

## Approach

We implement and compare two transformer-based models:

### ByT5 (Primary Model)
- Byte-level model (no explicit tokenization)
- Robust to noisy and irregular text
- Main model for this project

### mT5 (Secondary Model)
- Token-based multilingual transformer
- Requires explicit tokenization
- Used for comparison

---

## Project Structure

```
akkadian-translation-project/
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── splits/
│
├── docs/
│   ├── project_plan.md
│   ├── data_notes.md
│   └── experiment_notes.md
│
├── notebooks/
│   ├── eda.ipynb
│   └── error_analysis.ipynb
│
├── src/
│   ├── data/
│   │   ├── preprocess.py
│   │   └── build_splits.py
│   │
│   ├── models/
│   │   ├── train_byt5.py
│   │   ├── train_mt5.py
│   │   └── predict.py
│   │
│   ├── evaluation/
│   │   └── metrics.py
│   │
│   └── utils/
│
├── outputs/
│   ├── checkpoints/
│   ├── predictions/
│   └── results/
│
└── configs/
    ├── byt5.yaml
    └── mt5.yaml
```

---

## Data

- `train.csv`: Akkadian → English pairs (used for training and validation)  
- `test.csv`: Akkadian inputs only (used for generating predictions)  

Raw data is stored in:

```
data/raw/
```

Processed data and splits are stored in:

```
data/processed/
data/splits/
```

---

## Pipeline

The project follows this pipeline:

1. Data exploration (EDA)  
2. Preprocessing and cleaning  
3. Train/validation split  
4. Model training (ByT5 and mT5)  
5. Prediction generation  
6. Evaluation using BLEU and chrF++  

---

## Evaluation

Model performance is evaluated using:
- BLEU score (word-level similarity)  
- chrF++ score (character-level similarity)  

Evaluation is performed locally using Python libraries (e.g., `sacrebleu` or `evaluate`).

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Preprocess data
```bash
python src/data/preprocess.py
```

### 3. Train ByT5 model
```bash
python src/models/train_byt5.py
```

### 4. Train mT5 model
```bash
python src/models/train_mt5.py
```

### 5. Evaluate models
```bash
python src/evaluation/metrics.py
```

---

## Team

- Data & Preprocessing: [Name]  
- ByT5 Model: [Name]  
- mT5 Model: [Name]  
- Evaluation & Analysis: [Name]  

---

## Timeline

- Week 1: Setup, preprocessing, baseline model  
- Week 2: Model improvement and comparison  
- Week 3: Optimization and error analysis  
- Week 4: Finalization and documentation  

---

## Expected Outcomes

- A working Akkadian → English translation model  
- A comparison between two transformer architectures  
- Insights into preprocessing and modeling choices  

---

## Notes

This project focuses on understanding the full machine learning pipeline and making informed design decisions, rather than achieving state-of-the-art performance.