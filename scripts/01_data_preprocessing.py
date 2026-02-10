#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_data_preprocessing.py
========================
Data preprocessing and cleaning for Chikungunya surveillance study.

This script:
1. Loads raw RT-PCR and SINAN datasets
2. Standardizes variable names and formats
3. Creates derived variables
4. Exports processed datasets

Author: Welisson G.N. Costa
Date: January 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

DATA_RAW = '../data/raw/'
DATA_PROCESSED = '../data/processed/'

# Age group midpoint mappings for anonymized data
# These represent approximate midpoints or reasonable defaults for age groups
# used when exact ages have been anonymized to broader categories
AGE_GROUP_MIDPOINTS = {
    '0-17': 8.5,      # Midpoint of pediatric range
    '18-39': 28.5,    # Midpoint of young adult range
    '40-59': 49.5,    # Midpoint of middle-aged range
    '60+': 70,        # Representative value for elderly (not a true midpoint)
    '0-39': 20,       # Broad young range approximation
    '40+': 60,        # Broad older range approximation
    'ALL_AGES': 40    # Population-wide approximation (study mean ~41 years)
}

# =============================================================================
# LOAD DATA
# =============================================================================

def load_rtpcr_data():
    """Load and preprocess RT-PCR confirmed cases."""
    print("Loading RT-PCR data...")
    
    df = pd.read_csv(f'{DATA_RAW}RTPCR_chikungunya_anonymized.csv', sep=';')
    
    # Create unique ID only if not present
    if 'id' not in df.columns:
        df['id'] = range(1, len(df) + 1)
    
    # Handle anonymized date field (year_month instead of exact date)
    if 'year_month' in df.columns:
        # Convert year-month to datetime (first day of month for consistency)
        df['data'] = pd.to_datetime(df['year_month'] + '-01', errors='coerce')
    elif 'data' in df.columns:
        # Fallback if exact dates still present
        df['data'] = pd.to_datetime(df['data'], errors='coerce')
    
    # Clean age
    df['idade'] = pd.to_numeric(df['idade'], errors='coerce')
    
    # Standardize sex
    df['sexo'] = df['sexo'].str.upper().str.strip()
    df['sexo'] = df['sexo'].replace({'MASCULINO': 'M', 'FEMININO': 'F'})
    
    # Create binary symptom variables if not already binary
    symptom_cols = ['CEFALEIA', 'FEBRE', 'MIALGIA', 'ARTRALGIA', 'EDEMA', 
                    'EXANTEMA', 'NAUSEA', 'VOMITO', 'CONJUNTIVITE', 'ASTENIA', 
                    'ARTRITE', 'DOR_RETRO_ORBITAL']
    
    for col in symptom_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Create derived variables
    df['hospitalized'] = df['desfecho'].str.contains('INTERN|HOSPITALAR', 
                                                       case=False, na=False).astype(int)
    
    # Diagnostic accuracy
    df['diagnostic_correct'] = df['HIPOTESE_DIAGNOSTICA'].str.contains(
        'CHIK', case=False, na=False).astype(int)
    
    # Age groups - use existing age_bin if available, otherwise create
    if 'age_bin' not in df.columns:
        df['age_group'] = pd.cut(df['idade'], 
                                 bins=[0, 18, 40, 60, 100],
                                 labels=['<18', '18-39', '40-59', '≥60'],
                                 right=False)
    else:
        # Map anonymized age_bin to standard age_group labels
        # Handle various anonymized age bins
        df['age_group'] = df['age_bin']
    
    # Symptom count
    df['symptom_count'] = df[symptom_cols].sum(axis=1)
    
    print(f"  Loaded {len(df)} RT-PCR+ cases")
    return df


