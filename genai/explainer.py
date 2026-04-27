# genai/explainer
import os
import requests
import json
import pickle
import pandas as pd
import numpy as np


# STEP 1 — Saved model aur features load karo

# Base path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'artifacts', 'fraud_model.pkl')
FEATURES_PATH = os.path.join(BASE_DIR, 'models', 'artifacts', 'features_names.pkl')

# Trained Random Forest loading
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# Features loading
with open(FEATURES_PATH, 'rb') as f:
    feature_names = pickle.load(f)

print("✅ Model loaded successfully")
print(f"✅ Features loaded: {len(feature_names)} features")

# STEP 2 — Feature Engineering Function

def engineer_features(raw_data: dict) -> pd.DataFrame:
    """
    Raw CDR data → Engineered features
    Input : dict with raw CDR columns
    Output: DataFrame with all 29 features
    """
    df = pd.DataFrame([raw_data])

    # --- Call Volume Features ---
    df['total_calls'] = (df['Day Calls'] + df['Eve Calls'] +
                         df['Night Calls'] + df['Intl Calls'])
    df['total_mins'] = (df['Day Mins'] + df['Eve Mins'] +
                        df['Night Mins'] + df['Intl Mins'])
    df['total_charge'] = (df['Day Charge'] + df['Eve Charge'] +
                          df['Night Charge'] + df['Intl Charge'])
    df['avg_call_duration'] = df['total_mins'] / (df['total_calls'] + 1e-9)
    df['call_intensity'] = df['total_calls'] * df['total_mins']

    # --- Charge Behaviour Features ---
    df['charge_per_min'] = df['total_charge'] / (df['total_mins'] + 1e-9)
    df['day_charge_ratio'] = df['Day Charge'] / (df['total_charge'] + 1e-9)
    df['intl_charge_ratio'] = df['Intl Charge'] / (df['total_charge'] + 1e-9)

    # --- International Features ---
    df['intl_call_ratio'] = df['Intl Calls'] / (df['total_calls'] + 1e-9)
    df['intl_mins_ratio'] = df['Intl Mins'] / (df['total_mins'] + 1e-9)
    df['intl_avg_duration'] = df['Intl Mins'] / (df['Intl Calls'] + 1e-9)

    # --- Time-of-Day Features ---
    df['day_usage_ratio'] = df['Day Mins'] / (df['total_mins'] + 1e-9)
    df['night_usage_ratio'] = df['Night Mins'] / (df['total_mins'] + 1e-9)
    df['eve_usage_ratio'] = df['Eve Mins'] / (df['total_mins'] + 1e-9)
    df['night_to_day_ratio'] = df['Night Mins'] / (df['Day Mins'] + 1e-9)

    # --- Risk Signal Features ---
    df['high_custserv_flag'] = (df['CustServ Calls'] > 3).astype(int)
    df['voicemail_ratio'] = df['VMail Message'] / (df['total_calls'] + 1e-9)
    df['account_call_intensity'] = df['total_calls'] / (df['Account Length'] + 1e-9)

    # Charge columns drop karo — redundant hain
    df = df.drop(columns=['Day Charge', 'Eve Charge',
                          'Night Charge', 'Intl Charge'],
                 errors='ignore')

    return df[feature_names]  

# STEP 3 — Fraud Score Function

def get_fraud_score(raw_data: dict) -> dict:
    """
    Raw CDR data se fraud probability nikalo
    Input : dict with raw CDR values
    Output: dict with score + top features
    """
    # Features engineer karo
    features = engineer_features(raw_data)

    # Fraud probability nikalo
    fraud_prob = model.predict_proba(features)[0][1]
    is_fraud = fraud_prob > 0.3

    # Top 5 important features nikalo
    importances = model.feature_importances_
    feat_imp = pd.Series(importances, index=feature_names)
    top_features = feat_imp.nlargest(5).index.tolist()

    # Top features ki values nikalo
    top_values = {feat: round(float(features[feat].values[0]), 4)
                  for feat in top_features}

    return {
        'fraud_probability': round(float(fraud_prob), 4),
        'is_fraud': bool(is_fraud),
        'top_features': top_values
    }

# STEP 4 — LLM Explanation Function

def explain_fraud(raw_data: dict) -> str:
    """
    Fraud score + features → LLM se plain English explanation
    Input : dict with raw CDR values
    Output: Human readable explanation string
    """
    # Pehle fraud score nikalo
    result = get_fraud_score(raw_data)

    fraud_pct = round(result['fraud_probability'] * 100, 1)
    top_features = result['top_features']

    # PROMPT ENGINEERING
   
    prompt = f"""You are a telecom fraud detection analyst.

A phone number has been analyzed by our ML model with the following results:

Fraud Probability: {fraud_pct}%
Status: {"FRAUD DETECTED" if result['is_fraud'] else "LEGITIMATE"}

Top contributing features:
{json.dumps(top_features, indent=2)}

Based on these signals, write a clear 3-4 sentence explanation for a telecom analyst.
Explain WHY this number was flagged or cleared.
Be specific about which features are suspicious and why.
Do not use technical jargon — write in simple English.
"""

    # OLLAMA API CALL
    # Ollama locally chal raha hai port 11434 pe

    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'llama3',
            'prompt': prompt,
            'stream': False      
        }
    )

    if response.status_code == 200:
        explanation = response.json()['response']
        return explanation
    else:
        return f"Error: {response.status_code} — Ollama server check karo"


# STEP 5 — Test Karo

if __name__ == "__main__":

    # Example — ek suspicious user ka data
    suspicious_user = {
        'Account Length': 77,
        'VMail Message': 0,      # Voicemail nahi — red flag
        'Day Mins': 62.4,       # Bahut zyada — red flag
        'Day Calls': 89,        # Bahut zyada calls
        'Day Charge': 10.61,
        'Eve Mins': 169.9,
        'Eve Calls': 121,
        'Eve Charge': 14.44,
        'Night Mins': 209.6,     # Raat ko bhi zyada — red flag
        'Night Calls': 64,
        'Night Charge': 9.43,
        'Intl Mins': 5.7,
        'Intl Calls': 6,
        'Intl Charge': 1.54,
        'CustServ Calls': 5,   # >3 — red flag
    }

    print("\n" + "="*50)
    print("FRAUD DETECTION + LLM EXPLANATION")
    print("="*50)


    # Score nikalo
    result = get_fraud_score(suspicious_user)
    print(f"\nFraud Probability : {result['fraud_probability']*100:.1f}%")
    print(f"Is Fraud          : {result['is_fraud']}")
    print(f"Top Features      : {result['top_features']}")

    # LLM explanation 
    print("\nGenerating LLM Explanation...")
    explanation = explain_fraud(suspicious_user)
    print(f"\nExplanation:\n{explanation}")