#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_comparative_analysis.py
==========================
Comparative analysis between RT-PCR+ cases and SINAN subgroups.

Author: Welisson G.N. Costa
Date: January 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
import warnings
warnings.filterwarnings('ignore')

DATA_PROCESSED = '../data/processed/'

def compare_symptom_frequencies(merged_df):
    """Compare symptom frequencies across groups."""
    print("\n" + "=" * 60)
    print("SYMPTOM FREQUENCY COMPARISON")
    print("=" * 60)
    
    symptoms = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'ARTRALGIA', 'EXANTEMA', 'NAUSEA', 'VOMITO']
    groups = merged_df['subgroup'].unique()
    
    results = []
    
    print(f"\n{'Symptom':<12}", end='')
    for group in groups:
        short_name = group.replace('SINAN ', '').replace('RT-PCR Confirmed', 'RT-PCR+')[:12]
        print(f" {short_name:<12}", end='')
    print(f" {'χ²':<8} {'p-value':<10}")
    print("-" * 80)
    
    for symptom in symptoms:
        if symptom not in merged_df.columns:
            continue
            
        print(f"{symptom:<12}", end='')
        
        freqs = []
        for group in groups:
            group_data = merged_df[merged_df['subgroup'] == group]
            n = len(group_data)
            count = group_data[symptom].sum()
            pct = count / n * 100 if n > 0 else 0
            freqs.append(pct)
            print(f" {pct:>5.1f}%{'':>5}", end='')
        
        # Chi-square test
        contingency = pd.crosstab(merged_df['subgroup'], merged_df[symptom])
        chi2, p, dof, expected = stats.chi2_contingency(contingency)
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
        
        print(f" {chi2:>7.2f}  {p:>8.4f} {sig}")
        
        results.append({
            'symptom': symptom,
            'chi2': chi2,
            'p': p,
            'frequencies': dict(zip(groups, freqs))
        })
    
    print("\n* p<0.05, ** p<0.01, *** p<0.001")
    return results


def compare_demographics(merged_df):
    """Compare demographic characteristics across groups."""
    print("\n" + "=" * 60)
    print("DEMOGRAPHIC COMPARISON")
    print("=" * 60)
    
    groups = merged_df['subgroup'].unique()
    
    # Age comparison
    print("\nAge by Group:")
    age_data = []
    for group in groups:
        group_data = merged_df[merged_df['subgroup'] == group]['idade']
        mean = group_data.mean()
        std = group_data.std()
        median = group_data.median()
        age_data.append(group_data.values)
        short_name = group.replace('SINAN ', '').replace('RT-PCR Confirmed', 'RT-PCR+')[:20]
        print(f"  {short_name:<25}: {mean:.1f} ± {std:.1f} (median: {median:.1f})")
    
    # Kruskal-Wallis test
    h_stat, p_val = stats.kruskal(*age_data)
    print(f"\nKruskal-Wallis H: {h_stat:.2f}, p = {p_val:.4f}")
    
    # Sex comparison
    print("\nSex Distribution (% Female):")
    for group in groups:
        group_data = merged_df[merged_df['subgroup'] == group]
        female_pct = (group_data['sexo'] == 'F').sum() / len(group_data) * 100
        short_name = group.replace('SINAN ', '').replace('RT-PCR Confirmed', 'RT-PCR+')[:20]
        print(f"  {short_name:<25}: {female_pct:.1f}%")
    
    contingency = pd.crosstab(merged_df['subgroup'], merged_df['sexo'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    print(f"\nChi-square: {chi2:.2f}, p = {p:.4f}")


def compare_hospitalization_rates(merged_df):
    """Compare hospitalization rates across groups."""
    print("\n" + "=" * 60)
    print("HOSPITALIZATION COMPARISON")
    print("=" * 60)
    
    groups = merged_df['subgroup'].unique()
    
    print(f"\n{'Group':<30} {'N':<8} {'Hosp':<8} {'Rate':<10} {'95% CI':<15}")
    print("-" * 75)
    
    for group in groups:
        group_data = merged_df[merged_df['subgroup'] == group]
        n = len(group_data)
        hosp = group_data['hospitalized'].sum()
        rate = hosp / n * 100
        ci_low, ci_high = proportion_confint(hosp, n, method='wilson')
        
        short_name = group.replace('SINAN ', '').replace('RT-PCR Confirmed', 'RT-PCR+')[:28]
        print(f"{short_name:<30} {n:<8} {hosp:<8} {rate:>5.1f}%{'':>3} [{ci_low*100:.1f}-{ci_high*100:.1f}%]")
    
    # Chi-square test
    contingency = pd.crosstab(merged_df['subgroup'], merged_df['hospitalized'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
    print(f"\nChi-square: {chi2:.2f}, p = {p:.4f} {sig}")


if __name__ == "__main__":
    print("=" * 60)
    print("COMPARATIVE ANALYSIS")
    print("RT-PCR+ vs SINAN Subgroups")
    print("=" * 60)
    
    # Load data
    merged_df = pd.read_csv(f'{DATA_PROCESSED}merged_analysis_dataset.csv')
    
    # Run comparisons
    compare_demographics(merged_df)
    symptom_results = compare_symptom_frequencies(merged_df)
    compare_hospitalization_rates(merged_df)
    
    print("\n✓ Comparative analysis complete!")
