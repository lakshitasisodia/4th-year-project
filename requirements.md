# Requirements Documentation

## Robust Stress Classification Pipeline
### Integrating Academic, Social, and Health Indicators for Stress Classification Using Explainable Machine Learning

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Python Dependencies](#python-dependencies)
3. [Installation Guide](#installation-guide)
4. [Dataset Requirements](#dataset-requirements)
5. [Hardware Requirements](#hardware-requirements)
6. [Environment Setup](#environment-setup)
7. [Verification & Testing](#verification--testing)
8. [Troubleshooting](#troubleshooting)
9. [Optional Dependencies](#optional-dependencies)

---

## System Requirements

### Operating System
- **Linux**: Ubuntu 18.04+ / Debian 10+ / CentOS 7+ (Recommended)
- **macOS**: 10.14 (Mojave) or later
- **Windows**: Windows 10/11 (64-bit)

### Python Version
- **Required**: Python 3.8 - 3.11
- **Recommended**: Python 3.10.x
- **Not Compatible**: Python 3.12+ (due to scikit-learn compatibility issues)

```bash
# Check your Python version
python --version
# or
python3 --version
```

---

## Python Dependencies

### Core Dependencies

#### Scientific Computing & Data Processing
```
numpy>=1.21.0,<1.27.0
pandas>=1.3.0,<2.2.0
scipy>=1.7.0,<1.12.0
```

#### Machine Learning & Modeling
```
scikit-learn>=1.0.0,<1.4.0
imbalanced-learn>=0.10.0,<0.12.0
```

#### Visualization
```
matplotlib>=3.4.0,<3.9.0
seaborn>=0.11.0,<0.14.0
```

#### Explainable AI (Optional - Phase 9)
```
shap>=0.41.0,<0.45.0
```

### Complete requirements.txt
Create a file named `requirements.txt` with the following content:

```txt
# Core Scientific Computing
numpy==1.24.3
pandas==2.0.3
scipy==1.11.4

# Machine Learning
scikit-learn==1.3.2
imbalanced-learn==0.11.0

# Visualization
matplotlib==3.7.5
seaborn==0.13.2

# Statistical Analysis
statsmodels==0.14.1

# Optional: Explainable AI (for Phase 9/SHAP)
# shap==0.43.0

# Optional: Jupyter Notebook support
# jupyter==1.0.0
# notebook==7.0.6
# ipykernel==6.27.1
# ipywidgets==8.1.1

# Optional: Progress bars
# tqdm==4.66.1

# Optional: Export utilities
# openpyxl==3.1.2
# xlsxwriter==3.1.9
```

### Dependency Version Rationale

| Package | Version | Reason |
|---------|---------|--------|
| numpy | 1.24.3 | Stable release, compatible with scikit-learn 1.3.x |
| pandas | 2.0.3 | Modern API, performance improvements |
| scikit-learn | 1.3.2 | Stable, includes all required models & metrics |
| imbalanced-learn | 0.11.0 | SMOTE implementation, compatible with sklearn 1.3.x |
| matplotlib | 3.7.5 | Stable plotting backend |
| seaborn | 0.13.2 | Modern statistical visualizations |
| shap | 0.43.0 | Latest stable, tree explainer optimizations |

---

## Installation Guide

### Method 1: Using pip (Recommended)

#### Step 1: Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv stress_env
source stress_env/bin/activate

# Windows
python -m venv stress_env
stress_env\Scripts\activate
```

#### Step 2: Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

#### Step 3: Install Core Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Verify Installation
```bash
python -c "import sklearn; import pandas; import numpy; print('✓ Core dependencies installed')"
```

### Method 2: Using conda (Alternative)

#### Step 1: Create Conda Environment
```bash
conda create -n stress_env python=3.10
conda activate stress_env
```

#### Step 2: Install Dependencies
```bash
# Install from conda-forge (recommended for scientific packages)
conda install -c conda-forge numpy pandas scikit-learn matplotlib seaborn scipy

# Install imbalanced-learn via pip (not available on conda)
pip install imbalanced-learn==0.11.0
```

#### Step 3: Optional SHAP Installation
```bash
# For conda
conda install -c conda-forge shap

# Or via pip
pip install shap==0.43.0
```

### Method 3: Google Colab (Cloud-Based)

```python
# Run in Colab cell
!pip install -q scikit-learn==1.3.2 imbalanced-learn==0.11.0 seaborn==0.13.2

# For SHAP (Phase 9)
!pip install -q shap==0.43.0

# Upload datasets
from google.colab import files
uploaded = files.upload()  # Upload StressLevelDataset.csv and Stress_Dataset.csv
```

---

## Dataset Requirements

### Required Files

#### 1. StressLevelDataset.csv (Dataset 1)
- **Format**: CSV with header row
- **Expected Columns**: 
  - Numerical features (0-21 scale for stressors, 0-5 for factors)
  - Target column: `stress_level` (0, 1, 2)
  - Must include protective factors: `self_esteem`, `sleep_quality`, `safety`, `basic_needs`, `academic_performance`, `teacher_student_relationship`, `social_support`
  - Must include stressor factors for composite indices

- **Expected Size**: 
  - Minimum: 100 rows
  - Recommended: 500+ rows
  - Maximum: No limit

- **Data Quality**:
  - No missing values (NaN) allowed in feature columns
  - Numeric values only (except target)
  - Target must be categorical (0, 1, 2)

#### 2. Stress_Dataset.csv (Dataset 2)
- **Format**: CSV with header row (or auto-detected)
- **Expected Columns** (26 total):
  ```
  Gender, Age, Stress_Recent, Heart_Rate, Anxiety_Tension,
  Sleep_Problems, Anxiety_Tension_2, Headaches_Often,
  Irritability, Concentration_Difficulty, Sadness_Low_Mood,
  Illness_Health_Issues, Lonely_Isolated, Academic_Overload,
  Peer_Competition, Relationship_Stress, Professor_Difficulty,
  Working_Environment_Stress, Relaxation_Struggle, Home_Hostel_Difficulties,
  Academic_Confidence_Lack, Subject_Confidence_Lack, Activity_Conflict,
  Classes_Regularity, Weight_Change, Stress_Type
  ```

- **Target Column**: `Stress_Type`
  - Allowed values: "Eustress (Positive Stress) - Stress that motivates and enhances performance.", "Distress (Negative Stress) - Stress that causes anxiety and impairs well-being.", "No Stress - Currently experiencing minimal to no stress."
  - Or simplified: "Eustress", "Distress", "No Stress"

- **Expected Size**:
  - Minimum: 200 rows
  - Recommended: 500+ rows
  - Handles imbalanced classes automatically

- **Data Quality**:
  - Handles age outliers automatically
  - Detects and removes straight-line responses
  - Gender: 0 (Male) or 1 (Female)
  - Survey questions: 1-5 scale

### Dataset Placement
```
project_directory/
│
├── stress_classification.py    # Main code file
├── requirements.txt            # Dependencies
├── StressLevelDataset.csv     # Dataset 1 (REQUIRED)
├── Stress_Dataset.csv         # Dataset 2 (REQUIRED)
└── outputs/                   # Auto-created for visualizations
```

### Sample Dataset Validation
```python
import pandas as pd

# Validate Dataset 1
df1 = pd.read_csv('StressLevelDataset.csv')
assert 'stress_level' in df1.columns, "Missing 'stress_level' column"
assert df1['stress_level'].isin([0, 1, 2]).all(), "Invalid stress levels"
print(f"✓ Dataset 1 valid: {df1.shape}")

# Validate Dataset 2
df2 = pd.read_csv('Stress_Dataset.csv')
assert 'Stress_Type' in df2.columns, "Missing 'Stress_Type' column"
print(f"✓ Dataset 2 valid: {df2.shape}")
```

---

## Hardware Requirements

### Minimum Requirements
- **CPU**: Dual-core processor (Intel i3/AMD Ryzen 3 or equivalent)
- **RAM**: 4 GB
- **Disk Space**: 500 MB free space
- **Runtime**: ~5-10 minutes for full pipeline

### Recommended Requirements
- **CPU**: Quad-core processor (Intel i5/AMD Ryzen 5 or equivalent)
- **RAM**: 8 GB
- **Disk Space**: 2 GB free space
- **Runtime**: ~2-5 minutes for full pipeline

### For SHAP Analysis (Phase 9)
- **CPU**: Hexa-core or better (Intel i7/AMD Ryzen 7+)
- **RAM**: 16 GB (SHAP is memory-intensive)
- **GPU**: Not required (SHAP TreeExplainer runs on CPU)
- **Runtime**: +10-30 minutes for full SHAP computation

### Performance Optimization
```python
# Set number of CPU cores for parallel processing
import os
os.environ['OMP_NUM_THREADS'] = '4'  # Adjust based on your CPU
os.environ['OPENBLAS_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '4'
```

---

## Environment Setup

### Complete Setup Script (Linux/macOS)

Create `setup.sh`:
```bash
#!/bin/bash

echo "=== Stress Classification Pipeline Setup ==="

# 1. Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# 2. Create virtual environment
echo "Creating virtual environment..."
python3 -m venv stress_env
source stress_env/bin/activate

# 3. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# 4. Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# 5. Verify installation
echo "Verifying installation..."
python3 << EOF
import numpy
import pandas
import sklearn
import imblearn
import matplotlib
import seaborn
print("\n✓ All core dependencies installed successfully")
print(f"  - NumPy: {numpy.__version__}")
print(f"  - Pandas: {pandas.__version__}")
print(f"  - scikit-learn: {sklearn.__version__}")
print(f"  - imbalanced-learn: {imblearn.__version__}")
print(f"  - Matplotlib: {matplotlib.__version__}")
print(f"  - Seaborn: {seaborn.__version__}")
EOF

# 6. Create output directory
mkdir -p outputs

echo "\n=== Setup Complete ==="
echo "To activate the environment:"
echo "  source stress_env/bin/activate"
echo "\nTo run the pipeline:"
echo "  python stress_classification.py"
```

Run the script:
```bash
chmod +x setup.sh
./setup.sh
```

### Complete Setup Script (Windows)

Create `setup.bat`:
```batch
@echo off
echo === Stress Classification Pipeline Setup ===

REM 1. Check Python version
python --version

REM 2. Create virtual environment
echo Creating virtual environment...
python -m venv stress_env
call stress_env\Scripts\activate.bat

REM 3. Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM 4. Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM 5. Verify installation
echo Verifying installation...
python -c "import numpy, pandas, sklearn, imblearn, matplotlib, seaborn; print('\n✓ All dependencies installed')"

REM 6. Create output directory
if not exist outputs mkdir outputs

echo.
echo === Setup Complete ===
echo To activate the environment:
echo   stress_env\Scripts\activate.bat
echo.
echo To run the pipeline:
echo   python stress_classification.py

pause
```

Run by double-clicking `setup.bat` or:
```cmd
setup.bat
```

---

## Verification & Testing

### Test Installation
```bash
# Activate environment
source stress_env/bin/activate  # Linux/macOS
# OR
stress_env\Scripts\activate     # Windows

# Run verification
python << EOF
import sys
import numpy as np
import pandas as pd
import sklearn
import imblearn

print("Python version:", sys.version)
print("\nPackage versions:")
print(f"  NumPy:             {np.__version__}")
print(f"  Pandas:            {pd.__version__}")
print(f"  scikit-learn:      {sklearn.__version__}")
print(f"  imbalanced-learn:  {imblearn.__version__}")

# Test critical functions
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import RobustScaler

print("\n✓ All critical imports successful")
print("✓ System ready for execution")
EOF
```

### Expected Output
```
Python version: 3.10.x ...

Package versions:
  NumPy:             1.24.3
  Pandas:            2.0.3
  scikit-learn:      1.3.2
  imbalanced-learn:  0.11.0

✓ All critical imports successful
✓ System ready for execution
```

### Dry Run Test
```python
# Create test_pipeline.py
import pandas as pd
import numpy as np

# Create dummy datasets
np.random.seed(42)

# Dataset 1
df1_test = pd.DataFrame({
    'self_esteem': np.random.randint(0, 6, 100),
    'sleep_quality': np.random.randint(0, 6, 100),
    'anxiety_level': np.random.randint(0, 22, 100),
    'depression': np.random.randint(0, 22, 100),
    'study_load': np.random.randint(0, 22, 100),
    'stress_level': np.random.randint(0, 3, 100)
})
df1_test.to_csv('StressLevelDataset_test.csv', index=False)

# Dataset 2
df2_test = pd.DataFrame({
    'Gender': np.random.randint(0, 2, 200),
    'Age': np.random.randint(18, 25, 200),
    'Anxiety_Tension': np.random.randint(1, 6, 200),
    'Classes_Regularity': np.random.randint(1, 6, 200),
    'Stress_Type': np.random.choice(['Eustress', 'Distress', 'No Stress'], 200)
})
df2_test.to_csv('Stress_Dataset_test.csv', index=False)

print("✓ Test datasets created")
```

---

## Troubleshooting

### Common Issues

#### Issue 1: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'sklearn'
```
**Solution:**
```bash
# Ensure virtual environment is activated
source stress_env/bin/activate  # Linux/macOS
stress_env\Scripts\activate     # Windows

# Reinstall scikit-learn
pip install scikit-learn==1.3.2
```

#### Issue 2: Incompatible numpy version
```
ValueError: numpy.ndarray size changed, may indicate binary incompatibility
```
**Solution:**
```bash
# Uninstall and reinstall numpy
pip uninstall numpy -y
pip install numpy==1.24.3 --no-cache-dir
```

#### Issue 3: SMOTE ImportError
```
ImportError: cannot import name 'SMOTE' from 'imblearn.over_sampling'
```
**Solution:**
```bash
pip install imbalanced-learn==0.11.0
```

#### Issue 4: Dataset not found
```
FileNotFoundError: [Errno 2] No such file or directory: 'StressLevelDataset.csv'
```
**Solution:**
- Verify datasets are in the same directory as the script
- Check file names (case-sensitive on Linux/macOS)
- Use absolute paths if necessary:
  ```python
  df1 = pd.read_csv('/full/path/to/StressLevelDataset.csv')
  ```

#### Issue 5: Memory Error (during SHAP)
```
MemoryError: Unable to allocate array
```
**Solution:**
```python
# Reduce SHAP computation size
shap_values = explainer.shap_values(X_test[:100])  # First 100 samples only

# Or use approximate SHAP
explainer = shap.TreeExplainer(model, X_train.sample(100))
```

#### Issue 6: Matplotlib display issues (headless servers)
```
_tkinter.TclError: no display name and no $DISPLAY environment variable
```
**Solution:**
```python
# Add at the top of the script
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
```

---

## Optional Dependencies

### For Jupyter Notebook (Phase 9 - SHAP Analysis)
```bash
pip install jupyter notebook ipykernel ipywidgets
```

Launch Jupyter:
```bash
jupyter notebook
```

### For Enhanced Progress Tracking
```bash
pip install tqdm
```

Usage in code:
```python
from tqdm import tqdm
for i in tqdm(range(100), desc="Processing"):
    # Your code here
    pass
```

### For Excel Export (Results)
```bash
pip install openpyxl xlsxwriter
```

Export results:
```python
results_df.to_excel('model_results.xlsx', index=False)
```

### For PDF Report Generation
```bash
pip install reportlab fpdf
```

### For Advanced Statistical Tests
```bash
pip install statsmodels pingouin
```

---

## Development Environment (Optional)

### For Code Development
```bash
# Linting & formatting
pip install black flake8 pylint

# Type checking
pip install mypy

# Testing
pip install pytest pytest-cov

# Documentation
pip install sphinx sphinx-rtd-theme
```

### Pre-commit Hooks (Code Quality)
Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        language_version: python3.10
```

Install:
```bash
pip install pre-commit
pre-commit install
```

---

## Version Compatibility Matrix

| Component | Tested Versions | Status |
|-----------|----------------|--------|
| Python | 3.8, 3.9, 3.10, 3.11 | ✅ Compatible |
| Python | 3.12+ | ❌ Not supported yet |
| NumPy | 1.21.x - 1.26.x | ✅ Compatible |
| Pandas | 1.3.x - 2.1.x | ✅ Compatible |
| scikit-learn | 1.0.x - 1.3.x | ✅ Compatible |
| imbalanced-learn | 0.10.x - 0.11.x | ✅ Compatible |
| SHAP | 0.41.x - 0.44.x | ✅ Compatible |

---

## Support & Resources

### Documentation
- **scikit-learn**: https://scikit-learn.org/stable/
- **imbalanced-learn**: https://imbalanced-learn.org/stable/
- **SHAP**: https://shap.readthedocs.io/
- **Pandas**: https://pandas.pydata.org/docs/
- **Seaborn**: https://seaborn.pydata.org/

### Community Support
- **Stack Overflow**: Tag questions with `scikit-learn`, `machine-learning`, `shap`
- **GitHub Issues**: Report bugs or request features

### Citation
If using this pipeline in academic work:
```bibtex
@software{stress_classification_2025,
  title={Robust Stress Classification Pipeline},
  subtitle={Integrating Academic, Social, and Health Indicators},
  year={2025},
  version={1.0.0}
}
```

---

## License Requirements

This pipeline uses the following open-source licenses:
- **scikit-learn**: BSD-3-Clause
- **imbalanced-learn**: MIT
- **SHAP**: MIT
- **Pandas**: BSD-3-Clause
- **NumPy**: BSD-3-Clause
- **Matplotlib**: PSF-based
- **Seaborn**: BSD-3-Clause

All dependencies are compatible with academic and commercial use.

---

**Last Updated**: 2025-11-06  
**Maintainer**: [lakshita]