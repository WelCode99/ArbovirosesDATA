#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07_selection_bias_analysis.py
=============================
Analysis of selection bias for PCR testing.

Author: Welisson G.N. Costa
Date: January 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

DATA_PROCESSED = '../data/processed/'

def analyze_selection_bias(sinan_df):
    """Analyze selection bias for PCR testing in SINAN data."""
    print("\n" + "=" * 60)
    print("SELECTION BIAS ANALYSIS")
    print("=" * 60)
    
    # Create PCR tested indicator
    sinan_df['pcr_tested'] = (sinan_df['sinan_group'] == 'Laboratory').astype(int)
    
    n_total = len(sinan_df)
    n_tested = sinan_df['pcr_tested'].sum()
    
    print(f"\nSample: n = {n_total}")
    print(f"PCR tested: {n_tested} ({n_tested/n_total*100:.1f}%)")
    
    # Factors associated with PCR testing
    print("\n--- Factors Associated with PCR Testing ---")
    
    symptoms = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'ARTRALGIA', 
                'EXANTEMA', 'NAUSEA', 'VOMITO']
    
    print(f"\n{'Factor':<15} {'Tested %':<12} {'Not Tested %':<15} {'OR':<8} {'p-value'}")
    print("-" * 65)
    
    results = []
    
    for symptom in symptoms:
        if symptom not in sinan_df.columns:
            continue
        
        tested = sinan_df[sinan_df['pcr_tested'] == 1]
        not_tested = sinan_df[sinan_df['pcr_tested'] == 0]
        
        freq_tested = tested[symptom].mean() * 100
        freq_not_tested = not_tested[symptom].mean() * 100
        
        # Chi-square and OR
        table = pd.crosstab(sinan_df[symptom], sinan_df['pcr_tested'])
        
        if table.shape == (2, 2):
            a, b = table.iloc[1, 1], table.iloc[1, 0]
            c, d = table.iloc[0, 1], table.iloc[0, 0]
            
            if b * c > 0:
                or_val = (a * d) / (b * c)
                chi2, p, dof, exp = stats.chi2_contingency(table)
                sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
                
                results.append({
                    'factor': symptom,
                    'freq_tested': freq_tested,
                    'freq_not_tested': freq_not_tested,
                    'or': or_val,
                    'p': p
                })
                
                print(f"{symptom:<15} {freq_tested:>5.1f}%{'':>5} {freq_not_tested:>5.1f}%{'':>8} {or_val:>6.2f}   {p:.4f} {sig}")
    
    # Hospitalization as predictor of testing
    print("\n--- Hospitalization and Testing ---")
    
    table = pd.crosstab(sinan_df['hospitalized'], sinan_df['pcr_tested'])
    if table.shape == (2, 2):
        a, b = table.iloc[1, 1], table.iloc[1, 0]
        c, d = table.iloc[0, 1], table.iloc[0, 0]
        
        if b * c > 0:
            or_val = (a * d) / (b * c)
            chi2, p, dof, exp = stats.chi2_contingency(table)
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            
            print(f"Hospitalized patients more likely to be PCR tested:")
            print(f"  OR = {or_val:.2f}, p = {p:.4f} {sig}")
    
    return results


def propensity_score_analysis(sinan_df):
    """Propensity score analysis for PCR testing."""
    print("\n" + "=" * 60)
    print("PROPENSITY SCORE MODEL")
    print("=" * 60)
    
    sinan_df['pcr_tested'] = (sinan_df['sinan_group'] == 'Laboratory').astype(int)
    
    # Predictors
    predictors = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'ARTRALGIA', 'hospitalized']
    available = [p for p in predictors if p in sinan_df.columns]
    
    try:
        X = sinan_df[available].fillna(0)
        X = sm.add_constant(X)
        y = sinan_df['pcr_tested']
        
        model = sm.Logit(y, X)
        result = model.fit(disp=0)
        
        print(f"\nModel fit:")
        print(f"  Pseudo R²: {result.prsquared:.3f}")
        print(f"  AIC: {result.aic:.2f}")
        
        print(f"\n{'Variable':<15} {'Coef':<8} {'OR':<8} {'p-value'}")
        print("-" * 45)
        
        for var in available:
            coef = result.params[var]
            or_val = np.exp(coef)
            p = result.pvalues[var]
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            print(f"{var:<15} {coef:>7.3f}  {or_val:>6.2f}   {p:.4f} {sig}")
        
        # Calculate propensity scores
        sinan_df['propensity_score'] = result.predict(X)
        
        print(f"\nPropensity score distribution:")
        print(f"  Mean: {sinan_df['propensity_score'].mean():.3f}")
        print(f"  Std:  {sinan_df['propensity_score'].std():.3f}")
        print(f"  Range: {sinan_df['propensity_score'].min():.3f} - {sinan_df['propensity_score'].max():.3f}")
        
        return result
        
    except Exception as e:
        print(f"Model error: {e}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("SELECTION BIAS ANALYSIS")
    print("Propensity for PCR Testing")
    print("=" * 60)
    
    # Load data
    sinan_df = pd.read_csv(f'{DATA_PROCESSED}sinan_processed.csv')
    
    # Analysis
    bias_results = analyze_selection_bias(sinan_df)
    propensity_model = propensity_score_analysis(sinan_df)
    
    print("\n✓ Selection bias analysis complete!")
