# Statistical Analysis Plan

## Chikungunya Surveillance Study - Foz do Iguaçu, Brazil (2023)

### Study Design
Retrospective cohort study comparing RT-PCR confirmed Chikungunya cases with SINAN surveillance data.

---

## Primary Objectives

1. **Diagnostic Accuracy**: Evaluate accuracy of initial clinical diagnosis in RT-PCR confirmed cases
2. **Group Comparison**: Compare clinical-epidemiological profiles between RT-PCR+ and SINAN subgroups
3. **Hospitalization Analysis**: Identify risk factors for hospitalization
4. **Selection Bias**: Evaluate selection bias for PCR testing

---

## Statistical Methods

### 1. Descriptive Statistics
- Continuous variables: Mean ± SD, Median (IQR)
- Categorical variables: Frequencies and percentages with 95% CI (Wilson method)

### 2. Diagnostic Accuracy Analysis
- **Outcome**: Correct initial diagnosis (including Chikungunya)
- **Method**: Univariate and multivariate logistic regression
- **Variables**: Symptoms (binary), tourniquet test, demographics
- **Results**: Odds ratios with 95% CI

### 3. Group Comparisons
- **Chi-square test**: Categorical variables
- **Kruskal-Wallis test**: Continuous variables (non-normal distribution)
- **Z-test for proportions**: Pairwise hospitalization rate comparisons
- **Bonferroni correction**: Multiple comparisons

### 4. Hospitalization Risk Analysis
- **Univariate analysis**: Individual risk factors with OR and 95% CI
- **Multivariate logistic regression**: Adjusted OR
- **Model selection**: Backward stepwise (p < 0.10 for entry)

### 5. Cluster Analysis
- **Method**: Hierarchical clustering (Ward's method)
- **Distance**: Euclidean on standardized symptom matrix
- **Number of clusters**: Determined by dendrogram inspection and domain knowledge
- **Validation**: Chi-square test for cluster-outcome association

### 6. Selection Bias Analysis
- **Propensity score model**: Logistic regression predicting PCR testing
- **Covariates**: Symptoms, hospitalization, demographics
- **Assessment**: Distribution overlap, standardized differences

---

## Sample Size Considerations

| Group | N | Description |
|-------|---|-------------|
| RT-PCR+ | 201 | Primary cohort, laboratory confirmed |
| SINAN Laboratory | 558 | SINAN cases with laboratory confirmation |
| SINAN Clinical | 543 | SINAN cases with clinical-epidemiological criteria |
| **Total SINAN** | **1,101** | All confirmed SINAN cases |

---

## Software and Packages

- **Python 3.8+**
  - pandas, numpy: Data manipulation
  - scipy.stats: Statistical tests
  - statsmodels: Regression models
  - scikit-learn: Clustering
  - matplotlib, seaborn: Visualization

---

## Quality Control

1. **Data validation**: Range checks, consistency checks
2. **Missing data**: Complete case analysis (low missing rate <5%)
3. **Outliers**: Clinical review, no exclusion without justification
4. **Reproducibility**: All code version-controlled, random seeds fixed

---

## Significance Level

- **Alpha**: 0.05 (two-tailed)
- **Multiple comparisons**: Bonferroni correction when applicable

---

## Reporting

- Results reported according to STROBE guidelines
- Effect sizes with confidence intervals
- P-values reported to 3 decimal places (or <0.001)

---

*Document version: 1.0*  
*Date: January 2025*
