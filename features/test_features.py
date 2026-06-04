# features/tests/test_features.py
# Unit tests for feature engineering pipeline

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Path add karo
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


# ─── Helper — ek raw CDR row banao ───────────────────────────────────────────

def make_raw_cdr(**kwargs):
    """Base CDR row with default values — override with kwargs."""
    defaults = {
        'Account Length': 82,
        'VMail Message': 0,
        'Day Mins': 300.0,
        'Day Calls': 100,
        'Day Charge': 51.0,
        'Eve Mins': 180.0,
        'Eve Calls': 90,
        'Eve Charge': 15.0,
        'Night Mins': 270.0,
        'Night Calls': 70,
        'Night Charge': 12.0,
        'Intl Mins': 10.0,
        'Intl Calls': 4,
        'Intl Charge': 3.0,
        'CustServ Calls': 2,
    }
    defaults.update(kwargs)
    return pd.DataFrame([defaults])


def apply_features(df):
    """Apply all feature engineering steps — mirrors explainer.py logic."""
    df = df.copy()

    # Category 1 — Call Volume
    df['total_calls'] = (df['Day Calls'] + df['Eve Calls'] +
                         df['Night Calls'] + df['Intl Calls'])
    df['total_mins'] = (df['Day Mins'] + df['Eve Mins'] +
                        df['Night Mins'] + df['Intl Mins'])
    df['total_charge'] = (df['Day Charge'] + df['Eve Charge'] +
                          df['Night Charge'] + df['Intl Charge'])
    df['avg_call_duration'] = df['total_mins'] / (df['total_calls'] + 1e-9)
    df['call_intensity'] = df['total_calls'] * df['total_mins']

    # Category 2 — Charge Behaviour
    df['charge_per_min'] = df['total_charge'] / (df['total_mins'] + 1e-9)
    df['day_charge_ratio'] = df['Day Charge'] / (df['total_charge'] + 1e-9)
    df['intl_charge_ratio'] = df['Intl Charge'] / (df['total_charge'] + 1e-9)

    # Category 3 — International
    df['intl_call_ratio'] = df['Intl Calls'] / (df['total_calls'] + 1e-9)
    df['intl_mins_ratio'] = df['Intl Mins'] / (df['total_mins'] + 1e-9)
    df['intl_avg_duration'] = df['Intl Mins'] / (df['Intl Calls'] + 1e-9)

    # Category 4 — Time-of-Day
    df['day_usage_ratio'] = df['Day Mins'] / (df['total_mins'] + 1e-9)
    df['night_usage_ratio'] = df['Night Mins'] / (df['total_mins'] + 1e-9)
    df['eve_usage_ratio'] = df['Eve Mins'] / (df['total_mins'] + 1e-9)
    df['night_to_day_ratio'] = df['Night Mins'] / (df['Day Mins'] + 1e-9)

    # Category 5 — Risk Signals
    df['high_custserv_flag'] = (df['CustServ Calls'] > 3).astype(int)
    df['voicemail_ratio'] = df['VMail Message'] / (df['total_calls'] + 1e-9)
    df['account_call_intensity'] = df['total_calls'] / (df['Account Length'] + 1e-9)

    # Drop redundant charge columns
    df = df.drop(columns=['Day Charge', 'Eve Charge',
                           'Night Charge', 'Intl Charge'], errors='ignore')
    return df


# ─── Category 1: Call Volume Tests ───────────────────────────────────────────

def test_total_calls_correct():
    """total_calls = sum of all 4 call types."""
    df = make_raw_cdr(Day_Calls=10, Eve_Calls=5, Night_Calls=3, Intl_Calls=2)
    # Fix column names
    df.columns = [c.replace('_', ' ') for c in df.columns]
    result = apply_features(df)
    assert result['total_calls'].iloc[0] == 20


def test_total_mins_correct():
    df = make_raw_cdr()
    result = apply_features(df)
    expected = 300.0 + 180.0 + 270.0 + 10.0
    assert abs(result['total_mins'].iloc[0] - expected) < 0.01


def test_avg_call_duration_positive():
    """avg_call_duration should always be positive."""
    df = make_raw_cdr()
    result = apply_features(df)
    assert result['avg_call_duration'].iloc[0] > 0


def test_call_intensity_positive():
    df = make_raw_cdr()
    result = apply_features(df)
    assert result['call_intensity'].iloc[0] > 0


