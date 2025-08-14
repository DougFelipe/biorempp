# 🔍 Checklist de Validação TestPyPI - BioRemPP

## Pre-Upload Validation

### ✅ Build System Check
```bash
# Verify build tools are installed
python -m build --version
twine --version
```

### ✅ Package Build Check
```bash
# Clean build
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
python -m build

# Verify files are created
ls dist/
# Expected: biorempp-X.Y.Z-py3-none-any.whl and biorempp-X.Y.Z.tar.gz
```

### ✅ Package Integrity Check
```bash
# All checks must pass
twine check dist/*
# Expected output: All files PASSED
```

### ✅ Version Check
```bash
# Verify version format (PEP 440 compliant, no local segments)
python -c "import setuptools_scm; print(setuptools_scm.get_version())"
# Expected: X.Y.Z.postN.devM or X.Y.Z.devN (no +local suffix)
```

## Upload Validation

### ✅ Environment Setup
```powershell
# Set authentication
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-YOUR_TESTPYPI_TOKEN_HERE"
```

### ✅ Upload to TestPyPI
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# Expected: Successful upload message
```

## Post-Upload Validation

### ✅ Fresh Environment Setup
```bash
# Create clean virtual environment
python -m venv test_env
test_env\Scripts\activate  # Windows
# source test_env/bin/activate  # Linux/Mac
```

### ✅ Installation from TestPyPI
```bash
# Install from TestPyPI
pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ biorempp

# Verify installation
pip list | findstr biorempp
```

### ✅ Import Test
```bash
# Test Python import
python -c "import biorempp; print(f'BioRemPP version: {biorempp.__version__}')"
# Expected: Version number without errors
```

### ✅ CLI Test
```bash
# Test command line interface
biorempp --help
# Expected: Help text displayed

biorempp --version
# Expected: Version displayed

biorempp info
# Expected: System information displayed
```

### ✅ Minimal E2E Test
```bash
# Create test input file
echo -e "compound1\ncompound2\ncompound3" > test_input.txt

# Test single database processing
biorempp --input test_input.txt --database biorempp --output test_output.txt
# Expected: Output file created without errors

# Verify output
cat test_output.txt
# Expected: Structured output with results

# Cleanup
rm test_input.txt test_output.txt
```

### ✅ Package Metadata Verification
```bash
# Check package metadata
pip show biorempp
# Verify:
# - Name: biorempp
# - Version: correct format
# - Author: Douglas Felipe
# - Requires: pandas, numpy, tqdm, click
```

### ✅ Dependencies Check
```bash
# Verify all dependencies installed correctly
python -c "import pandas, numpy, tqdm, click; print('All dependencies OK')"
# Expected: No import errors
```

### ✅ Data Files Check
```bash
# Verify data files are included
python -c "
import biorempp
import pkg_resources
import os

# Check for data files
pkg_path = pkg_resources.resource_filename('biorempp', 'data')
files = os.listdir(pkg_path)
print(f'Data files found: {files}')
print(f'Expected: CSV and TXT files')
"
```

## Error Troubleshooting

### 🔧 Common Issues

#### Build Errors
- Check Python version >= 3.8
- Update setuptools: `pip install -U setuptools setuptools_scm wheel`
- Verify git repository is clean

#### Upload Errors  
- Verify token permissions
- Check token format (starts with `pypi-`)
- Ensure TestPyPI account has project permissions

#### Installation Errors
- Use `--no-cache-dir` flag
- Verify network connectivity to TestPyPI
- Check for conflicting package versions

#### Import Errors
- Verify virtual environment is activated
- Check package installation: `pip list`
- Test minimal import: `python -c "import biorempp"`

#### CLI Errors
- Check entry point installation: `pip show -f biorempp | findstr Scripts`
- Verify PATH includes Python scripts directory
- Test direct module call: `python -m biorempp --help`

## Success Criteria

### ✅ All checks must pass:
- [ ] Package builds without errors
- [ ] `twine check` passes all files  
- [ ] Version is PEP 440 compliant (no +local suffix)
- [ ] Upload to TestPyPI succeeds
- [ ] Fresh installation works
- [ ] `import biorempp` succeeds
- [ ] `biorempp --help` displays correctly
- [ ] Basic E2E test completes
- [ ] All dependencies resolve correctly
- [ ] Data files are accessible

### 🎯 Ready for Production PyPI
Only proceed to production PyPI upload if ALL validation checks pass successfully.
