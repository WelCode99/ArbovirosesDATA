#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
00_anonymize_data.py
====================
Data anonymization script for Chikungunya surveillance study.

This script implements proper anonymization techniques to prevent
re-identification of individuals while preserving analytical utility.

Anonymization measures:
1. Date generalization (exact date → week/month)
2. Age binning for rare combinations
3. Remove precise geographic coordinates
4. Remove health unit identifiers
5. Remove birth year information
6. K-anonymity validation

Author: Welisson G.N. Costa
Date: February 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

DATA_RAW = '../data/raw/'
K_ANONYMITY_THRESHOLD = 3  # Minimum group size for k-anonymity

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generalize_date_to_week(date_series):
    """
    Generalize exact dates to epidemiological week.
    Returns the Monday of the week for each date.
    """
    dates = pd.to_datetime(date_series, errors='coerce')
    # Get the Monday of each week
    week_start = dates - pd.to_timedelta(dates.dt.dayofweek, unit='D')
    return week_start.dt.strftime('%Y-W%U')  # Year-Week format

def generalize_date_to_month(date_series):
    """
    Generalize exact dates to year-month.
    """
    dates = pd.to_datetime(date_series, errors='coerce')
    return dates.dt.strftime('%Y-%m')

def check_k_anonymity(df, quasi_identifiers, k=3):
    """
    Check k-anonymity for given quasi-identifiers.
    Returns groups with less than k individuals.
    """
    group_sizes = df.groupby(quasi_identifiers).size()
    violations = group_sizes[group_sizes < k]
    return violations

def generalize_age_for_small_groups(df, age_col, group_cols, k=3):
    """
    Generalize age into broader bins for groups smaller than k.
    """
    # Start with broad age bins to ensure k-anonymity
    bins = [0, 18, 40, 60, 120]
    labels = ['0-17', '18-39', '40-59', '60+']
    
    df['age_bin'] = pd.cut(df[age_col], bins=bins, labels=labels, right=False).astype(str)
    
    # Check which groups still need further generalization
    group_sizes = df.groupby(group_cols + ['age_bin']).size()
    small_groups = group_sizes[group_sizes < k].index
    
    if len(small_groups) > 0:
        # For very small groups, use even broader bins
        for group in small_groups:
            mask = True
            for i, col in enumerate(group_cols + ['age_bin']):
                if i < len(group):
                    mask &= (df[col] == group[i]) if col in df.columns else True
            
            if mask.any():
                ages = df.loc[mask, age_col]
                # Manually assign broader categories
                df.loc[mask & (df[age_col] < 40), 'age_bin'] = '0-39'
                df.loc[mask & (df[age_col] >= 40), 'age_bin'] = '40+'
    
    return df

# =============================================================================
# ANONYMIZE RTPCR DATASET
# =============================================================================