def load_sinan_data():
    """Load and preprocess SINAN surveillance data."""
    print("Loading SINAN data...")
    
    df = pd.read_csv(f'{DATA_RAW}SINAN_chikungunya_2023.csv', sep=';', low_memory=False)
    
    # Filter confirmed Chikungunya cases
    df = df[df['CLASSI_FIN'] == 'Chikungunya'].copy()
    
    # Create subgroups
    df['sinan_group'] = np.where(
        df['CRITERIO'] == 'Laboratório', 
        'Laboratory', 
        'Clinical-epidemiological'
    )
    
    # Handle anonymized age field
    if 'age_group' in df.columns:
        # Age already anonymized - extract numeric age from age_group for analysis
        # Use predefined midpoints for compatibility with analyses requiring numeric age
        df['idade'] = df['age_group'].map(AGE_GROUP_MIDPOINTS)
        # Keep original age_group from anonymization
    elif 'NU_IDADE_N' in df.columns:
        # Fallback if exact age still present (legacy compatibility)
        df['idade'] = df['NU_IDADE_N'].apply(
            lambda x: x - 4000 if pd.notna(x) and x >= 4000 else x
        )
        # Create age groups
        df['age_group'] = pd.cut(df['idade'], 
                                 bins=[0, 18, 40, 60, 100],
                                 labels=['<18', '18-39', '40-59', '≥60'],
                                 right=False)
    else:
        print("  WARNING: No age information found")
        df['idade'] = np.nan
        df['age_group'] = 'Unknown'
    
    # Standardize sex
    if 'CS_SEXO' in df.columns:
        df['sexo'] = df['CS_SEXO'].map({'Masculino': 'M', 'Feminino': 'F'})
    
    # Standardize symptoms (Sim/Não to 1/0)
    symptom_mapping = {'Sim': 1, 'Não': 0}
    symptom_cols_sinan = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'EXANTEMA', 'VOMITO',
                          'NAUSEA', 'DOR_COSTAS', 'CONJUNTVIT', 'ARTRITE', 
                          'ARTRALGIA', 'PETEQUIA_N', 'DOR_RETRO']
    
    for col in symptom_cols_sinan:
        if col in df.columns:
            df[col] = df[col].map(symptom_mapping).fillna(0).astype(int)
    
    # Hospitalization
    if 'HOSPITALIZ' in df.columns:
        df['hospitalized'] = (df['HOSPITALIZ'] == 'Sim').astype(int)
    
    print(f"  Loaded {len(df)} SINAN confirmed cases")
    print(f"    - Laboratory confirmed: {(df['sinan_group'] == 'Laboratory').sum()}")
    print(f"    - Clinical-epidemiological: {(df['sinan_group'] == 'Clinical-epidemiological').sum()}")
    
    return df


def create_merged_dataset(rtpcr_df, sinan_df):
    """Create harmonized dataset for comparative analysis."""
    print("Creating merged analysis dataset...")
    
    # Standardize RT-PCR
    rtpcr_std = rtpcr_df[['id', 'idade', 'sexo', 'age_group', 'hospitalized',
                          'FEBRE', 'MIALGIA', 'CEFALEIA', 'ARTRALGIA', 
                          'EXANTEMA', 'NAUSEA', 'VOMITO']].copy()
    rtpcr_std['source'] = 'RT-PCR+'
    rtpcr_std['subgroup'] = 'RT-PCR Confirmed'
    
    # Standardize SINAN Lab
    sinan_lab = sinan_df[sinan_df['sinan_group'] == 'Laboratory'].copy()
    sinan_lab_std = sinan_lab[['idade', 'sexo', 'age_group', 'hospitalized',
                               'FEBRE', 'MIALGIA', 'CEFALEIA', 'ARTRALGIA',
                               'EXANTEMA', 'NAUSEA', 'VOMITO']].copy()
    # Create ID only if not already present
    if 'id' not in sinan_lab_std.columns:
        sinan_lab_std['id'] = range(1000, 1000 + len(sinan_lab_std))
    sinan_lab_std['source'] = 'SINAN'
    sinan_lab_std['subgroup'] = 'SINAN Laboratory'
    
    # Standardize SINAN Clinical
    sinan_clin = sinan_df[sinan_df['sinan_group'] == 'Clinical-epidemiological'].copy()
    sinan_clin_std = sinan_clin[['idade', 'sexo', 'age_group', 'hospitalized',
                                  'FEBRE', 'MIALGIA', 'CEFALEIA', 'ARTRALGIA',
                                  'EXANTEMA', 'NAUSEA', 'VOMITO']].copy()
    # Create ID only if not already present
    if 'id' not in sinan_clin_std.columns:
        sinan_clin_std['id'] = range(5000, 5000 + len(sinan_clin_std))
    sinan_clin_std['source'] = 'SINAN'
    sinan_clin_std['subgroup'] = 'SINAN Clinical-Epidemiological'
    
    # Merge
    merged = pd.concat([rtpcr_std, sinan_lab_std, sinan_clin_std], 
                       ignore_index=True)
    
    print(f"  Created merged dataset with {len(merged)} records")
    return merged


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DATA PREPROCESSING")
    print("Chikungunya Surveillance Study - Foz do Iguaçu, 2023")
    print("=" * 60)
    print()
    
    # Load data
    rtpcr_df = load_rtpcr_data()
    sinan_df = load_sinan_data()
    
    # Create merged dataset
    merged_df = create_merged_dataset(rtpcr_df, sinan_df)
    
    # Export processed data
    print("\nExporting processed datasets...")
    rtpcr_df.to_csv(f'{DATA_PROCESSED}rtpcr_processed.csv', index=False)
    sinan_df.to_csv(f'{DATA_PROCESSED}sinan_processed.csv', index=False)
    merged_df.to_csv(f'{DATA_PROCESSED}merged_analysis_dataset.csv', index=False)
    
    print("\n✓ Preprocessing complete!")
    print(f"  - RT-PCR processed: {len(rtpcr_df)} cases")
    print(f"  - SINAN processed: {len(sinan_df)} cases")
    print(f"  - Merged dataset: {len(merged_df)} records")
