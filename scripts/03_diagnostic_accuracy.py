#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_diagnostic_accuracy.py
=========================
Analysis of initial clinical diagnostic accuracy.

This script evaluates:
1. Distribution of initial diagnostic hypotheses
2. Factors associated with correct diagnosis
3. Odds ratios for diagnostic accuracy by symptom

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

def analyze_diagnostic_hypotheses(df):
    """Analyze distribution of initial diagnostic hypotheses."""
    print("\n" + "=" * 60)
    print("INITIAL DIAGNOSTIC HYPOTHESES")
    print("=" * 60)
    
    n = len(df)
    
    # Categorize diagnoses
    def categorize_diagnosis(dx):
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
    
    df['dx_category'] = df['HIPOTESE_DIAGNOSTICA'].apply(categorize_diagnosis)
    
    print(f"\nDistribution of Initial Diagnoses (n={n}):")
    print("-" * 45)
    
    categories = ['Dengue only', 'Dengue or Chikungunya', 'Chikungunya only', 'Other']
    results = {}
    
    for cat in categories:
        count = (df['dx_category'] == cat).sum()
        pct = count / n * 100
        ci_low, ci_high = proportion_confint(count, n, method='wilson')
        results[cat] = {'count': count, 'pct': pct, 'ci': (ci_low*100, ci_high*100)}
        print(f"  {cat:<25}: {count:>4} ({pct:>5.1f}%) [95% CI: {ci_low*100:.1f}-{ci_high*100:.1f}%]")
    
    # Overall accuracy
    correct = (df['diagnostic_correct'] == 1).sum()
    accuracy = correct / n * 100
    ci_low, ci_high = proportion_confint(correct, n, method='wilson')
    
    print(f"\n{'='*45}")
    print(f"Overall Diagnostic Accuracy (including Chikungunya):")
    print(f"  Correct: {correct}/{n} ({accuracy:.1f}%) [95% CI: {ci_low*100:.1f}-{ci_high*100:.1f}%]")
    
    # Chikungunya-specific accuracy
    chik_only = (df['dx_category'] == 'Chikungunya only').sum()
    chik_accuracy = chik_only / n * 100
    ci_low_c, ci_high_c = proportion_confint(chik_only, n, method='wilson')
    print(f"\nChikungunya as sole diagnosis:")
    print(f"  Correct: {chik_only}/{n} ({chik_accuracy:.1f}%) [95% CI: {ci_low_c*100:.1f}-{ci_high_c*100:.1f}%]")
    
    return df, results