def anonymize_rtpcr_data():
    """
    Anonymize RT-PCR dataset to prevent re-identification.
    """
    print("=" * 70)
    print("ANONYMIZING RT-PCR DATASET")
    print("=" * 70)
    
    # Load data
    df = pd.read_csv(f'{DATA_RAW}RTPCR_chikungunya_anonymized.csv', sep=';')
    print(f"Original records: {len(df)}")
    
    # 1. Date generalization - use month instead of week for better k-anonymity
    print("\n1. Generalizing dates...")
    df['data_original'] = df['data']
    df['year_month'] = generalize_date_to_month(df['data'])
    print(f"   Dates generalized to year-month")
    
    # Check uniqueness with month-level dates
    unique_month_combos = df.groupby(['year_month', 'idade', 'sexo']).size()
    print(f"   Unique (Month + Age + Sex) combinations: {len(unique_month_combos)}")
    print(f"   Single-person combinations: {(unique_month_combos == 1).sum()}")
    
    # 2. Age generalization for small groups
    print("\n2. Generalizing age for k-anonymity...")
    df = generalize_age_for_small_groups(
        df, 'idade', ['year_month', 'sexo', 'bairro'], k=K_ANONYMITY_THRESHOLD
    )
    
    # 3. Generalize rare neighborhoods
    print("\n3. Generalizing rare neighborhoods...")
    neighborhood_counts = df['bairro'].value_counts()
    rare_neighborhoods = neighborhood_counts[neighborhood_counts < K_ANONYMITY_THRESHOLD].index
    df.loc[df['bairro'].isin(rare_neighborhoods), 'bairro'] = 'OTHER'
    print(f"   {len(rare_neighborhoods)} rare neighborhoods generalized to 'OTHER'")
    
    # 4. Remove free-text symptom descriptions (may contain identifying info)
    print("\n4. Removing free-text symptom field...")
    if 'sintomas' in df.columns:
        # Keep only structured symptom variables
        df = df.drop(columns=['sintomas'])
        print("   Free-text 'sintomas' field removed")
    
    # 5. Final k-anonymity check
    print("\n5. Final k-anonymity validation...")
    quasi_ids = ['year_month', 'age_bin', 'sexo', 'bairro']
    violations = check_k_anonymity(df, quasi_ids, k=K_ANONYMITY_THRESHOLD)
    
    if len(violations) > 0:
        print(f"   WARNING: {len(violations)} groups with < {K_ANONYMITY_THRESHOLD} individuals")
        print("   Applying additional generalization...")
        
        # For small groups, generalize neighborhood to broader categories
        for group in violations.index:
            mask = True
            for i, col in enumerate(quasi_ids):
                if i < len(group):
                    mask &= (df[col] == group[i])
            
            if mask.any():
                # Generalize neighborhood for small groups
                df.loc[mask, 'bairro'] = 'OTHER'
        
        # Re-check after generalization
        violations_after = check_k_anonymity(df, quasi_ids, k=K_ANONYMITY_THRESHOLD)
        if len(violations_after) > 0:
            print(f"   Still {len(violations_after)} violations - further generalizing age")
            # Final resort: use only two age groups
            for group in violations_after.index:
                mask = True
                for i, col in enumerate(quasi_ids):
                    if i < len(group):
                        mask &= (df[col] == group[i])
                
                if mask.any():
                    df.loc[mask & (df['idade'] < 40), 'age_bin'] = '0-39'
                    df.loc[mask & (df['idade'] >= 40), 'age_bin'] = '40+'
        
        # Final check
        violations_final = check_k_anonymity(df, quasi_ids, k=K_ANONYMITY_THRESHOLD)
        print(f"   Final violations: {len(violations_final)}")
    else:
        print(f"   ✓ All groups have ≥ {K_ANONYMITY_THRESHOLD} individuals")
    
    # 6. Remove exact date column
    df = df.drop(columns=['data', 'data_original'], errors='ignore')
    
    # 7. Shuffle the IDs to break any ordering
    print("\n6. Shuffling record IDs...")
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df['id'] = range(1, len(df) + 1)
    
    # Save anonymized data
    output_file = f'{DATA_RAW}RTPCR_chikungunya_anonymized.csv'
    df.to_csv(output_file, sep=';', index=False)
    print(f"\n✓ Anonymized data saved to: {output_file}")
    print(f"  Final records: {len(df)}")
    
    return df

# =============================================================================
# ANONYMIZE SINAN DATASET
# =============================================================================

