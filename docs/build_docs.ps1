# ============================================================================
# BioRemPP Documentation Build Script
# PowerShell script for building Sphinx documentation on Windows
# ============================================================================

param(
    [switch]$Clean,
    [switch]$Api,
    [switch]$Html,
    [switch]$Help,
    [switch]$All
)

# Configuration
$SourceDir = "."
$BuildDir = "_build"
$ApiDir = "api"
$PackagePath = "..\src\biorempp"

# Colors for output
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Cyan"
$WarningColor = "Yellow"

function Write-Status {
    param($Message, $Color = "White")
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $Message" -ForegroundColor $Color
}

function Show-Help {
    Write-Host @"
BioRemPP Documentation Build Script
==================================

Usage:
    .\build_docs.ps1 [options]

Options:
    -Clean    Remove all build artifacts and API stubs
    -Api      Generate API documentation stubs only
    -Html     Build HTML documentation (includes API generation)
    -All      Clean + Generate API + Build HTML (complete rebuild)
    -Help     Show this help message

Examples:
    .\build_docs.ps1 -Html          # Build documentation
    .\build_docs.ps1 -All           # Complete rebuild
    .\build_docs.ps1 -Clean         # Clean build artifacts
    .\build_docs.ps1 -Api           # Generate API stubs only

"@ -ForegroundColor $InfoColor
}

function Clean-Build {
    Write-Status "Cleaning build artifacts..." $InfoColor

    if (Test-Path $BuildDir) {
        Remove-Item -Recurse -Force $BuildDir
        Write-Status "Removed build directory" $SuccessColor
    }

    if (Test-Path $ApiDir) {
        Remove-Item -Recurse -Force $ApiDir
        Write-Status "Removed API documentation" $SuccessColor
    }
}

function Generate-Api {
    Write-Status "Generating API documentation..." $InfoColor

    if (-not (Test-Path $PackagePath)) {
        Write-Status "Package path not found: $PackagePath" $ErrorColor
        return $false
    }

    try {
        $cmd = "python -m sphinx.ext.apidoc -o `"$ApiDir`" `"$PackagePath`" -f -e -M --implicit-namespaces"
        Write-Status "Running: $cmd" $InfoColor
        Invoke-Expression $cmd

        if ($LASTEXITCODE -eq 0) {
            Write-Status "API documentation generated successfully" $SuccessColor
            return $true
        } else {
            Write-Status "API generation failed with exit code $LASTEXITCODE" $ErrorColor
            return $false
        }
    }
    catch {
        Write-Status "Error generating API documentation: $($_.Exception.Message)" $ErrorColor
        return $false
    }
}

function Build-Html {
    Write-Status "Building HTML documentation..." $InfoColor

    try {
        # Build com warnings filtrados
        $cmd = "sphinx-build -b html -q -W --keep-going `"$SourceDir`" `"$BuildDir\html`""
        Write-Status "Running: $cmd" $InfoColor
        Invoke-Expression $cmd

        if ($LASTEXITCODE -eq 0) {
            Write-Status "HTML documentation built successfully" $SuccessColor
            $indexPath = Join-Path $BuildDir "html\index.html"
            if (Test-Path $indexPath) {
                Write-Status "Documentation available at: $indexPath" $InfoColor
            }
            return $true
        } else {
            # Se falhou com -W, tenta sem -W para ver warnings
            Write-Status "Build failed with warnings as errors. Rebuilding to show warnings..." $WarningColor
            $cmd = "sphinx-build -b html -n `"$SourceDir`" `"$BuildDir\html`""
            Invoke-Expression $cmd

            if ($LASTEXITCODE -eq 0) {
                Write-Status "HTML documentation built with warnings" $WarningColor
                return $true
            } else {
                Write-Status "HTML build failed with exit code $LASTEXITCODE" $ErrorColor
                return $false
            }
        }
    }
    catch {
        Write-Status "Error building HTML documentation: $($_.Exception.Message)" $ErrorColor
        return $false
    }
}

function Test-Environment {
    Write-Status "Checking environment..." $InfoColor

    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Status "Python: $pythonVersion" $SuccessColor
    }
    catch {
        Write-Status "Python not found in PATH" $ErrorColor
        return $false
    }

    # Check Sphinx
    try {
        $sphinxVersion = python -c "import sphinx; print(f'Sphinx {sphinx.__version__}')" 2>&1
        Write-Status "$sphinxVersion" $SuccessColor
    }
    catch {
        Write-Status "Sphinx not installed" $ErrorColor
        return $false
    }

    # Check MyST Parser
    try {
        $mystVersion = python -c "import myst_parser; print(f'MyST Parser {myst_parser.__version__}')" 2>&1
        Write-Status "$mystVersion" $SuccessColor
    }
    catch {
        Write-Status "MyST Parser not installed" $ErrorColor
        return $false
    }

    return $true
}

# Main execution
Write-Status "BioRemPP Documentation Build Script" $InfoColor
Write-Status "=================================" $InfoColor

if ($Help) {
    Show-Help
    exit 0
}

if (-not (Test-Environment)) {
    Write-Status "Environment check failed. Please ensure Python, Sphinx, and MyST Parser are installed." $ErrorColor
    exit 1
}

$success = $true

if ($Clean -or $All) {
    Clean-Build
}

if ($Api -or $Html -or $All) {
    if (-not (Generate-Api)) {
        $success = $false
    }
}

if ($Html -or $All) {
    if (-not (Build-Html)) {
        $success = $false
    }
}

if (-not ($Clean -or $Api -or $Html -or $All)) {
    Write-Status "No action specified. Use -Help for usage information." $WarningColor
    Show-Help
    exit 0
}

if ($success) {
    Write-Status "Documentation build completed successfully!" $SuccessColor
    exit 0
} else {
    Write-Status "Documentation build failed!" $ErrorColor
    exit 1
}
