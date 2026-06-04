# Feature Engineering Specification
## Telecom Fraud Detection Platform

---

## Overview

Starting from raw CDR data (15 fields), 18 new features were engineered across 5 categories. Redundant charge columns were dropped after engineering composite features. Final feature set: 29 features (15 raw - 4 dropped + 18 engineered).

---

## Raw CDR Fields (Input)

| Field | Type | Description |
|---|---|---|
| Account Length | float | Account age in days |
| VMail Message | float | Number of voicemail messages |
| Day Mins | float | Total daytime minutes |
| Day Calls | float | Total daytime calls |
| Day Charge | float | Total daytime charge |
| Eve Mins | float | Total evening minutes |
| Eve Calls | float | Total evening calls |
| Eve Charge | float | Total evening charge |
| Night Mins | float | Total night minutes |
| Night Calls | float | Total night calls |
| Night Charge | float | Total night charge |
| Intl Mins | float | Total international minutes |
| Intl Calls | float | Total international calls |
| Intl Charge | float | Total international charge |
| CustServ Calls | float | Number of customer service calls |

**Dropped columns:** Day Charge, Eve Charge, Night Charge, Intl Charge
**Reason:** Mathematically redundant — derived from minutes × fixed rate. Including them would introduce multicollinearity.

---

## Engineered Features

### Category 1 — Call Volume (5 features)

| # | Feature | Formula | Rationale |
|---|---|---|---|
| F1 | total_calls | Day + Eve + Night + Intl Calls | Overall call activity — spammers make unusually high call counts |
| F2 | total_mins | Day + Eve + Night + Intl Mins | Total usage intensity signal |
| F3 | total_charge | Day + Eve + Night + Intl Charge | Aggregate billing signal — fraud rings accumulate high charges |
| F4 | avg_call_duration | total_mins / (total_calls + ε) | Robocalls average 2-3 seconds; legitimate calls 3-5 minutes |
| F5 | call_intensity | total_calls × total_mins | Composite aggression score — high calls AND high mins = strong signal |

### Category 2 — Charge Behaviour (3 features)

| # | Feature | Formula | Rationale |
|---|---|---|---|
| F6 | charge_per_min | total_charge / (total_mins + ε) | Billing anomaly detector — unexpected rate deviations |
| F7 | day_charge_ratio | Day Charge / (total_charge + ε) | Daytime billing proportion — fraud rings often active day |
| F8 | intl_charge_ratio | Intl Charge / (total_charge + ε) | High international charge proportion = suspicious activity |

### Category 3 — International Call Behaviour (3 features)

| # | Feature | Formula | Rationale |
|---|---|---|---|
| F9 | intl_call_ratio | Intl Calls / (total_calls + ε) | Normal: 1-2%; Fraud rings: 20-30%+ |
| F10 | intl_mins_ratio | Intl Mins / (total_mins + ε) | International usage proportion |
| F11 | intl_avg_duration | Intl Mins / (Intl Calls + ε) | Short repeated international calls = IRSF fraud red flag |

### Category 4 — Time-of-Day Behaviour (4 features)

| # | Feature | Formula | Rationale |
|---|---|---|---|
| F12 | day_usage_ratio | Day Mins / (total_mins + ε) | Normal users call mostly during day |
| F13 | night_usage_ratio | Night Mins / (total_mins + ε) | Spammers more active at night to avoid detection |
| F14 | eve_usage_ratio | Eve Mins / (total_mins + ε) | Evening activity proportion |
| F15 | night_to_day_ratio | Night Mins / (Day Mins + ε) | Ratio > 1 = suspicious night-heavy activity |

### Category 5 — Risk Signals (3 features)

| # | Feature | Formula | Rationale |
|---|---|---|---|
| F16 | high_custserv_flag | 1 if CustServ Calls > 3 else 0 | >3 complaints = strong fraud signal (TRAI threshold) |
| F17 | voicemail_ratio | VMail Message / (total_calls + ε) | Spammers skip voicemail — ratio near 0 = red flag |
| F18 | account_call_intensity | total_calls / (Account Length + ε) | New account + high calls = fraud pattern |

*ε = 1e-9 (small constant to avoid division by zero)*

---

## Validation Evidence

All 18 features were validated for discriminative power between fraud and legitimate callers.

**Statistical validation methods used:**
- Distribution plots (boxplots, histograms) per class
- Mean comparison: fraud vs legitimate per feature
- Correlation with isFraud label
- SHAP feature importance from trained Random Forest

**Top 5 features by SHAP importance:**
1. Day Mins — highest discriminative power
2. Intl Mins — international usage anomaly
3. VMail Message — voicemail behaviour
4. intl_avg_duration — short international calls
5. high_custserv_flag — complaint history

**Validation notebook:** `notebooks/02_feature_engineering.ipynb`

---

## Computation Logic

```python
# Category 1 — Call Volume
df['total_calls'] = df['Day Calls'] + df['Eve Calls'] + df['Night Calls'] + df['Intl Calls']
df['total_mins']  = df['Day Mins']  + df['Eve Mins']  + df['Night Mins']  + df['Intl Mins']
df['total_charge']= df['Day Charge']+ df['Eve Charge']+ df['Night Charge']+ df['Intl Charge']
df['avg_call_duration'] = df['total_mins'] / (df['total_calls'] + 1e-9)
df['call_intensity']    = df['total_calls'] * df['total_mins']

# Category 2 — Charge Behaviour
df['charge_per_min']   = df['total_charge'] / (df['total_mins'] + 1e-9)
df['day_charge_ratio'] = df['Day Charge']  / (df['total_charge'] + 1e-9)
df['intl_charge_ratio']= df['Intl Charge'] / (df['total_charge'] + 1e-9)

# Category 3 — International
df['intl_call_ratio']   = df['Intl Calls'] / (df['total_calls'] + 1e-9)
df['intl_mins_ratio']   = df['Intl Mins']  / (df['total_mins']  + 1e-9)
df['intl_avg_duration'] = df['Intl Mins']  / (df['Intl Calls']  + 1e-9)

# Category 4 — Time-of-Day
df['day_usage_ratio']   = df['Day Mins']   / (df['total_mins'] + 1e-9)
df['night_usage_ratio'] = df['Night Mins'] / (df['total_mins'] + 1e-9)
df['eve_usage_ratio']   = df['Eve Mins']   / (df['total_mins'] + 1e-9)
df['night_to_day_ratio']= df['Night Mins'] / (df['Day Mins']   + 1e-9)

# Category 5 — Risk Signals
df['high_custserv_flag']    = (df['CustServ Calls'] > 3).astype(int)
df['voicemail_ratio']       = df['VMail Message'] / (df['total_calls'] + 1e-9)
df['account_call_intensity']= df['total_calls']   / (df['Account Length'] + 1e-9)

# Drop redundant charge columns
df = df.drop(columns=['Day Charge','Eve Charge','Night Charge','Intl Charge'])
```