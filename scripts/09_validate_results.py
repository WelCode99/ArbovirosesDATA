#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
09_validate_results.py
======================
Validate analysis results against expected reference values.

This script:
1. Loads processed data
2. Recalculates key statistics
3. Compares against expected values from EXPECTED_RESULTS.md
4. Reports validation status

Author: Welisson G.N. Costa
Date: January 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
import statsmodels.api as sm
import sys
import os

# Add parent directory to path to import expected results
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

DATA_PROCESSED = '../data/processed/'

# Expected values (from EXPECTED_RESULTS.md)
EXPECTED = {
    'sample_sizes': {
        'rtpcr': 201,
        'sinan_lab': 558,
        'sinan_clin': 543,
        'sinan_total': 1101
    },
    'diagnostic_accuracy': {
        'overall': {'value': 41.3, 'ci_low': 34.4, 'ci_high': 48.2},
        'chik_only': {'value': 9.0, 'ci_low': 5.0, 'ci_high': 13.0}
    },
    'diagnostic_hypotheses': {
        'Dengue only': {'count': 114, 'pct': 56.7},
        'Dengue or Chikungunya': {'count': 65, 'pct': 32.3},
        'Chikungunya only': {'count': 18, 'pct': 9.0},
        'Other': {'count': 4, 'pct': 2.0}
    },
    'hospitalization_rates': {
        'rtpcr': {'rate': 5.5, 'ci_low': 2.3, 'ci_high': 8.6},
        'sinan_lab': {'rate': 12.4, 'ci_low': 9.6, 'ci_high': 15.1},
        'sinan_clin': {'rate': 1.3, 'ci_low': 0.3, 'ci_high': 2.3}
    }
}

# Tolerance levels
TOLERANCE = {
    'percentage': 2.0,
    'or': 0.2,
    'ci': 0.3,
    'pvalue': 0.01,
    'count': 0  # Exact match required
}


def categorize_diagnosis(dx):
    """Categorize diagnostic hypothesis."""
    if pd.isna(dx):
        return 'Other'
    dx = str(dx).upper()
    if 'CHIKUNGUNYA' in dx and 'DENGUE' not in dx:
        return 'Chikungunya only'
    elif 'DENGUE' in dx and 'CHIKUNGUNYA' not in dx:
        return 'Dengue only'
    elif 'DENGUE' in dx and 'CHIKUNGUNYA' in dx:
        return 'Dengue or Chikungunya'
    elif 'DENGUE OU CHIK' in dx:
        return 'Dengue or Chikungunya'
    else:
        return 'Other'


def check_tolerance(observed, expected, tolerance, metric_name='value'):
    """Check if observed value is within tolerance of expected."""
    diff = abs(observed - expected)
    if diff <= tolerance:
        return True, diff
    else:
        return False, diff


def validate_sample_sizes(rtpcr_df, sinan_df, merged_df):
    """Validate sample sizes."""
    print("\n" + "=" * 60)
    print("VALIDATING SAMPLE SIZES")
    print("=" * 60)
    
    all_passed = True
    
    # RT-PCR
    n_rtpcr = len(rtpcr_df)
    expected_rtpcr = EXPECTED['sample_sizes']['rtpcr']
    passed, diff = check_tolerance(n_rtpcr, expected_rtpcr, TOLERANCE['count'])
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"RT-PCR+: {n_rtpcr} (expected: {expected_rtpcr}) - {status}")
    if not passed:
        all_passed = False
    
    # SINAN Lab
    sinan_lab = sinan_df[sinan_df['sinan_group'] == 'Laboratory']
    n_sinan_lab = len(sinan_lab)
    expected_sinan_lab = EXPECTED['sample_sizes']['sinan_lab']
    passed, diff = check_tolerance(n_sinan_lab, expected_sinan_lab, TOLERANCE['count'])
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"SINAN Laboratory: {n_sinan_lab} (expected: {expected_sinan_lab}) - {status}")
    if not passed:
        all_passed = False
    
    # SINAN Clinical
    sinan_clin = sinan_df[sinan_df['sinan_group'] == 'Clinical-epidemiological']
    n_sinan_clin = len(sinan_clin)
    expected_sinan_clin = EXPECTED['sample_sizes']['sinan_clin']
    passed, diff = check_tolerance(n_sinan_clin, expected_sinan_clin, TOLERANCE['count'])
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"SINAN Clinical: {n_sinan_clin} (expected: {expected_sinan_clin}) - {status}")
    if not passed:
        all_passed = False
    
    return all_passed


