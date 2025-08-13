# PyPI Configuration Guide

This directory contains templates and scripts to help you configure PyPI uploads for the biorempp package.

## Quick Start

### Option 1: Automatic Setup (Recommended)
```bash
# Basic setup - you'll need to add tokens manually afterward
python scripts/configure_pypi.py

# Setup with tokens (replace with your actual tokens)
python scripts/configure_pypi.py \
    --pypi-token "pypi-YOUR_PYPI_TOKEN_HERE" \
    --testpypi-token "pypi-YOUR_TESTPYPI_TOKEN_HERE"
```

### Option 2: Manual Setup
1. Copy `scripts/.pypirc_template` to your home directory as `.pypirc`
2. Edit the file and replace the token placeholders
3. Save and secure the file

## Files Overview

- **`.pypirc_template`**: Ready-to-use PyPI configuration template
- **`configure_pypi.py`**: Automated setup script
- **`pypirc_example`**: Legacy example file (Portuguese)

## Getting Your Tokens

### 1. PyPI Production Token
1. Go to https://pypi.org/manage/account/#api-tokens
2. Click "Add API token"
3. Name: `biorempp-upload` (or your preferred name)
4. Scope: "Entire account" (for first upload)
5. Copy the generated token (starts with `pypi-`)

### 2. TestPyPI Token  
1. Go to https://test.pypi.org/manage/account/#api-tokens
2. Click "Add API token"
3. Name: `biorempp-test-upload`
4. Scope: "Entire account"
5. Copy the generated token (starts with `pypi-`)

## File Locations

The `.pypirc` file should be placed in:
- **Windows**: `C:\Users\USERNAME\.pypirc`
- **Linux/Mac**: `~/.pypirc`

## Upload Commands

### Testing on TestPyPI (Always do this first!)
```bash
# Build the package
python -m build

# Check the package
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ biorempp
```

### Production Upload to PyPI
```bash
# Upload to PyPI (only after testing on TestPyPI)
twine upload --repository pypi dist/*

# Or simply (uses pypi by default)
twine upload dist/*
```

## Configuration Script Usage

```bash
# Show current configuration and paths
python scripts/configure_pypi.py --show-info

# Force overwrite existing .pypirc
python scripts/configure_pypi.py --force

# Get help
python scripts/configure_pypi.py --help
```

## Security Best Practices

1. **Never commit `.pypirc` to version control**
2. **Set appropriate file permissions**:
   ```bash
   # On Linux/Mac
   chmod 600 ~/.pypirc
   ```
3. **Use project-specific tokens** after initial upload
4. **Regularly rotate your tokens**
5. **Keep tokens secure and private**

## Troubleshooting

### Authentication Errors
- Verify tokens are correct and not expired
- Ensure `.pypirc` is in the correct location
- Check for extra spaces or characters in tokens

### File Not Found
- Use `configure_pypi.py --show-info` to verify paths
- Ensure the file has no extension (not `.pypirc.txt`)

### Permission Denied
- On Unix systems: `chmod 600 ~/.pypirc`
- On Windows: Check user folder permissions

### Package Already Exists
- You cannot overwrite existing versions on PyPI
- Increment version number in `pyproject.toml`
- Test on TestPyPI first with new version

## Complete Upload Workflow

1. **Setup authentication** (one time):
   ```bash
   python scripts/configure_pypi.py --show-info
   python scripts/configure_pypi.py
   # Edit .pypirc with your tokens
   ```

2. **Test upload** (every release):
   ```bash
   python -m build
   twine check dist/*
   twine upload --repository testpypi dist/*
   ```

3. **Production upload**:
   ```bash
   twine upload --repository pypi dist/*
   ```

4. **Verify installation**:
   ```bash
   pip install biorempp
   python -c "import biorempp; print(biorempp.__version__)"
   ```
