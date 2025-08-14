#!/usr/bin/env python3
"""
Automated TestPyPI Upload Script for biorempp

This script automates the complete workflow for uploading packages to TestPyPI:
1. Cleans previous builds
2. Builds the package
3. Checks package integrity
4. Uploads to TestPyPI
5. Provides installation instructions

Usage:
    python scripts/upload_to_testpypi.py
    python scripts/upload_to_testpypi.py --skip-build
    python scripts/upload_to_testpypi.py --verbose
"""

import sys
import subprocess
import shutil
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_step(message, step_num=None):
    """Print a formatted step message."""
    if step_num:
        print(f"\n{Colors.BLUE}{Colors.BOLD}[Step {step_num}]{Colors.END} {message}")
    else:
        print(f"\n{Colors.BLUE}{Colors.BOLD}•{Colors.END} {message}")


def print_success(message):
    """Print a success message."""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")


def print_error(message):
    """Print an error message."""
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def run_command(command, description, check=True, capture_output=False):
    """
    Run a shell command with error handling.
    
    Args:
        command (list): Command to run as list of strings
        description (str): Description of what the command does
        check (bool): Whether to raise exception on non-zero exit
        capture_output (bool): Whether to capture and return output
        
    Returns:
        subprocess.CompletedProcess: Result of the command
    """
    print(f"  → {description}")
    
    try:
        result = subprocess.run(
            command,
            check=check,
            capture_output=capture_output,
            text=True,
            cwd=Path.cwd()
        )
        
        if capture_output and result.stdout:
            print(f"    Output: {result.stdout.strip()}")
            
        return result
        
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(command)}")
        if e.stdout:
            print(f"    stdout: {e.stdout}")
        if e.stderr:
            print(f"    stderr: {e.stderr}")
        raise
    except FileNotFoundError:
        print_error(f"Command not found: {command[0]}")
        print("    Make sure the required tools are installed.")
        raise