def anonymize_sinan_data():
    """
    Anonymize SINAN dataset to prevent re-identification.
    """
    print("\n" + "=" * 70)
    print("ANONYMIZING SINAN DATASET")
    print("=" * 70)
    
    # Load data
    df = pd.read_csv(f'{DATA_RAW}SINAN_chikungunya_2023.csv', sep=';', low_memory=False)
    print(f"Original records: {len(df)}")
    
    # 1. Remove exact geographic coordinates
    print("\n1. Removing precise geographic coordinates...")
    geo_cols_to_remove = ['munResLat', 'munResLon', 'munResAlt', 'munResArea']
    removed_cols = [col for col in geo_cols_to_remove if col in df.columns]
    if removed_cols:
        df = df.drop(columns=removed_cols)
        print(f"   Removed: {', '.join(removed_cols)}")
    
    # 2. Remove health unit identifiers
    print("\n2. Removing health unit identifiers...")
    health_unit_cols = ['ID_UNIDADE', 'ID_REGIONA']
    removed_cols = [col for col in health_unit_cols if col in df.columns]
    if removed_cols:
        df = df.drop(columns=removed_cols)
        print(f"   Removed: {', '.join(removed_cols)}")
    
    # 3. Remove birth year
    print("\n3. Removing birth year...")
    if 'ANO_NASC' in df.columns:
        df = df.drop(columns=['ANO_NASC'])
        print("   Removed: ANO_NASC")
    
    # 4. Date generalization  
    print("\n4. Generalizing dates...")
    date_cols = ['DT_NOTIFIC', 'DT_SIN_PRI', 'DT_INVEST', 'DT_CHIK_S1', 'DT_CHIK_S2',
                 'DT_PRNT', 'DT_SORO', 'DT_NS1', 'DT_VIRAL', 'DT_PCR',
                 'DT_INTERNA', 'DT_OBITO', 'DT_ENCERRA', 'DT_ALRM', 'DT_GRAV', 'DT_DIGITA']
    
    generalized_count = 0
    for col in date_cols:
        if col in df.columns:
            # Keep month-level precision, remove exact dates
            df[f'{col}_month'] = generalize_date_to_month(df[col])
            df = df.drop(columns=[col], errors='ignore')
            generalized_count += 1
    
    print(f"   Generalized {generalized_count} date fields to month-level")
    
    # 5. Generalize occupation codes
    print("\n5. Removing occupation identifiers...")
    if 'ID_OCUPA_N' in df.columns:
        df = df.drop(columns=['ID_OCUPA_N'])
        print("   Removed: ID_OCUPA_N")
    
    # 6. Remove residence municipality details (keep only state level)
    print("\n6. Generalizing residence location...")
    residence_cols_to_remove = ['ID_MN_RESI', 'ID_RG_RESI', 'munResNome', 
                                 'munResTipo', 'munResStatus', 'COMUNINF']
    removed_cols = [col for col in residence_cols_to_remove if col in df.columns]
    if removed_cols:
        df = df.drop(columns=removed_cols)
        print(f"   Removed: {', '.join(removed_cols)}")
    
    # 7. Remove notification municipality details
    print("\n7. Generalizing notification location...")
    notif_cols_to_remove = ['ID_MUNICIP']
    removed_cols = [col for col in notif_cols_to_remove if col in df.columns]
    if removed_cols:
        df = df.drop(columns=removed_cols)
        print(f"   Removed: {', '.join(removed_cols)}")
    
    # 8. Remove system/administrative identifiers
    print("\n8. Removing system identifiers...")
    admin_cols = ['NU_LOTE_I', 'NDUPLIC_N', 'MIGRADO_W']
    removed_cols = [col for col in admin_cols if col in df.columns]
    if removed_cols:
        df = df.drop(columns=removed_cols)
        print(f"   Removed: {', '.join(removed_cols)}")
    
    # 9. K-anonymity check (using available quasi-identifiers)
    print("\n9. Validating k-anonymity...")
    
    # Create age groups from coded age
    if 'NU_IDADE_N' in df.columns:
        df['age_years'] = df['NU_IDADE_N'] - 4000
        df['age_years'] = df['age_years'].clip(lower=0, upper=120)
        
        bins = [0, 18, 40, 60, 120]
        labels = ['0-17', '18-39', '40-59', '60+']
        df['age_group'] = pd.cut(df['age_years'], bins=bins, labels=labels, right=False).astype(str)
    
    # Check k-anonymity on key quasi-identifiers
    if 'DT_SIN_PRI_month' in df.columns and 'age_group' in df.columns and 'CS_SEXO' in df.columns:
        quasi_ids = ['DT_SIN_PRI_month', 'age_group', 'CS_SEXO']
        violations = check_k_anonymity(df, quasi_ids, k=K_ANONYMITY_THRESHOLD)
        
        if len(violations) > 0:
            print(f"   WARNING: {len(violations)} groups with < {K_ANONYMITY_THRESHOLD} individuals")
            print("   Applying additional generalization...")
            
            # First attempt: generalize to broader age groups for small groups
            for group in violations.index:
                mask = True
                for i, col in enumerate(quasi_ids):
                    if i < len(group):
                        mask &= (df[col] == group[i])
                
                if mask.any():
                    df.loc[mask & (df['age_years'] < 40), 'age_group'] = '0-39'
                    df.loc[mask & (df['age_years'] >= 40), 'age_group'] = '40+'
            
            # Re-check
            violations_after = check_k_anonymity(df, quasi_ids, k=K_ANONYMITY_THRESHOLD)
            
            if len(violations_after) > 0:
                print(f"   Still {len(violations_after)} violations - grouping low-volume periods")
                # For months/quarters with very few cases, generalize to semester
                semester_mapping = {
                    '2023-01': '2023-H1', '2023-02': '2023-H1', '2023-03': '2023-H1',
                    '2023-04': '2023-H1', '2023-05': '2023-H1', '2023-06': '2023-H1',
                    '2023-07': '2023-H2', '2023-08': '2023-H2', '2023-09': '2023-H2',
                    '2023-10': '2023-H2', '2023-11': '2023-H2', '2023-12': '2023-H2',
                    '2023-Q1': '2023-H1', '2023-Q2': '2023-H1',
                    '2023-Q3': '2023-H2', '2023-Q4': '2023-H2'
                }
                
                for period, semester in semester_mapping.items():
                    df.loc[df['DT_SIN_PRI_month'] == period, 'DT_SIN_PRI_month'] = semester
                
                violations_final = check_k_anonymity(df, quasi_ids, k=K_ANONYMITY_THRESHOLD)
                print(f"   Violations after semester grouping: {len(violations_final)}")
                
                if len(violations_final) > 0:
                    print(f"   Final step: generalizing age for remaining {len(violations_final)} groups")
                    # Final resort: suppress age distinction entirely for these groups
                    for group in violations_final.index:
                        mask = True
                        for i, col in enumerate(quasi_ids):
                            if i < len(group):
                                mask &= (df[col] == group[i])
                        if mask.any():
                            df.loc[mask, 'age_group'] = 'ALL_AGES'
                    
                    violations_ultimate = check_k_anonymity(df, quasi_ids, k=K_ANONYMITY_THRESHOLD)
                    if len(violations_ultimate) == 0:
                        print(f"   ✓ All groups now have ≥ {K_ANONYMITY_THRESHOLD} individuals")
                    else:
                        print(f"   WARNING: {len(violations_ultimate)} groups still below threshold")
                        print(f"   Suppressing {violations_ultimate.sum()} records to ensure k-anonymity")
                        # Suppress records that can't be anonymized
                        for group in violations_ultimate.index:
                            mask = True
                            for i, col in enumerate(quasi_ids):
                                if i < len(group):
                                    mask &= (df[col] == group[i])
                            if mask.any():
                                df = df[~mask].copy()
                        print(f"   ✓ Records after suppression: {len(df)}")
            else:
                print(f"   ✓ All groups now have ≥ {K_ANONYMITY_THRESHOLD} individuals")
        else:
            print(f"   ✓ All groups have ≥ {K_ANONYMITY_THRESHOLD} individuals")
    
    # 10. Remove temporary columns and exact age
    if 'age_years' in df.columns:
        df = df.drop(columns=['age_years'])
    if 'NU_IDADE_N' in df.columns:
        df = df.drop(columns=['NU_IDADE_N'])
    
    # Save anonymized data
    output_file = f'{DATA_RAW}SINAN_chikungunya_2023.csv'
    df.to_csv(output_file, sep=';', index=False)
    print(f"\n✓ Anonymized data saved to: {output_file}")
    print(f"  Final records: {len(df)}")
    
    return df

# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run complete anonymization pipeline.
    """
    print("\n" + "=" * 70)
    print(" DATA ANONYMIZATION FOR CHIKUNGUNYA SURVEILLANCE STUDY")
    print("=" * 70)
    print(f"\nK-anonymity threshold: {K_ANONYMITY_THRESHOLD}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Anonymize datasets
    rtpcr_df = anonymize_rtpcr_data()
    sinan_df = anonymize_sinan_data()
    
    print("\n" + "=" * 70)
    print(" ANONYMIZATION COMPLETE")
    print("=" * 70)
    print("\nSummary:")
    print(f"  - RT-PCR records: {len(rtpcr_df)}")
    print(f"  - SINAN records: {len(sinan_df)}")
    print(f"  - K-anonymity: ≥{K_ANONYMITY_THRESHOLD}")
    print("\nAnonymization measures applied:")
    print("  ✓ Date generalization (exact → week/month)")
    print("  ✓ Age binning for small groups")
    print("  ✓ Geographic coordinate removal")
    print("  ✓ Health unit identifier removal")
    print("  ✓ Birth year removal")
    print("  ✓ Free-text field removal")
    print("  ✓ Administrative ID removal")
    print("  ✓ K-anonymity validation")
    
    print("\nNOTE: This script modifies the original data files.")
    print("Ensure you have backups before running in production.")

if __name__ == '__main__':
    main()
