# Telecom Fraud Detection - Model Selection Report

## Objective

The objective of model selection was to evaluate multiple machine learning approaches for telecom fraud detection using engineered CDR behavioral features while effectively handling severe class imbalance.

---

# Dataset Characteristics

- Legitimate Users: 89.6%
- Fraudulent Users: 10.4%

This heavy imbalance required specialized fraud-learning strategies to improve minority-class detection performance.

---

# Models Evaluated

## 1. Logistic Regression

### Type
Supervised Learning

### Performance
- Precision: 0.14
- Recall: 0.59
- F1-Score: 0.23
- PR-AUC: 0.1556

### Observations
Linear modelling struggled to capture complex telecom fraud behavior patterns.

---

## 2. Random Forest

### Type
Supervised Learning

### Performance
- Precision: 0.77
- Recall: 0.85
- F1-Score: 0.81
- PR-AUC: 0.7806

### Observations
Random Forest demonstrated strong fraud detection capability and stable performance across engineered telecom features.

---

## 3. XGBoost

### Type
Supervised Learning

### Performance
- Precision: 0.54
- Recall: 0.90
- F1-Score: 0.68
- PR-AUC: 0.7691

### Observations
XGBoost achieved high recall but generated more false positives.

---

## 4. LightGBM

### Type
Supervised Learning

### Performance
- Precision: 0.46
- Recall: 0.90
- F1-Score: 0.60
- PR-AUC: 0.7296

### Observations
LightGBM provided fast training and strong recall but lower precision compared to Random Forest.

---

## 5. Isolation Forest

### Type
Unsupervised Anomaly Detection

### Performance
- Precision: 0.16
- Recall: 0.15
- F1-Score: 0.15

### Observations
Unsupervised anomaly detection struggled to separate fraud patterns effectively.

---

## 6. Random Forest + SMOTE

### Type
Supervised Learning with Oversampling

### Performance
- Precision: 0.81
- Recall: 0.86
- F1-Score: 0.83
- PR-AUC: 0.8610

### Observations
Applying SMOTE significantly improved minority fraud learning and reduced missed fraud cases.

---

# Final Selected Model

## Final Model:
Random Forest + SMOTE

### Reason for Selection

After extensive experimentation and comparative benchmarking, Random Forest combined with SMOTE achieved the strongest overall telecom fraud detection performance.

The model demonstrated:

- highest PR-AUC score
- improved minority fraud detection
- strong precision-recall balance
- reduced false negatives
- stable probability scoring
- reliable SHAP explainability integration

SMOTE successfully addressed severe class imbalance by generating synthetic fraud samples during training.

---

# Explainability

SHAP explainability was applied to both:
- baseline Random Forest
- final Random Forest + SMOTE pipeline

## Key SHAP Findings

Top fraud-driving features included:
- Day Minutes
- Intl Minutes
- voicemail_ratio
- intl_avg_duration
- high_custserv_flag

The Random Forest + SMOTE model learned minority fraud behavior more effectively, confirmed by improved SHAP feature rankings.

---

# Threshold Tuning

Fraud probability threshold was reduced from:
- 0.5 → 0.3

### Purpose
Improve fraud recall and minimize missed fraudsters.

---

# Final Saved Artifacts

The following production artifacts were exported:

- fraud_model.pkl
- scaler.pkl
- features_names.pkl

These artifacts are used by the FastAPI backend for real-time fraud scoring.

---

# Why PR-AUC Over Accuracy

Dataset mein 89.6% legitimate users hain.

A model predicting "all legitimate" gets:
- Accuracy: 89.6% ← misleading
- PR-AUC: 0.10 ← correctly shows it's useless

Random Forest + SMOTE:
- Accuracy: 94%
- PR-AUC: 0.8610 ← actually captures fraud well

PR-AUC measures precision-recall tradeoff across all
thresholds — the correct metric for imbalanced fraud detection.

---

**Training notebook:** `notebooks/03_model_cdr.ipynb`
**Evaluation plots:** `data/processed/model_compariso.png`,
`shap_beeswarm.png`, `shap_important.png`

---
