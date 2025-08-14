# PowerShell script for TestPyPI upload workflow
# Usage: .\upload-to-testpypi.ps1

# Set error handling
$ErrorActionPreference = "Stop"

Write-Host "🚀 BioRemPP TestPyPI Upload Workflow" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Step 1: Clean dist/
Write-Host "`n📁 Step 1: Cleaning dist/ directory..." -ForegroundColor Yellow
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "✅ Cleaned dist/ directory" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No dist/ directory found" -ForegroundColor Blue
}

# Step 2: Build package
Write-Host "`n🔨 Step 2: Building package..." -ForegroundColor Yellow
python -m build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Package built successfully" -ForegroundColor Green

# Step 3: Check package integrity
Write-Host "`n🔍 Step 3: Checking package integrity..." -ForegroundColor Yellow
twine check dist/*
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Package integrity check failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Package integrity check passed" -ForegroundColor Green

# Step 4: Upload to TestPyPI
Write-Host "`n📤 Step 4: Uploading to TestPyPI..." -ForegroundColor Yellow
Write-Host "Environment variables needed:" -ForegroundColor Cyan
Write-Host "  TWINE_USERNAME=__token__" -ForegroundColor Gray
Write-Host "  TWINE_PASSWORD=pypi-YOUR_TESTPYPI_TOKEN" -ForegroundColor Gray

# Check if environment variables are set
if (-not $env:TWINE_USERNAME -or -not $env:TWINE_PASSWORD) {
    Write-Host "⚠️  Environment variables not set. Setting defaults..." -ForegroundColor Yellow
    $env:TWINE_USERNAME = "__token__"
    if (-not $env:TWINE_PASSWORD) {
        Write-Host "❌ TWINE_PASSWORD environment variable not set!" -ForegroundColor Red
        Write-Host "Set it with: `$env:TWINE_PASSWORD='pypi-YOUR_TESTPYPI_TOKEN'" -ForegroundColor Yellow
        exit 1
    }
}

twine upload --repository-url https://test.pypi.org/legacy/ dist/*
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Upload to TestPyPI failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 Upload completed successfully!" -ForegroundColor Green
Write-Host "`n📦 Test installation with:" -ForegroundColor Cyan
Write-Host "pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ biorempp" -ForegroundColor Gray

Write-Host "`n🧪 Test the package:" -ForegroundColor Cyan
Write-Host "python -c `"import biorempp; print(biorempp.__version__)`"" -ForegroundColor Gray
Write-Host "biorempp --help" -ForegroundColor Gray