def validate_diagnostic_accuracy(rtpcr_df):
    """Validate diagnostic accuracy metrics."""
    print("\n" + "=" * 60)
    print("VALIDATING DIAGNOSTIC ACCURACY")
    print("=" * 60)
    
    all_passed = True
    n = len(rtpcr_df)
    
    # Overall accuracy
    correct = (rtpcr_df['diagnostic_correct'] == 1).sum()
    accuracy = correct / n * 100
    ci_low, ci_high = proportion_confint(correct, n, method='wilson')
    ci_low, ci_high = ci_low * 100, ci_high * 100
    
    expected = EXPECTED['diagnostic_accuracy']['overall']
    passed_val, diff_val = check_tolerance(accuracy, expected['value'], TOLERANCE['percentage'])
    passed_ci_low, diff_ci_low = check_tolerance(ci_low, expected['ci_low'], TOLERANCE['ci'])
    passed_ci_high, diff_ci_high = check_tolerance(ci_high, expected['ci_high'], TOLERANCE['ci'])
    
    passed = passed_val and passed_ci_low and passed_ci_high
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"Overall accuracy: {accuracy:.1f}% [{ci_low:.1f}-{ci_high:.1f}%] "
          f"(expected: {expected['value']:.1f}% [{expected['ci_low']:.1f}-{expected['ci_high']:.1f}%]) - {status}")
    if not passed:
        all_passed = False
    
    # Chikungunya only
    rtpcr_df['dx_category'] = rtpcr_df['HIPOTESE_DIAGNOSTICA'].apply(categorize_diagnosis)
    chik_only = (rtpcr_df['dx_category'] == 'Chikungunya only').sum()
    accuracy_chik = chik_only / n * 100
    ci_low_c, ci_high_c = proportion_confint(chik_only, n, method='wilson')
    ci_low_c, ci_high_c = ci_low_c * 100, ci_high_c * 100
    
    expected_chik = EXPECTED['diagnostic_accuracy']['chik_only']
    passed_val, diff_val = check_tolerance(accuracy_chik, expected_chik['value'], TOLERANCE['percentage'])
    passed_ci_low, diff_ci_low = check_tolerance(ci_low_c, expected_chik['ci_low'], TOLERANCE['ci'])
    passed_ci_high, diff_ci_high = check_tolerance(ci_high_c, expected_chik['ci_high'], TOLERANCE['ci'])
    
    passed = passed_val and passed_ci_low and passed_ci_high
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"Chikungunya only: {accuracy_chik:.1f}% [{ci_low_c:.1f}-{ci_high_c:.1f}%] "
          f"(expected: {expected_chik['value']:.1f}% [{expected_chik['ci_low']:.1f}-{expected_chik['ci_high']:.1f}%]) - {status}")
    if not passed:
        all_passed = False
    
    return all_passed


def validate_diagnostic_hypotheses(rtpcr_df):
    """Validate diagnostic hypotheses distribution."""
    print("\n" + "=" * 60)
    print("VALIDATING DIAGNOSTIC HYPOTHESES DISTRIBUTION")
    print("=" * 60)
    
    all_passed = True
    n = len(rtpcr_df)
    
    if 'dx_category' not in rtpcr_df.columns:
        rtpcr_df['dx_category'] = rtpcr_df['HIPOTESE_DIAGNOSTICA'].apply(categorize_diagnosis)
    
    for category, expected in EXPECTED['diagnostic_hypotheses'].items():
        count = (rtpcr_df['dx_category'] == category).sum()
        pct = count / n * 100
        
        passed_count, diff_count = check_tolerance(count, expected['count'], TOLERANCE['count'])
        passed_pct, diff_pct = check_tolerance(pct, expected['pct'], TOLERANCE['percentage'])
        
        passed = passed_count and passed_pct
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{category}: {count} ({pct:.1f}%) "
              f"(expected: {expected['count']} ({expected['pct']:.1f}%)) - {status}")
        if not passed:
            all_passed = False
    
    return all_passed