def analyze_factors_accuracy(df):
    """Analyze factors associated with correct diagnosis."""
    print("\n" + "=" * 60)
    print("FACTORS ASSOCIATED WITH CORRECT DIAGNOSIS")
    print("=" * 60)
    
    symptoms = ['ARTRALGIA', 'CEFALEIA', 'FEBRE', 'MIALGIA', 'EXANTEMA', 
                'NAUSEA', 'VOMITO', 'EDEMA', 'ASTENIA', 'DOR_RETRO_ORBITAL']
    
    results = []
    
    print(f"\n{'Factor':<20} {'OR':<8} {'95% CI':<15} {'p-value':<10}")
    print("-" * 55)
    
    for symptom in symptoms:
        if symptom not in df.columns:
            continue
            
        # Create contingency table
        table = pd.crosstab(df[symptom], df['diagnostic_correct'])
        
        if table.shape != (2, 2):
            continue
        
        # Calculate OR
        try:
            a, b = table.iloc[1, 1], table.iloc[1, 0]  # symptom present
            c, d = table.iloc[0, 1], table.iloc[0, 0]  # symptom absent
            
            if b * c == 0:
                continue
                
            odds_ratio = (a * d) / (b * c)
            
            # 95% CI using log transformation
            se_log_or = np.sqrt(1/a + 1/b + 1/c + 1/d)
            ci_low = np.exp(np.log(odds_ratio) - 1.96 * se_log_or)
            ci_high = np.exp(np.log(odds_ratio) + 1.96 * se_log_or)
            
            # Chi-square test
            chi2, p, dof, expected = stats.chi2_contingency(table)
            
            significance = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            
            results.append({
                'factor': symptom,
                'or': odds_ratio,
                'ci_low': ci_low,
                'ci_high': ci_high,
                'p': p
            })
            
            print(f"{symptom:<20} {odds_ratio:>6.2f}   [{ci_low:>5.2f}-{ci_high:>5.2f}]   {p:>8.4f} {significance}")
            
        except Exception as e:
            continue
    
    # Tourniquet test
    if 'PROVA_LACO' in df.columns:
        df['laco_positive'] = df['PROVA_LACO'].str.contains('POSITIV', case=False, na=False).astype(int)
        table = pd.crosstab(df['laco_positive'], df['diagnostic_correct'])
        
        if table.shape == (2, 2):
            a, b = table.iloc[1, 1], table.iloc[1, 0]
            c, d = table.iloc[0, 1], table.iloc[0, 0]
            
            if b * c > 0:
                odds_ratio = (a * d) / (b * c)
                se_log_or = np.sqrt(1/max(a,1) + 1/max(b,1) + 1/max(c,1) + 1/max(d,1))
                ci_low = np.exp(np.log(odds_ratio) - 1.96 * se_log_or)
                ci_high = np.exp(np.log(odds_ratio) + 1.96 * se_log_or)
                chi2, p, dof, expected = stats.chi2_contingency(table)
                
                significance = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
                print(f"{'Tourniquet +':<20} {odds_ratio:>6.2f}   [{ci_low:>5.2f}-{ci_high:>5.2f}]   {p:>8.4f} {significance}")
    
    print("\n* p<0.05, ** p<0.01, *** p<0.001")
    
    return results


def multivariate_logistic_regression(df):
    """Multivariate logistic regression for diagnostic accuracy."""
    print("\n" + "=" * 60)
    print("MULTIVARIATE LOGISTIC REGRESSION")
    print("=" * 60)
    
    # Prepare variables
    predictors = ['ARTRALGIA', 'CEFALEIA', 'FEBRE', 'MIALGIA', 'EXANTEMA']
    available_predictors = [p for p in predictors if p in df.columns]
    
    X = df[available_predictors].fillna(0)
    X = sm.add_constant(X)
    y = df['diagnostic_correct']
    
    try:
        model = sm.Logit(y, X)
        result = model.fit(disp=0)
        
        print(f"\nModel Summary:")
        print(f"  Pseudo R-squared: {result.prsquared:.3f}")
        print(f"  Log-Likelihood: {result.llf:.2f}")
        print(f"  AIC: {result.aic:.2f}")
        
        print(f"\n{'Variable':<15} {'Coef':<8} {'OR':<8} {'95% CI':<15} {'p-value':<10}")
        print("-" * 60)
        
        conf = result.conf_int()
        for var in available_predictors:
            coef = result.params[var]
            or_val = np.exp(coef)
            ci_low = np.exp(conf.loc[var, 0])
            ci_high = np.exp(conf.loc[var, 1])
            p = result.pvalues[var]
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            print(f"{var:<15} {coef:>7.3f}  {or_val:>6.2f}   [{ci_low:>5.2f}-{ci_high:>5.2f}]   {p:>8.4f} {sig}")
        
        return result
        
    except Exception as e:
        print(f"Model fitting error: {e}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("DIAGNOSTIC ACCURACY ANALYSIS")
    print("Chikungunya Surveillance Study - Foz do Iguaçu, 2023")
    print("=" * 60)
    
    # Load data
    rtpcr_df = pd.read_csv(f'{DATA_PROCESSED}rtpcr_processed.csv')
    
    # Analysis
    rtpcr_df, hypothesis_results = analyze_diagnostic_hypotheses(rtpcr_df)
    or_results = analyze_factors_accuracy(rtpcr_df)
    model_result = multivariate_logistic_regression(rtpcr_df)
    
    print("\n" + "=" * 60)
    print("✓ Diagnostic accuracy analysis complete!")
