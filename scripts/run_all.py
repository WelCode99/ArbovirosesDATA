#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py
==========
Orchestrate the complete analysis pipeline.

This script runs all analysis scripts in sequence:
1. Data preprocessing
2. Descriptive analysis
3. Diagnostic accuracy analysis
4. Comparative analysis
5. Hospitalization analysis
6. Cluster analysis
7. Selection bias analysis
8. Generate figures
9. Validate results

Author: Welisson G.N. Costa
Date: January 2025
"""

import subprocess
import sys
import os
from datetime import datetime

# Script execution order
SCRIPTS = [
    '01_data_preprocessing.py',
    '02_descriptive_analysis.py',
    '03_diagnostic_accuracy.py',
    '04_comparative_analysis.py',
    '05_hospitalization_analysis.py',
    '06_cluster_analysis.py',
    '07_selection_bias_analysis.py',
    '08_generate_figures.py',
    '09_validate_results.py'
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)


def run_script(script_name):
    """Run a single analysis script."""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    
    if not os.path.exists(script_path):
        print(f"✗ ERROR: Script not found: {script_path}")
        return False
    
    print(f"\n{'='*70}")
    print(f"Running: {script_name}")
    print(f"{'='*70}")
    
    try:
        # Change to script directory to ensure relative paths work
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=SCRIPT_DIR,
            capture_output=False,
            text=True,
            check=True
        )
        print(f"\n✓ {script_name} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ ERROR: {script_name} failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: Unexpected error running {script_name}: {e}")
        return False


def main():
    """Main execution function."""
    print("=" * 70)
    print("CHIKUNGUNYA SURVEILLANCE STUDY - COMPLETE ANALYSIS PIPELINE")
    print("=" * 70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {PROJECT_ROOT}")
    print("=" * 70)
    
    # Track execution results
    results = {}
    failed_scripts = []
    
    # Run each script in sequence
    for i, script in enumerate(SCRIPTS, 1):
        print(f"\n[{i}/{len(SCRIPTS)}] Processing: {script}")
        
        success = run_script(script)
        results[script] = success
        
        if not success:
            failed_scripts.append(script)
            print(f"\n⚠ WARNING: {script} failed. Continuing with remaining scripts...")
            # Continue automatically (non-interactive mode)
    
    # Summary
    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION SUMMARY")
    print("=" * 70)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for script, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {script}")
    
    print()
    
    if not failed_scripts:
        print("=" * 70)
        print("✓ ALL SCRIPTS COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\nGenerated outputs:")
        print("  - Processed datasets: data/processed/")
        print("  - Figures: figures/")
        print("  - Validation: See output above")
        return 0
    else:
        print("=" * 70)
        print("✗ PIPELINE COMPLETED WITH ERRORS")
        print("=" * 70)
        print(f"\nFailed scripts ({len(failed_scripts)}):")
        for script in failed_scripts:
            print(f"  - {script}")
        print("\nPlease review the error messages above and fix issues before re-running.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠ Pipeline execution interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