def validate_hospitalization_rates(merged_df):
    """Validate hospitalization rates."""
    print("\n" + "=" * 60)
    print("VALIDATING HOSPITALIZATION RATES")
    print("=" * 60)
    
    all_passed = True
    
    # RT-PCR+
    rtpcr_data = merged_df[merged_df['subgroup'] == 'RT-PCR Confirmed']
    n_rtpcr = len(rtpcr_data)
    hosp_rtpcr = rtpcr_data['hospitalized'].sum()
    rate_rtpcr = hosp_rtpcr / n_rtpcr * 100 if n_rtpcr > 0 else 0
    ci_low_r, ci_high_r = proportion_confint(hosp_rtpcr, n_rtpcr, method='wilson')
    ci_low_r, ci_high_r = ci_low_r * 100, ci_high_r * 100
    
    expected = EXPECTED['hospitalization_rates']['rtpcr']
    passed_rate, diff_rate = check_tolerance(rate_rtpcr, expected['rate'], TOLERANCE['percentage'])
    passed_ci_low, diff_ci_low = check_tolerance(ci_low_r, expected['ci_low'], TOLERANCE['ci'])
    passed_ci_high, diff_ci_high = check_tolerance(ci_high_r, expected['ci_high'], TOLERANCE['ci'])
    
    passed = passed_rate and passed_ci_low and passed_ci_high
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"RT-PCR+: {rate_rtpcr:.1f}% [{ci_low_r:.1f}-{ci_high_r:.1f}%] "
          f"(expected: {expected['rate']:.1f}% [{expected['ci_low']:.1f}-{expected['ci_high']:.1f}%]) - {status}")
    if not passed:
        all_passed = False
    
    # SINAN Lab
    sinan_lab_data = merged_df[merged_df['subgroup'] == 'SINAN Laboratory']
    n_sinan_lab = len(sinan_lab_data)
    hosp_sinan_lab = sinan_lab_data['hospitalized'].sum()
    rate_sinan_lab = hosp_sinan_lab / n_sinan_lab * 100 if n_sinan_lab > 0 else 0
    ci_low_sl, ci_high_sl = proportion_confint(hosp_sinan_lab, n_sinan_lab, method='wilson')
    ci_low_sl, ci_high_sl = ci_low_sl * 100, ci_high_sl * 100
    
    expected = EXPECTED['hospitalization_rates']['sinan_lab']
    passed_rate, diff_rate = check_tolerance(rate_sinan_lab, expected['rate'], TOLERANCE['percentage'])
    passed_ci_low, diff_ci_low = check_tolerance(ci_low_sl, expected['ci_low'], TOLERANCE['ci'])
    passed_ci_high, diff_ci_high = check_tolerance(ci_high_sl, expected['ci_high'], TOLERANCE['ci'])
    
    passed = passed_rate and passed_ci_low and passed_ci_high
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"SINAN Laboratory: {rate_sinan_lab:.1f}% [{ci_low_sl:.1f}-{ci_high_sl:.1f}%] "
          f"(expected: {expected['rate']:.1f}% [{expected['ci_low']:.1f}-{expected['ci_high']:.1f}%]) - {status}")
    if not passed:
        all_passed = False
    
    # SINAN Clinical
    sinan_clin_data = merged_df[merged_df['subgroup'] == 'SINAN Clinical-Epidemiological']
    n_sinan_clin = len(sinan_clin_data)
    hosp_sinan_clin = sinan_clin_data['hospitalized'].sum()
    rate_sinan_clin = hosp_sinan_clin / n_sinan_clin * 100 if n_sinan_clin > 0 else 0
    ci_low_sc, ci_high_sc = proportion_confint(hosp_sinan_clin, n_sinan_clin, method='wilson')
    ci_low_sc, ci_high_sc = ci_low_sc * 100, ci_high_sc * 100
    
    expected = EXPECTED['hospitalization_rates']['sinan_clin']
    passed_rate, diff_rate = check_tolerance(rate_sinan_clin, expected['rate'], TOLERANCE['percentage'])
    passed_ci_low, diff_ci_low = check_tolerance(ci_low_sc, expected['ci_low'], TOLERANCE['ci'])
    passed_ci_high, diff_ci_high = check_tolerance(ci_high_sc, expected['ci_high'], TOLERANCE['ci'])
    
    passed = passed_rate and passed_ci_low and passed_ci_high
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"SINAN Clinical: {rate_sinan_clin:.1f}% [{ci_low_sc:.1f}-{ci_high_sc:.1f}%] "
          f"(expected: {expected['rate']:.1f}% [{expected['ci_low']:.1f}-{expected['ci_high']:.1f}%]) - {status}")
    if not passed:
        all_passed = False
    
    return all_passed


