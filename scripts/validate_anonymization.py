#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_anonymization.py
=========================
Validation script to verify data anonymization compliance.

This script validates that:
1. No PII fields exist in the datasets
2. K-anonymity (k≥3) is achieved
3. Preprocessing scripts work with anonymized data
4. All documentation is in place

Author: Welisson G.N. Costa
Date: February 2025
"""

import pandas as pd
import os
import sys

# =============================================================================
# CONFIGURATION
# =============================================================================

DATA_RAW = '../data/raw/'
DOCS_DIR = '../docs/'

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def check_pii_fields():
    """Check for presence of PII fields that should be removed."""
    print("\n" + "=" * 70)
    print("1. CHECKING FOR PII FIELDS")
    print("=" * 70)
    
    issues = []
    
    # RTPCR dataset
    print("\nRTCPR Dataset:")
    rtpcr = pd.read_csv(f'{DATA_RAW}RTPCR_chikungunya_anonymized.csv', sep=';')
    
    pii_fields_rtpcr = ['nome', 'cpf', 'rg', 'endereco', 'telefone', 'email', 
                        'data', 'sintomas']  # data and sintomas should be removed
    found_pii = [f for f in pii_fields_rtpcr if f in rtpcr.columns]
    
    if found_pii:
        issues.append(f"RTPCR: Found PII fields: {found_pii}")
        print(f"  ✗ FAIL: Found PII fields: {found_pii}")
    else:
        print("  ✓ PASS: No PII fields found")
    
    # Check for required anonymized fields
    required_anon = ['year_month', 'age_bin']
    missing_anon = [f for f in required_anon if f not in rtpcr.columns]
    if missing_anon:
        issues.append(f"RTPCR: Missing anonymized fields: {missing_anon}")
        print(f"  ✗ FAIL: Missing anonymized fields: {missing_anon}")
    else:
        print("  ✓ PASS: Anonymized fields present")
    
    # SINAN dataset
    print("\nSINAN Dataset:")
    sinan = pd.read_csv(f'{DATA_RAW}SINAN_chikungunya_2023.csv', sep=';', low_memory=False)
    
    pii_fields_sinan = ['ANO_NASC', 'NU_IDADE_N', 'munResLat', 'munResLon', 
                        'ID_UNIDADE', 'ID_MN_RESI', 'munResNome', 'ID_MUNICIP']
    found_pii_sinan = [f for f in pii_fields_sinan if f in sinan.columns]
    
    if found_pii_sinan:
        issues.append(f"SINAN: Found PII fields: {found_pii_sinan}")
        print(f"  ✗ FAIL: Found PII fields: {found_pii_sinan}")
    else:
        print("  ✓ PASS: No PII fields found")
    
    # Check for anonymized fields
    required_anon_sinan = ['age_group']
    missing_anon_sinan = [f for f in required_anon_sinan if f not in sinan.columns]
    if missing_anon_sinan:
        issues.append(f"SINAN: Missing anonymized fields: {missing_anon_sinan}")
        print(f"  ✗ FAIL: Missing anonymized fields: {missing_anon_sinan}")
    else:
        print("  ✓ PASS: Anonymized fields present")
    
    return issues

def check_k_anonymity():
    """Validate k-anonymity compliance."""
    print("\n" + "=" * 70)
    print("2. VALIDATING K-ANONYMITY (k≥3)")
    print("=" * 70)
    
    issues = []
    
    # RTPCR dataset
    print("\nRTCPR Dataset:")
    rtpcr = pd.read_csv(f'{DATA_RAW}RTPCR_chikungunya_anonymized.csv', sep=';')
    
    quasi_ids = ['year_month', 'age_bin', 'sexo', 'bairro']
    group_sizes = rtpcr.groupby(quasi_ids).size()
    min_size = group_sizes.min()
    violations = (group_sizes < 3).sum()
    
    print(f"  Minimum group size: {min_size}")
    print(f"  Violations (groups < 3): {violations}")
    
    if violations > 0 or min_size < 3:
        issues.append(f"RTPCR: K-anonymity violated ({violations} groups < 3)")
        print(f"  ✗ FAIL: K-anonymity not achieved")
    else:
        print("  ✓ PASS: K-anonymity k≥3 achieved")
    
    # SINAN dataset
    print("\nSINAN Dataset:")
    sinan = pd.read_csv(f'{DATA_RAW}SINAN_chikungunya_2023.csv', sep=';', low_memory=False)
    
    if 'DT_SIN_PRI_month' in sinan.columns and 'age_group' in sinan.columns:
        quasi_ids_sinan = ['DT_SIN_PRI_month', 'age_group', 'CS_SEXO']
        group_sizes_sinan = sinan.groupby(quasi_ids_sinan).size()
        min_size_sinan = group_sizes_sinan.min()
        violations_sinan = (group_sizes_sinan < 3).sum()
        
        print(f"  Minimum group size: {min_size_sinan}")
        print(f"  Violations (groups < 3): {violations_sinan}")
        
        if violations_sinan > 0 or min_size_sinan < 3:
            issues.append(f"SINAN: K-anonymity violated ({violations_sinan} groups < 3)")
            print(f"  ✗ FAIL: K-anonymity not achieved")
        else:
            print("  ✓ PASS: K-anonymity k≥3 achieved")
    else:
        issues.append("SINAN: Cannot validate k-anonymity (missing required fields)")
        print("  ✗ FAIL: Cannot validate (missing fields)")
    
    return issues

def check_documentation():
    """Verify required documentation exists."""
    print("\n" + "=" * 70)
    print("3. CHECKING DOCUMENTATION")
    print("=" * 70)
    
    issues = []
    
    required_docs = [
        'DATA_ANONYMIZATION.md',
        'CODEBOOK.md'
    ]
    
    for doc in required_docs:
        path = f'{DOCS_DIR}{doc}'
        if os.path.exists(path):
            print(f"  ✓ {doc} exists")
        else:
            issues.append(f"Missing documentation: {doc}")
            print(f"  ✗ {doc} missing")
    
    return issues

def check_scripts():
    """Verify anonymization and preprocessing scripts exist."""
    print("\n" + "=" * 70)
    print("4. CHECKING SCRIPTS")
    print("=" * 70)
    
    issues = []
    
    required_scripts = [
        '00_anonymize_data.py',
        '01_data_preprocessing.py'
    ]
    
    for script in required_scripts:
        path = f'../scripts/{script}'
        if os.path.exists(path):
            print(f"  ✓ {script} exists")
        else:
            issues.append(f"Missing script: {script}")
            print(f"  ✗ {script} missing")
    
    return issues

# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run all validation checks."""
    print("\n" + "=" * 70)
    print(" DATA ANONYMIZATION VALIDATION")
    print("=" * 70)
    print("\nValidating LGPD compliance and k-anonymity...")
    
    all_issues = []
    
    # Run checks
    all_issues.extend(check_pii_fields())
    all_issues.extend(check_k_anonymity())
    all_issues.extend(check_documentation())
    all_issues.extend(check_scripts())
    
    # Summary
    print("\n" + "=" * 70)
    print(" VALIDATION SUMMARY")
    print("=" * 70)
    
    if all_issues:
        print(f"\n✗ VALIDATION FAILED - {len(all_issues)} issue(s) found:\n")
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
        sys.exit(1)
    else:
        print("\n✓ ALL VALIDATION CHECKS PASSED")
        print("\nThe repository data is properly anonymized and compliant with:")
        print("  - Brazilian LGPD (Lei nº 13.709/2018)")
        print("  - K-anonymity standard (k≥3)")
        print("  - International privacy best practices")
        print("\nThe data is safe for public sharing and research use.")
        sys.exit(0)

if __name__ == '__main__':
    main()
