#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_descriptive_analysis.py
==========================
Descriptive statistics for Chikungunya surveillance study.

Author: Welisson G.N. Costa
Date: January 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

DATA_PROCESSED = '../data/processed/'

def calculate_descriptive_stats(df, group_name):
    """Calculate descriptive statistics for a dataset."""
    print(f"\n{'='*60}")
    print(f"DESCRIPTIVE STATISTICS: {group_name}")
    print(f"{'='*60}")
    
    n = len(df)
    print(f"\nSample size: n = {n}")
    
    # Demographics
    print(f"\n--- Demographics ---")
    
    # Age
    age_mean = df['idade'].mean()
    age_std = df['idade'].std()
    age_median = df['idade'].median()
    age_iqr = df['idade'].quantile([0.25, 0.75])
    print(f"Age: {age_mean:.1f} ± {age_std:.1f} years")
    print(f"     Median: {age_median:.1f} (IQR: {age_iqr[0.25]:.1f}-{age_iqr[0.75]:.1f})")
    
    # Sex distribution
    sex_counts = df['sexo'].value_counts()
    print(f"\nSex:")
    for sex, count in sex_counts.items():
        pct = count / n * 100
        print(f"  {sex}: {count} ({pct:.1f}%)")
    
    # Age groups
    if 'age_group' in df.columns:
        print(f"\nAge groups:")
        for group in ['<18', '18-39', '40-59', '≥60']:
            count = (df['age_group'] == group).sum()
            pct = count / n * 100
            print(f"  {group}: {count} ({pct:.1f}%)")
    
    # Symptoms
    symptom_cols = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'ARTRALGIA', 
                    'EXANTEMA', 'NAUSEA', 'VOMITO']
    
    print(f"\n--- Symptom Frequency ---")
    for col in symptom_cols:
        if col in df.columns:
            count = df[col].sum()
            pct = count / n * 100
            symptom_name = col.replace('_', ' ').title()
            print(f"  {symptom_name}: {count} ({pct:.1f}%)")
    
    # Hospitalization
    if 'hospitalized' in df.columns:
        hosp_count = df['hospitalized'].sum()
        hosp_pct = hosp_count / n * 100
        print(f"\nHospitalization: {hosp_count} ({hosp_pct:.1f}%)")
    
    return {
        'n': n,
        'age_mean': age_mean,
        'age_std': age_std,
        'age_median': age_median,
        'female_pct': (df['sexo'] == 'F').sum() / n * 100
    }


def compare_groups_chi2(df, var, group_var='subgroup'):
    """Perform chi-square test comparing groups."""
    contingency = pd.crosstab(df[group_var], df[var])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    return chi2, p


if __name__ == "__main__":
    print("=" * 60)
    print("DESCRIPTIVE ANALYSIS")
    print("Chikungunya Surveillance Study - Foz do Iguaçu, 2023")
    print("=" * 60)
    
    # Load processed data
    rtpcr_df = pd.read_csv(f'{DATA_PROCESSED}rtpcr_processed.csv')
    sinan_df = pd.read_csv(f'{DATA_PROCESSED}sinan_processed.csv')
    
    # RT-PCR descriptives
    rtpcr_stats = calculate_descriptive_stats(rtpcr_df, "RT-PCR Confirmed Cases")
    
    # SINAN Laboratory
    sinan_lab = sinan_df[sinan_df['sinan_group'] == 'Laboratory']
    sinan_lab_stats = calculate_descriptive_stats(sinan_lab, "SINAN Laboratory Confirmed")
    
    # SINAN Clinical
    sinan_clin = sinan_df[sinan_df['sinan_group'] == 'Clinical-epidemiological']
    sinan_clin_stats = calculate_descriptive_stats(sinan_clin, "SINAN Clinical-Epidemiological")
    
    print("\n" + "=" * 60)
    print("SUMMARY TABLE")
    print("=" * 60)
    print(f"\n{'Variable':<25} {'RT-PCR+':<15} {'SINAN Lab':<15} {'SINAN Clin':<15}")
    print("-" * 70)
    print(f"{'N':<25} {rtpcr_stats['n']:<15} {sinan_lab_stats['n']:<15} {sinan_clin_stats['n']:<15}")
    print(f"{'Age (mean ± SD)':<25} {rtpcr_stats['age_mean']:.1f}±{rtpcr_stats['age_std']:.1f}{'':>5} {sinan_lab_stats['age_mean']:.1f}±{sinan_lab_stats['age_std']:.1f}{'':>5} {sinan_clin_stats['age_mean']:.1f}±{sinan_clin_stats['age_std']:.1f}")
    print(f"{'Female (%)':<25} {rtpcr_stats['female_pct']:.1f}%{'':>10} {sinan_lab_stats['female_pct']:.1f}%{'':>10} {sinan_clin_stats['female_pct']:.1f}%")
    
    print("\n✓ Descriptive analysis complete!")
