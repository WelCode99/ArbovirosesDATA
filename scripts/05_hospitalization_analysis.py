#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_hospitalization_analysis.py
==============================
Analysis of hospitalization rates and risk factors.

Author: Welisson G.N. Costa
Date: January 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.proportion import proportion_confint
import warnings
warnings.filterwarnings('ignore')

DATA_PROCESSED = '../data/processed/'

def analyze_hospitalization_by_group(merged_df):
    """Analyze hospitalization rates by diagnostic group."""
    print("\n" + "=" * 60)
    print("HOSPITALIZATION RATES BY GROUP")
    print("=" * 60)
    
    results = []
    
    print(f"\n{'Group':<35} {'N':<7} {'Hosp':<7} {'Rate':<8} {'95% CI'}")
    print("-" * 70)
    
    for group in merged_df['subgroup'].unique():
        data = merged_df[merged_df['subgroup'] == group]
        n = len(data)
        hosp = data['hospitalized'].sum()
        rate = hosp / n * 100
        ci_low, ci_high = proportion_confint(hosp, n, method='wilson')
        
        results.append({
            'group': group,
            'n': n,
            'hospitalized': hosp,
            'rate': rate,
            'ci_low': ci_low * 100,
            'ci_high': ci_high * 100
        })
        
        print(f"{group:<35} {n:<7} {hosp:<7} {rate:>5.1f}%   [{ci_low*100:.1f}-{ci_high*100:.1f}%]")
    
    # Pairwise comparisons
    print("\n--- Pairwise Comparisons ---")
    groups = merged_df['subgroup'].unique()
    
    for i in range(len(groups)):
        for j in range(i+1, len(groups)):
            g1, g2 = groups[i], groups[j]
            d1 = merged_df[merged_df['subgroup'] == g1]
            d2 = merged_df[merged_df['subgroup'] == g2]
            
            # Z-test for proportions
            n1, x1 = len(d1), d1['hospitalized'].sum()
            n2, x2 = len(d2), d2['hospitalized'].sum()
            
            p1, p2 = x1/n1, x2/n2
            p_pool = (x1 + x2) / (n1 + n2)
            
            if p_pool > 0 and p_pool < 1:
                se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
                z = (p1 - p2) / se
                p_val = 2 * (1 - stats.norm.cdf(abs(z)))
                
                sig = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else ''
                
                short1 = g1.replace('SINAN ', '').replace('RT-PCR Confirmed', 'RT-PCR+')[:15]
                short2 = g2.replace('SINAN ', '').replace('RT-PCR Confirmed', 'RT-PCR+')[:15]
                print(f"  {short1} vs {short2}: z = {z:.2f}, p = {p_val:.4f} {sig}")
    
    return results


def analyze_risk_factors(rtpcr_df):
    """Analyze risk factors for hospitalization in RT-PCR+ cases."""
    print("\n" + "=" * 60)
    print("RISK FACTORS FOR HOSPITALIZATION (RT-PCR+ Cases)")
    print("=" * 60)
    
    # Univariate analysis
    print("\n--- Univariate Analysis ---")
    
    factors = {
        'age_60plus': (rtpcr_df['idade'] >= 60).astype(int),
        'female': (rtpcr_df['sexo'] == 'F').astype(int),
        'ARTRALGIA': rtpcr_df['ARTRALGIA'] if 'ARTRALGIA' in rtpcr_df.columns else None,
        'FEBRE': rtpcr_df['FEBRE'] if 'FEBRE' in rtpcr_df.columns else None,
        'VOMITO': rtpcr_df['VOMITO'] if 'VOMITO' in rtpcr_df.columns else None,
        'NAUSEA': rtpcr_df['NAUSEA'] if 'NAUSEA' in rtpcr_df.columns else None,
    }
    
    print(f"\n{'Factor':<20} {'OR':<8} {'95% CI':<15} {'p-value'}")
    print("-" * 50)
    
    univariate_results = []
    
    for name, factor in factors.items():
        if factor is None:
            continue
        
        table = pd.crosstab(factor, rtpcr_df['hospitalized'])
        
        if table.shape != (2, 2):
            continue
        
        try:
            a, b = table.iloc[1, 1], table.iloc[1, 0]
            c, d = table.iloc[0, 1], table.iloc[0, 0]
            
            if min(a, b, c, d) == 0:
                # Add 0.5 correction
                a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
            
            or_val = (a * d) / (b * c)
            se_log = np.sqrt(1/a + 1/b + 1/c + 1/d)
            ci_low = np.exp(np.log(or_val) - 1.96 * se_log)
            ci_high = np.exp(np.log(or_val) + 1.96 * se_log)
            
            chi2, p, dof, exp = stats.chi2_contingency(table)
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            
            univariate_results.append({
                'factor': name,
                'or': or_val,
                'ci_low': ci_low,
                'ci_high': ci_high,
                'p': p
            })
            
            print(f"{name:<20} {or_val:>6.2f}   [{ci_low:>5.2f}-{ci_high:>5.2f}]   {p:.4f} {sig}")
            
        except Exception as e:
            continue
    
    # Multivariate analysis
    print("\n--- Multivariate Logistic Regression ---")
    
    rtpcr_df['age_60plus'] = (rtpcr_df['idade'] >= 60).astype(int)
    rtpcr_df['female'] = (rtpcr_df['sexo'] == 'F').astype(int)
    
    predictors = ['age_60plus', 'female', 'VOMITO']
    available = [p for p in predictors if p in rtpcr_df.columns]
    
    try:
        X = rtpcr_df[available].fillna(0)
        X = sm.add_constant(X)
        y = rtpcr_df['hospitalized']
        
        model = sm.Logit(y, X)
        result = model.fit(disp=0)
        
        print(f"\n{'Variable':<15} {'aOR':<8} {'95% CI':<15} {'p-value'}")
        print("-" * 50)
        
        conf = result.conf_int()
        for var in available:
            coef = result.params[var]
            aor = np.exp(coef)
            ci_low = np.exp(conf.loc[var, 0])
            ci_high = np.exp(conf.loc[var, 1])
            p = result.pvalues[var]
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            
            print(f"{var:<15} {aor:>6.2f}   [{ci_low:>5.2f}-{ci_high:>5.2f}]   {p:.4f} {sig}")
            
    except Exception as e:
        print(f"Model error: {e}")
    
    return univariate_results


if __name__ == "__main__":
    print("=" * 60)
    print("HOSPITALIZATION ANALYSIS")
    print("Chikungunya Surveillance Study")
    print("=" * 60)
    
    # Load data
    merged_df = pd.read_csv(f'{DATA_PROCESSED}merged_analysis_dataset.csv')
    rtpcr_df = pd.read_csv(f'{DATA_PROCESSED}rtpcr_processed.csv')
    
    # Analysis
    hosp_results = analyze_hospitalization_by_group(merged_df)
    risk_results = analyze_risk_factors(rtpcr_df)
    
    print("\n✓ Hospitalization analysis complete!")