def check_pypirc_exists():
    """Check if .pypirc file exists and has TestPyPI configuration."""
    home_dir = Path.home()
    pypirc_path = home_dir / ".pypirc"
    
    if not pypirc_path.exists():
        return False, "File does not exist"
    
    try:
        with open(pypirc_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '[testpypi]' not in content:
            return False, "No TestPyPI configuration found"
            
        if 'YOUR_TESTPYPI_TOKEN_HERE' in content:
            return False, "Token placeholder not replaced"
            
        return True, "Configuration looks good"
        
    except Exception as e:
        return False, f"Error reading file: {e}"


def clean_dist_directory():
    """Remove existing dist directory to ensure clean build."""
    dist_path = Path("dist")
    
    if dist_path.exists():
        print("  → Removing existing dist/ directory")
        shutil.rmtree(dist_path)
        print_success("Cleaned dist/ directory")
    else:
        print("  → No existing dist/ directory found")


def build_package():
    """Build the package using python -m build."""
    run_command(
        [sys.executable, "-m", "build"],
        "Building package with python -m build"
    )


def check_package():
    """Check package integrity with twine."""
    run_command(
        ["twine", "check", "dist/*"],
        "Checking package integrity with twine"
    )


def upload_to_testpypi():
    """Upload package to TestPyPI."""
    run_command(
        ["twine", "upload", "--repository", "testpypi", "dist/*"],
        "Uploading to TestPyPI"
    )


def get_package_info():
    """Get package name and version from pyproject.toml."""
    try:
        import tomllib
    except ImportError:
        # Fallback for Python < 3.11
        try:
            import tomli as tomllib
        except ImportError:
            print_warning("Cannot read pyproject.toml (tomllib/tomli not available)")
            return "biorempp", "unknown"
    
    try:
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
            
        project = data.get("project", {})
        name = project.get("name", "biorempp")
        version = project.get("version", "unknown")
        
        return name, version
        
    except Exception as e:
        print_warning(f"Could not read package info: {e}")
        return "biorempp", "unknown"


def show_installation_instructions():
    """Show instructions for installing from TestPyPI."""
    package_name, version = get_package_info()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Upload Successful!{Colors.END}")
    print(f"\n{Colors.BOLD}Package Information:{Colors.END}")
    print(f"  Name: {package_name}")
    print(f"  Version: {version}")
    
    print(f"\n{Colors.BOLD}🔗 TestPyPI URLs:{Colors.END}")
    print(f"  Package page: https://test.pypi.org/project/{package_name}/")
    print(f"  Specific version: https://test.pypi.org/project/"
          f"{package_name}/{version}/")
    
    print(f"\n{Colors.BOLD}📦 Installation Commands:{Colors.END}")
    print("  # Install from TestPyPI")
    print(f"  pip install --index-url https://test.pypi.org/simple/ {package_name}")
    print("")
    print("  # Install specific version")
    print(f"  pip install --index-url https://test.pypi.org/simple/ "
          f"{package_name}=={version}")
    print("")
    print("  # Install with extra dependencies (if needed)")
    print(f"  pip install --index-url https://test.pypi.org/simple/ "
          f"--extra-index-url https://pypi.org/simple/ {package_name}")
    
    print(f"\n{Colors.BOLD}🧪 Testing Commands:{Colors.END}")
    print("  # Test the installation")
    print(f"  python -c \"import {package_name}; print({package_name}.__version__)\"")
    print("")
    print("  # Test CLI (if available)")
    print(f"  python -m {package_name} --help")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automated TestPyPI upload for biorempp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/upload_to_testpypi.py
  python scripts/upload_to_testpypi.py --skip-build
  python scripts/upload_to_testpypi.py --verbose

Prerequisites:
  - .pypirc configured with TestPyPI token
  - build and twine packages installed
  - Clean working directory (committed changes)
        """
    )
    
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip the build step (use existing dist/ files)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show more detailed output"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually doing it"
    )
    
    args = parser.parse_args()
    
    print(f"{Colors.BOLD}🚀 TestPyPI Upload Script for biorempp{Colors.END}")
    print("=" * 50)
    
    if args.dry_run:
        print_warning("DRY RUN MODE - No changes will be made")
    
    try:
        # Step 1: Check prerequisites
        print_step("Checking prerequisites", 1)
        
        # Check if we're in the right directory
        if not Path("pyproject.toml").exists():
            print_error("pyproject.toml not found. Are you in the project root?")
            sys.exit(1)
        print_success("Found pyproject.toml")
        
        # Check .pypirc configuration
        pypirc_ok, pypirc_msg = check_pypirc_exists()
        if not pypirc_ok:
            print_error(f".pypirc configuration issue: {pypirc_msg}")
            print("  Run: python scripts/create_pypirc.py --help")
            sys.exit(1)
        print_success(f".pypirc configuration: {pypirc_msg}")
        
        # Check required tools
        for tool in ["build", "twine"]:
            try:
                run_command(
                    [sys.executable, "-m", tool, "--help"],
                    f"Checking {tool} availability",
                    capture_output=True
                )
                print_success(f"{tool} is available")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print_error(f"{tool} is not available")
                print(f"  Install with: pip install {tool}")
                sys.exit(1)
        
        if args.dry_run:
            print("\n✅ Dry run complete - all prerequisites met")
            return
        
        # Step 2: Clean previous builds (if not skipping build)
        if not args.skip_build:
            print_step("Cleaning previous builds", 2)
            clean_dist_directory()
        
        # Step 3: Build package (if not skipping)
        if not args.skip_build:
            print_step("Building package", 3)
            build_package()
            print_success("Package built successfully")
        else:
            print_step("Skipping build (using existing dist/ files)", 3)
        
        # Step 4: Check package integrity
        print_step("Checking package integrity", 4)
        check_package()
        print_success("Package integrity check passed")
        
        # Step 5: Upload to TestPyPI
        print_step("Uploading to TestPyPI", 5)
        upload_to_testpypi()
        print_success("Upload completed successfully")
        
        # Step 6: Show installation instructions
        print_step("Upload complete!", 6)
        show_installation_instructions()
        
    except KeyboardInterrupt:
        print_error("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
