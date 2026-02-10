# CODEBOOK - Data Dictionary

## 📊 Chikungunya Surveillance Study - Foz do Iguaçu, 2023

---

## Dataset 1: `RTPCR_chikungunya_anonymized.csv`

### Source
Medical records from Municipal Emergency Care Unit (UPA), Foz do Iguaçu, PR, Brazil

### Sample
n = 201 RT-PCR confirmed Chikungunya cases

### Variables

| Variable | Type | Description | Values/Range |
|----------|------|-------------|--------------|
| `id` | Integer | Unique case identifier (randomized) | 1-201 |
| `detectado` | String | Arbovirus detected | "CHIK" |
| `year_month` | String | Presentation year-month (anonymized) | YYYY-MM |
| `idade` | Numeric | Age in years | 0-99 |
| `age_bin` | Categorical | Age group (anonymized) | "0-17", "18-39", "40-59", "60+", "0-39", "40+" |
| `sexo` | Categorical | Biological sex | "M" = Male, "F" = Female |
| `bairro` | String | Neighborhood (anonymized) | Text or "OTHER" for rare neighborhoods |
| `desfecho` | Categorical | Clinical outcome | See below |
| `sequelas` | String | Reported sequelae | Text or "NONE" |
| `HIPOTESE_DIAGNOSTICA` | Categorical | Initial clinical hypothesis | See below |
| `PROVA_LACO` | Categorical | Tourniquet test result | See below |

**Note:** Original `data` field removed for anonymization. Original `sintomas` (free-text symptom descriptions) removed to prevent re-identification.

#### Symptom Variables (Binary: 0 = Absent, 1 = Present)

| Variable | Description |
|----------|-------------|
| `CEFALEIA` | Headache |
| `FEBRE` | Fever |
| `MIALGIA` | Myalgia |
| `ARTRALGIA` | Arthralgia |
| `EDEMA` | Edema/swelling |
| `EXANTEMA` | Rash/exanthema |
| `NAUSEA` | Nausea |
| `VOMITO` | Vomiting |
| `CONJUNTIVITE` | Conjunctivitis |
| `ASTENIA` | Asthenia/fatigue |
| `ARTRITE` | Arthritis |
| `DOR_RETRO_ORBITAL` | Retro-orbital pain |

#### Categorical Value Labels

**DESFECHO (Outcome)**
| Value | Description |
|-------|-------------|
| ALTA | Discharged |
| ALTA MELHORADO | Discharged improved |
| INTERNAMENTO HOSPITALAR | Hospital admission |
| OBITO | Death |

**HIPOTESE_DIAGNOSTICA (Initial Diagnosis)**
| Value | Description |
|-------|-------------|
| DENGUE A | Dengue without warning signs |
| DENGUE B | Dengue with warning signs |
| DENGUE C | Severe dengue |
| CHIKUNGUNYA | Chikungunya |
| DENGUE OU CHIKUNGUNYA | Dengue or Chikungunya differential |
| OTHER | Other diagnosis |

**PROVA_LACO (Tourniquet Test)**
| Value | Description |
|-------|-------------|
| POSITIVA / POSITIVO | Positive |
| NEGATIVA / NEGATIVO | Negative |
| NAO REALIZADO | Not performed |
| - | Missing |

---

## Dataset 2: `SINAN_chikungunya_2023.csv`

### Source
SINAN/DATASUS - Brazilian Notifiable Diseases Information System

### Sample
n = 1,964 Chikungunya notifications from Foz do Iguaçu, 2023 (1 record suppressed for k-anonymity)

### Anonymization Changes

**Removed Fields (for privacy protection):**
- All exact dates replaced with `_month` suffix fields (YYYY-MM or semester format)
- `ANO_NASC` (birth year)
- `NU_IDADE_N` (exact age code) - replaced with `age_group`
- `munResLat`, `munResLon`, `munResAlt`, `munResArea` (geographic coordinates)
- `ID_UNIDADE`, `ID_REGIONA` (health facility identifiers)
- `ID_MUNICIP`, `ID_MN_RESI`, `ID_RG_RESI` (municipality identifiers)
- `munResNome`, `munResTipo`, `munResStatus` (municipality details)
- `ID_OCUPA_N` (occupation code)
- `NU_LOTE_I`, `NDUPLIC_N`, `MIGRADO_W` (system identifiers)
- `COMUNINF` (infection municipality code)

