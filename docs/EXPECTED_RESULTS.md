# Expected Results - Reference Values

## Chikungunya Surveillance Study - Foz do Iguaçu, 2023

This document contains the expected reference values from the published article for validation purposes.

---

## Sample Sizes

| Group | Expected N | Description |
|-------|-----------|-------------|
| RT-PCR+ | 201 | Primary cohort, laboratory confirmed |
| SINAN Laboratory | 558 | SINAN cases with laboratory confirmation |
| SINAN Clinical-Epidemiological | 543 | SINAN cases with clinical-epidemiological criteria |
| **Total SINAN** | **1,101** | All confirmed SINAN cases |

---

## Diagnostic Accuracy (RT-PCR+ cases)

| Metric | Expected Value | 95% CI |
|--------|---------------|--------|
| Overall diagnostic accuracy (including Chikungunya) | 41.3% | 34.4-48.2% |
| Correct Chikungunya diagnosis (sole diagnosis) | 9.0% | 5.0-13.0% |

### Diagnostic Hypotheses Distribution

| Category | Expected Count | Expected % |
|----------|---------------|-------------|
| Dengue only | 114 | 56.7% |
| Dengue or Chikungunya | 65 | 32.3% |
| Chikungunya only | 18 | 9.0% |
| Other | 4 | 2.0% |

---

## Factors Associated with Correct Diagnosis (Odds Ratios)

| Factor | OR | 95% CI | p-value |
|--------|----|--------|---------|
| Arthralgia | 2.87 | 1.67-4.93 | <0.001 |
| Positive tourniquet | 0.52 | 0.29-0.93 | 0.028 |
| Headache | 0.89 | 0.48-1.65 | 0.714 |
| Fever | 0.76 | 0.38-1.52 | 0.438 |
| Myalgia | 0.82 | 0.43-1.56 | 0.548 |
| Rash | 1.24 | 0.69-2.23 | 0.473 |
| Nausea | 0.91 | 0.51-1.62 | 0.749 |
| Vomiting | 0.68 | 0.32-1.45 | 0.318 |

---

## Symptom Frequencies by Group

### RT-PCR+ (n=201)

| Symptom | Expected Frequency (%) |
|---------|----------------------|
| Fever | 85.1% |
| Myalgia | 78.6% |
| Headache | 74.1% |
| Arthralgia | 82.6% |
| Rash | 24.9% |
| Nausea | 28.9% |
| Vomiting | 14.9% |

### SINAN Laboratory (n=558)

| Symptom | Expected Frequency (%) |
|---------|----------------------|
| Fever | 78.5% |
| Myalgia | 72.4% |
| Headache | 69.2% |
| Arthralgia | 76.3% |
| Rash | 31.2% |
| Nausea | 22.1% |
| Vomiting | 18.5% |

### SINAN Clinical-Epidemiological (n=543)

| Symptom | Expected Frequency (%) |
|---------|----------------------|
| Fever | 82.3% |
| Myalgia | 68.9% |
| Headache | 71.5% |
| Arthralgia | 45.2% |
| Rash | 18.6% |
| Nausea | 19.4% |
| Vomiting | 12.1% |

---

## Hospitalization Rates

| Group | Expected Rate (%) | 95% CI |
|-------|------------------|--------|
| RT-PCR+ | 5.5% | 2.3-8.6% |
| SINAN Laboratory | 12.4% | 9.6-15.1% |
| SINAN Clinical-Epidemiological | 1.3% | 0.3-2.3% |
| SINAN Total | 6.9% | 5.3-8.5% |

### Pairwise Comparisons

| Comparison | Expected p-value |
|------------|-----------------|
| RT-PCR+ vs SINAN Laboratory | 0.006 |
| RT-PCR+ vs SINAN Clinical | 0.001 |

---

## Risk Factors for Hospitalization (RT-PCR+ cases)

### Multivariate Analysis (Adjusted OR)

| Factor | aOR | 95% CI | p-value |
|--------|-----|--------|---------|
| Age ≥60 years | 2.47 | 1.12-5.45 | 0.025 |
| Autoimmune disease | 2.89 | 1.08-7.73 | 0.034 |
| Vomiting | 1.86 | 0.78-4.44 | 0.162 |
| Female sex | 0.92 | 0.41-2.07 | 0.841 |

---

## Symptom Clustering Analysis

### Cluster Distribution

| Cluster | Expected % | Description |
|---------|-----------|-------------|
| Cluster 1 - Classical Triad | 42.3% | Fever-Myalgia-Headache dominant |
| Cluster 2 - Articular Profile | 35.7% | Arthralgia dominant |
| Cluster 3 - Gastrointestinal | 22.0% | Nausea-Vomiting dominant |

### Cluster Characteristics

**Cluster 1 - Classical Triad (42.3%)**
- Fever: ~95%
- Myalgia: ~90%
- Headache: ~85%
- Arthralgia: ~30%
- Nausea: ~20%
- Vomiting: ~15%

**Cluster 2 - Articular Profile (35.7%)**
- Fever: ~90%
- Myalgia: ~85%
- Headache: ~40%
- Arthralgia: ~95%
- Nausea: ~25%
- Vomiting: ~10%

**Cluster 3 - Gastrointestinal (22.0%)**
- Fever: ~85%
- Myalgia: ~45%
- Headache: ~35%
- Arthralgia: ~40%
- Nausea: ~90%
- Vomiting: ~80%

### RT-PCR+ Concentration by Cluster

| Cluster | Total Cluster % | RT-PCR+ in Cluster % |
|---------|----------------|---------------------|
| Cluster 1 | 42.3% | 9.8% |
| Cluster 2 | 35.7% | 17.4% |
| Cluster 3 | 22.0% | 6.2% |

**Chi-square test**: χ² = 35.63, p < 0.001

---

## Selection Bias Analysis

### Factors Associated with PCR Testing (OR)

| Factor | Expected OR | 95% CI |
|--------|------------|--------|
| Hospitalization | 3.21 | 2.1-4.9 |
| Severe symptoms | 2.45 | 1.8-3.3 |
| Arthralgia | 1.87 | 1.4-2.5 |
| Age ≥60 | 1.52 | 1.1-2.1 |
| Urban residence | 1.23 | 0.9-1.7 |

---

## Validation Tolerance

For automated validation, the following tolerances are acceptable:

- **Percentages**: ±2.0 percentage points
- **Odds Ratios**: ±0.2 OR units
- **Confidence Intervals**: ±0.3 CI units
- **Sample Sizes**: Exact match required
- **P-values**: ±0.01 for p > 0.05, ±0.001 for p < 0.05

---

*Document version: 1.0*  
*Date: January 2025*  
*Reference: Costa et al. (2025) - Chikungunya Surveillance Study*
