# ArbovirosesDATA

## 🔬 Chikungunya Surveillance Data Repository - Foz do Iguaçu, Brazil (2023)

[![DOI](https://img.shields.io/badge/DOI-pending-blue)]()
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Data: Open](https://img.shields.io/badge/Data-Open%20Access-green.svg)]()

### 📖 About This Repository

This repository contains the dataset and analytical code supporting the research article:

> **"Acurácia do diagnóstico clínico inicial e comparação com dados de vigilância em surto de Chikungunya: estudo de coorte retrospectivo"**  
> Welisson B. Costa¹, Maria Leandra Terencio
>
> ¹ Faculdade de Medicina, Universidade Federal da Integração Latino-Americana (UNILA), Foz do Iguaçu, PR, Brasil  

### 🎯 Study Overview

**Objective**: To evaluate the accuracy of initial clinical diagnosis and compare clinical-epidemiological profiles between RT-PCR confirmed cases and SINAN surveillance data during the 2023 Chikungunya epidemic in Foz do Iguaçu, Brazil.

**Study Design**: Retrospective cohort study

**Period**: January - December 2023

**Setting**: Emergency Department of Municipal Emergency Care Unit (HMPGL) and SINAN/DATASUS surveillance database

### 📊 Data Description

| Dataset | Records | Source | Description |
|---------|---------|--------|-------------|
| `RTPCR_chikungunya_anonymized.csv` | 201 | Medical Records | RT-PCR confirmed Chikungunya cases with detailed clinical data |
| `SINAN_chikungunya_2023.csv` | 1,965 | SINAN/DATASUS | Surveillance notification data for Foz do Iguaçu |

### 📁 Repository Structure

```
ArbovirosesDATA/
├── README.md                           # This file
├── LICENSE                             # CC BY 4.0 License
├── CITATION.cff                        # Citation metadata
├── requirements.txt                    # Python dependencies
├── data/
│   ├── raw/
│   │   ├── RTPCR_chikungunya_anonymized.csv    # Primary dataset (anonymized)
│   │   └── SINAN_chikungunya_2023.csv          # Surveillance data
│   └── processed/
│       └── merged_analysis_dataset.csv          # Processed dataset for analysis
├── scripts/
│   ├── 01_data_preprocessing.py        # Data cleaning and preparation
│   ├── 02_descriptive_analysis.py      # Descriptive statistics
│   ├── 03_diagnostic_accuracy.py       # Diagnostic accuracy analysis
│   ├── 04_comparative_analysis.py      # Group comparisons (RT-PCR vs SINAN)
│   ├── 05_hospitalization_analysis.py  # Hospitalization and risk factors
│   ├── 06_cluster_analysis.py          # Symptom clustering
│   ├── 07_selection_bias_analysis.py   # Selection bias evaluation
│   └── 08_generate_figures.py          # Publication-ready figures
├── figures/
│   └── [Generated publication figures]
└── docs/
    ├── CODEBOOK.md                     # Variable dictionary
    └── STATISTICAL_ANALYSIS_PLAN.md    # Pre-registered analysis plan
```

### 🔧 Requirements

```bash
pip install -r requirements.txt
```

**Main dependencies:**
- Python ≥ 3.8
- pandas ≥ 1.5.0
- numpy ≥ 1.23.0
- scipy ≥ 1.9.0
- statsmodels ≥ 0.13.0
- scikit-learn ≥ 1.1.0
- matplotlib ≥ 3.6.0
- seaborn ≥ 0.12.0

### 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/WelCode99/ArbovirosesDATA.git
cd ArbovirosesDATA

# Install dependencies
pip install -r requirements.txt

# Run complete analysis pipeline
python scripts/01_data_preprocessing.py
python scripts/02_descriptive_analysis.py
python scripts/03_diagnostic_accuracy.py
python scripts/04_comparative_analysis.py
python scripts/05_hospitalization_analysis.py
python scripts/06_cluster_analysis.py
python scripts/07_selection_bias_analysis.py
python scripts/08_generate_figures.py
```

### 📈 Key Findings

| Finding | Value | 95% CI |
|---------|-------|--------|
| Overall diagnostic accuracy | 41.3% | 34.4-48.2% |
| Correct Chikungunya diagnosis | 9.0% | 5.0-13.0% |
| Arthralgia OR for accuracy | 2.87 | 1.67-4.93 |
| Hospitalization RT-PCR+ | 5.5% | 2.3-8.6% |
| Hospitalization SINAN Lab | 12.4% | 9.6-15.1% |

### 🔐 Data Privacy & Ethics

- **Ethical Approval**: This study was approved by the Research Ethics Committee (CEP) - Protocol CAAE: [pending]
- **Data Anonymization**: All personally identifiable information (addresses, names, ID numbers) has been removed
- **Geolocation**: Only neighborhood-level geographic data is included (bairro)
- **LGPD Compliance**: Data handling follows Brazilian General Data Protection Law (Lei nº 13.709/2018)

### 📄 License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.

### 📚 Citation

If you use this data or code, please cite:

```bibtex
@article{costa2025chikungunya,
  title={Acurácia do diagnóstico clínico inicial e comparação com dados de vigilância em surto de Chikungunya: estudo de coorte retrospectivo},
  author={Costa, Welisson G.N. and Nogueira, Eliane Lopes and Costa, José L.N.},
  journal={[Journal Name]},
  year={2025},
  volume={},
  pages={},
  doi={}
}
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for:
- Bug reports
- Feature requests
- Documentation improvements
- Additional analyses

### 📧 Contact

**Corresponding Author:**  
Welisson G.N. Costa  
Email: [contact email]  
ORCID: [ORCID ID]

### 🏛️ Institutional Support

- Universidade Federal da Integração Latino-Americana (UNILA)
- Hospital Municipal Padre Germano Lauck

---

*Last updated: January 2025*