def validate_data_integrity(rtpcr_df, sinan_df, merged_df):
    """Validate basic data integrity."""
    print("\n" + "=" * 60)
    print("VALIDATING DATA INTEGRITY")
    print("=" * 60)
    
    all_passed = True
    
    # Check for required columns
    required_rtpcr = ['id', 'idade', 'sexo', 'hospitalized', 'diagnostic_correct']
    for col in required_rtpcr:
        if col not in rtpcr_df.columns:
            print(f"✗ FAIL: Missing column '{col}' in RT-PCR data")
            all_passed = False
        else:
            print(f"✓ PASS: Column '{col}' present in RT-PCR data")
    
    # Check for missing IDs
    if 'id' in rtpcr_df.columns:
        if rtpcr_df['id'].isna().any():
            print("✗ FAIL: Missing IDs in RT-PCR data")
            all_passed = False
        else:
            print("✓ PASS: All RT-PCR IDs present")
    
    # Check merged dataset structure
    if len(merged_df) != len(rtpcr_df) + len(sinan_df[sinan_df['sinan_group'] == 'Laboratory']) + len(sinan_df[sinan_df['sinan_group'] == 'Clinical-epidemiological']):
        print("✗ FAIL: Merged dataset size mismatch")
        all_passed = False
    else:
        print("✓ PASS: Merged dataset size correct")
    
    return all_passed


if __name__ == "__main__":
    print("=" * 60)
    print("VALIDATING ANALYSIS RESULTS")
    print("Chikungunya Surveillance Study - Foz do Iguaçu, 2023")
    print("=" * 60)
    
    # Load processed data
    print("\nLoading processed data...")
    try:
        rtpcr_df = pd.read_csv(f'{DATA_PROCESSED}rtpcr_processed.csv')
        sinan_df = pd.read_csv(f'{DATA_PROCESSED}sinan_processed.csv')
        merged_df = pd.read_csv(f'{DATA_PROCESSED}merged_analysis_dataset.csv')
        print("✓ Data loaded successfully")
    except FileNotFoundError as e:
        print(f"✗ ERROR: Could not load data files: {e}")
        print("  Please run data preprocessing first (01_data_preprocessing.py)")
        sys.exit(1)
    
    # Run validations
    results = {}
    
    results['data_integrity'] = validate_data_integrity(rtpcr_df, sinan_df, merged_df)
    results['sample_sizes'] = validate_sample_sizes(rtpcr_df, sinan_df, merged_df)
    results['diagnostic_accuracy'] = validate_diagnostic_accuracy(rtpcr_df)
    results['diagnostic_hypotheses'] = validate_diagnostic_hypotheses(rtpcr_df)
    results['hospitalization_rates'] = validate_hospitalization_rates(merged_df)
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    all_passed = all(results.values())
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL VALIDATIONS PASSED")
        print("=" * 60)
        sys.exit(0)
    else:
        print("✗ SOME VALIDATIONS FAILED")
        print("=" * 60)
        print("\nNote: Some differences may be acceptable due to:")
        print("  - Rounding differences")
        print("  - Minor data processing variations")
        print("  - Statistical method implementation differences")
        sys.exit(1)