**See [DATA_ANONYMIZATION.md](DATA_ANONYMIZATION.md) for complete details.**

### Key Variables

| Variable | Type | Description | Values |
|----------|------|-------------|--------|
| `TP_NOT` | String | Notification type | "Individual" |
| `ID_AGRAVO` | String | Disease code (ICD-10) | "A92.0" = Chikungunya |
| `DT_NOTIFIC_month` | String | Notification month (anonymized) | YYYY-MM or YYYY-HX |
| `DT_SIN_PRI_month` | String | Symptom onset month (anonymized) | YYYY-MM or YYYY-HX |
| `age_group` | Categorical | Age group (anonymized) | "0-17", "18-39", "40-59", "60+", "0-39", "40+", "ALL_AGES" |
| `CS_SEXO` | Categorical | Sex | "Masculino", "Feminino", "Ignorado" |
| `CS_RACA` | Categorical | Race/ethnicity | Text |
| `CS_ESCOL_N` | Categorical | Education level | Text |
| `CLASSI_FIN` | Categorical | Final classification | See below |
| `CRITERIO` | Categorical | Confirmation criteria | See below |
| `HOSPITALIZ` | Binary | Hospitalization | "Sim"=1, "Não"=2 |
| `EVOLUCAO` | Categorical | Evolution | "Cura", "Óbito", etc. |

#### SINAN Symptom Variables (Binary: "Sim"=Yes, "Não"=No)

| Variable | Description |
|----------|-------------|
| `FEBRE` | Fever |
| `MIALGIA` | Myalgia |
| `CEFALEIA` | Headache |
| `EXANTEMA` | Rash |
| `VOMITO` | Vomiting |
| `NAUSEA` | Nausea |
| `DOR_COSTAS` | Back pain |
| `CONJUNTVIT` | Conjunctivitis |
| `ARTRITE` | Arthritis |
| `ARTRALGIA` | Arthralgia |
| `PETEQUIA_N` | Petechiae |
| `LEUCOPENIA` | Leukopenia |
| `LACO` | Positive tourniquet test |
| `DOR_RETRO` | Retro-orbital pain |

#### Comorbidity Variables

| Variable | Description |
|----------|-------------|
| `DIABETES` | Diabetes mellitus |
| `HEMATOLOG` | Hematological disease |
| `HEPATOPAT` | Liver disease |
| `RENAL` | Kidney disease |
| `HIPERTENSA` | Hypertension |
| `ACIDO_PEPT` | Peptic ulcer disease |
| `AUTO_IMUNE` | Autoimmune disease |

#### Classification Labels

**CLASSI_FIN (Final Classification)**
| Value | Description |
|-------|-------------|
| Chikungunya | Confirmed case |
| Descartado | Discarded case |

**CRITERIO (Confirmation Criteria)**
| Value | Description |
|-------|-------------|
| Laboratório | Laboratory confirmed |
| Clínico epidemiológico | Clinical-epidemiological |

---

## Derived Variables (Created During Analysis)

| Variable | Description | Calculation |
|----------|-------------|-------------|
| `diagnostic_correct` | Correct initial diagnosis | HIPOTESE includes "CHIK" |
| `age_group` | Age categories | <18, 18-39, 40-59, ≥60 |
| `hospitalized` | Hospitalization binary | desfecho contains "INTERN" |
| `symptom_count` | Number of symptoms | Sum of symptom variables |
| `sinan_group` | SINAN subgroup | Lab confirmed vs Clinical |

---

## Data Quality Notes

1. **Missing Data**: Missing values coded as empty string, "-", or "NONE"
2. **Dates**: All dates in ISO 8601 format (YYYY-MM-DD)
3. **Age Coding in SINAN**: Values 4XXX indicate age in years (e.g., 4045 = 45 years)
4. **Symptom Standardization**: All symptom variables standardized to binary (0/1)

---

## Data Harmonization

For comparative analysis, the following mappings were applied:

| RT-PCR Variable | SINAN Variable | Standardized |
|-----------------|----------------|--------------|
| sexo (M/F) | CS_SEXO | sex (M/F) |
| idade | NU_IDADE_N - 4000 | age_years |
| FEBRE | FEBRE | fever |
| ARTRALGIA | ARTRALGIA | arthralgia |
| ... | ... | ... |

---

*Last updated: January 2025*