# ─── Category 2: Charge Behaviour Tests ──────────────────────────────────────

def test_day_charge_ratio_between_0_and_1():
    """day_charge_ratio must be between 0 and 1."""
    df = make_raw_cdr()
    result = apply_features(df)
    ratio = result['day_charge_ratio'].iloc[0]
    assert 0.0 <= ratio <= 1.0


def test_intl_charge_ratio_between_0_and_1():
    df = make_raw_cdr()
    result = apply_features(df)
    ratio = result['intl_charge_ratio'].iloc[0]
    assert 0.0 <= ratio <= 1.0


# ─── Category 3: International Tests ─────────────────────────────────────────

def test_intl_call_ratio_between_0_and_1():
    df = make_raw_cdr()
    result = apply_features(df)
    ratio = result['intl_call_ratio'].iloc[0]
    assert 0.0 <= ratio <= 1.0


def test_intl_avg_duration_positive():
    df = make_raw_cdr()
    result = apply_features(df)
    assert result['intl_avg_duration'].iloc[0] > 0


def test_zero_intl_calls_no_division_error():
    """Zero international calls should not raise division error."""
    df = make_raw_cdr(**{'Intl Calls': 0, 'Intl Mins': 0})
    result = apply_features(df)
    assert not result['intl_avg_duration'].isna().any()


# ─── Category 4: Time-of-Day Tests ───────────────────────────────────────────

def test_usage_ratios_sum_to_approx_1():
    """day + night + eve + intl usage ratios should sum to ~1."""
    df = make_raw_cdr()
    result = apply_features(df)
    total = (result['day_usage_ratio'].iloc[0] +
             result['night_usage_ratio'].iloc[0] +
             result['eve_usage_ratio'].iloc[0] +
             result['Intl Mins'].iloc[0] / result['total_mins'].iloc[0])
    assert abs(total - 1.0) < 0.01


def test_night_to_day_ratio_high_for_night_heavy_user():
    """Night-heavy user should have night_to_day_ratio > 1."""
    df = make_raw_cdr(**{'Night Mins': 500.0, 'Day Mins': 100.0})
    result = apply_features(df)
    assert result['night_to_day_ratio'].iloc[0] > 1.0


# ─── Category 5: Risk Signal Tests ───────────────────────────────────────────

def test_high_custserv_flag_at_threshold():
    """Exactly 3 calls = NOT flagged. 4 calls = flagged."""
    df_3 = make_raw_cdr(**{'CustServ Calls': 3})
    df_4 = make_raw_cdr(**{'CustServ Calls': 4})
    assert apply_features(df_3)['high_custserv_flag'].iloc[0] == 0
    assert apply_features(df_4)['high_custserv_flag'].iloc[0] == 1


def test_high_custserv_flag_zero_calls():
    df = make_raw_cdr(**{'CustServ Calls': 0})
    assert apply_features(df)['high_custserv_flag'].iloc[0] == 0


def test_voicemail_ratio_zero_for_spammer():
    """Spammer with 0 voicemail and 100 calls — ratio should be near 0."""
    df = make_raw_cdr(**{'VMail Message': 0, 'Day Calls': 100})
    result = apply_features(df)
    assert result['voicemail_ratio'].iloc[0] < 0.01


def test_account_call_intensity_higher_for_new_account():
    """New account (short length) with many calls = high intensity."""
    old = make_raw_cdr(**{'Account Length': 200})
    new = make_raw_cdr(**{'Account Length': 5})
    old_intensity = apply_features(old)['account_call_intensity'].iloc[0]
    new_intensity = apply_features(new)['account_call_intensity'].iloc[0]
    assert new_intensity > old_intensity


# ─── Column Drop Tests ────────────────────────────────────────────────────────

def test_charge_columns_dropped():
    """Original charge columns must be removed after engineering."""
    df = make_raw_cdr()
    result = apply_features(df)
    for col in ['Day Charge', 'Eve Charge', 'Night Charge', 'Intl Charge']:
        assert col not in result.columns


def test_no_null_values_in_output():
    """No NaN values in final engineered feature set."""
    df = make_raw_cdr()
    result = apply_features(df)
    assert not result.isna().any().any()


def test_no_infinite_values():
    """No infinite values in output."""
    df = make_raw_cdr()
    result = apply_features(df)
    numeric = result.select_dtypes(include=[np.number])
    assert not np.isinf(numeric.values).any()