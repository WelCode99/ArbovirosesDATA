#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06_cluster_analysis.py
======================
Symptom clustering analysis using hierarchical clustering.

Author: Welisson G.N. Costa
Date: January 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

DATA_PROCESSED = '../data/processed/'

def perform_cluster_analysis(rtpcr_df):
    """Perform hierarchical clustering on symptom patterns."""
    print("\n" + "=" * 60)
    print("SYMPTOM CLUSTER ANALYSIS")
    print("=" * 60)
    
    # Select symptom variables
    symptoms = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'ARTRALGIA', 
                'EXANTEMA', 'NAUSEA', 'VOMITO']
    
    available_symptoms = [s for s in symptoms if s in rtpcr_df.columns]
    
    # Prepare data matrix
    X = rtpcr_df[available_symptoms].fillna(0).values
    
    print(f"\nUsing {len(available_symptoms)} symptom variables:")
    for s in available_symptoms:
        print(f"  - {s}")
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Hierarchical clustering
    print("\nPerforming hierarchical clustering (Ward's method)...")
    linkage_matrix = linkage(X_scaled, method='ward')
    
    # Determine optimal number of clusters (3 based on domain knowledge)
    n_clusters = 3
    clusters = fcluster(linkage_matrix, n_clusters, criterion='maxclust')
    rtpcr_df['cluster'] = clusters
    
    # Analyze cluster profiles
    print(f"\n--- Cluster Profiles (n={len(rtpcr_df)}) ---")
    
    cluster_profiles = []
    
    for i in range(1, n_clusters + 1):
        cluster_data = rtpcr_df[rtpcr_df['cluster'] == i]
        n = len(cluster_data)
        pct = n / len(rtpcr_df) * 100
        
        profile = {'cluster': i, 'n': n, 'pct': pct}
        
        print(f"\nCluster {i}: n={n} ({pct:.1f}%)")
        print(f"  Symptom frequencies:")
        
        for symptom in available_symptoms:
            freq = cluster_data[symptom].mean() * 100
            profile[symptom] = freq
            bar = '█' * int(freq / 5) + '░' * (20 - int(freq / 5))
            print(f"    {symptom:<12}: {bar} {freq:>5.1f}%")
        
        cluster_profiles.append(profile)
    
    # Identify cluster characteristics
    print("\n--- Cluster Interpretation ---")
    
    for profile in cluster_profiles:
        i = profile['cluster']
        dominant = []
        for symptom in available_symptoms:
            if profile[symptom] > 70:
                dominant.append(symptom)
        
        if 'FEBRE' in dominant and 'MIALGIA' in dominant and 'CEFALEIA' in dominant:
            print(f"  Cluster {i}: Classical Triad (Fever-Myalgia-Headache)")
        elif 'ARTRALGIA' in dominant:
            print(f"  Cluster {i}: Articular Profile")
        elif 'NAUSEA' in dominant or 'VOMITO' in dominant:
            print(f"  Cluster {i}: Gastrointestinal Profile")
        else:
            print(f"  Cluster {i}: Mixed Profile")
    
    # Chi-square test for cluster distribution
    print("\n--- Statistical Comparison ---")
    
    for symptom in available_symptoms:
        contingency = pd.crosstab(rtpcr_df['cluster'], rtpcr_df[symptom])
        chi2, p, dof, expected = stats.chi2_contingency(contingency)
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
        print(f"  {symptom:<12}: χ² = {chi2:>7.2f}, p = {p:.4f} {sig}")
    
    return rtpcr_df, cluster_profiles


def analyze_cluster_outcomes(rtpcr_df):
    """Analyze outcomes by cluster."""
    print("\n" + "=" * 60)
    print("OUTCOMES BY CLUSTER")
    print("=" * 60)
    
    print(f"\n{'Cluster':<10} {'N':<8} {'Hosp':<8} {'Rate':<10}")
    print("-" * 40)
    
    for cluster in sorted(rtpcr_df['cluster'].unique()):
        data = rtpcr_df[rtpcr_df['cluster'] == cluster]
        n = len(data)
        hosp = data['hospitalized'].sum()
        rate = hosp / n * 100 if n > 0 else 0
        print(f"{cluster:<10} {n:<8} {hosp:<8} {rate:>5.1f}%")
    
    # Chi-square test
    contingency = pd.crosstab(rtpcr_df['cluster'], rtpcr_df['hospitalized'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    print(f"\nChi-square: {chi2:.2f}, p = {p:.4f}")


if __name__ == "__main__":
    print("=" * 60)
    print("CLUSTER ANALYSIS")
    print("Symptom Pattern Identification")
    print("=" * 60)
    
    # Load data
    rtpcr_df = pd.read_csv(f'{DATA_PROCESSED}rtpcr_processed.csv')
    
    # Analysis
    rtpcr_df, profiles = perform_cluster_analysis(rtpcr_df)
    analyze_cluster_outcomes(rtpcr_df)
    
    # Save with cluster assignments
    rtpcr_df.to_csv(f'{DATA_PROCESSED}rtpcr_with_clusters.csv', index=False)
    
    print("\n✓ Cluster analysis complete!")
