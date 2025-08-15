#!/usr/bin/env python3
"""
PyPI Configuration Setup Script

This script helps you set up the .pypirc file automatically.
It will copy the template to the correct location and optionally
insert your tokens.

Usage:
    python configure_pypi.py
    python configure_pypi.py --pypi-token "pypi-YOUR_TOKEN" \\
                             --testpypi-token "pypi-YOUR_TOKEN"
"""

import os
import platform
import shutil
from pathlib import Path


def get_home_directory():
    """Get the user's home directory path."""
    return Path.home()


def get_pypirc_path():
    """Get the correct path for .pypirc file based on the operating system."""
    return get_home_directory() / ".pypirc"


def get_template_path():
    """Get the path to the .pypirc template file."""
    script_dir = Path(__file__).parent
    return script_dir / ".pypirc_template"


def create_pypirc_from_template(pypi_token=None, testpypi_token=None):
    """
    Create .pypirc file from template with optional token replacement.
    
    Args:
        pypi_token (str): PyPI production token
        testpypi_token (str): TestPyPI token
        
    Returns:
        bool: True if successful, False otherwise
    """
    template_path = get_template_path()
    pypirc_path = get_pypirc_path()
    
    if not template_path.exists():
        print(f"❌ Template file not found: {template_path}")
        return False
    
    try:
        # Read template content
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace tokens if provided
        if pypi_token:
            content = content.replace("YOUR_PYPI_TOKEN_HERE", pypi_token)
        if testpypi_token:
            content = content.replace("YOUR_TESTPYPI_TOKEN_HERE", testpypi_token)
        
        # Write to .pypirc location
        with open(pypirc_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Set appropriate permissions on Unix systems
        if platform.system() != "Windows":
            os.chmod(pypirc_path, 0o600)
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .pypirc file: {e}")
        return False


def check_existing_pypirc():
    """Check if .pypirc already exists."""
    pypirc_path = get_pypirc_path()
    return pypirc_path.exists()


def backup_existing_pypirc():
    """Create a backup of existing .pypirc file."""
    pypirc_path = get_pypirc_path()
    backup_path = pypirc_path.with_suffix('.pypirc.backup')
    
    try:
        shutil.copy2(pypirc_path, backup_path)
        print(f"📄 Existing .pypirc backed up to: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to backup existing .pypirc: {e}")
        return False


def main():
    """Main function with command line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Configure .pypirc file for PyPI uploads",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python configure_pypi.py
  python configure_pypi.py --pypi-token "pypi-ABC123..." \\
                           --testpypi-token "pypi-XYZ789..."
  python configure_pypi.py --force
  python configure_pypi.py --show-info

For token generation:
  PyPI: https://pypi.org/manage/account/#api-tokens
  TestPyPI: https://test.pypi.org/manage/account/#api-tokens
        """
    )
    
    parser.add_argument(
        "--pypi-token",
        help="PyPI production token (starts with 'pypi-')"
    )
    parser.add_argument(
        "--testpypi-token",
        help="TestPyPI token (starts with 'pypi-')"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing .pypirc file"
    )
    parser.add_argument(
        "--show-info",
        action="store_true",
        help="Show configuration information and paths"
    )
    
    args = parser.parse_args()
    
    # Show information if requested
    if args.show_info:
        print("🔧 PyPI Configuration Information")
        print("=" * 50)
        print(f"🏠 Home directory: {get_home_directory()}")
        print(f"📄 .pypirc location: {get_pypirc_path()}")
        print(f"📋 Template location: {get_template_path()}")
        print(f"✅ Template exists: {get_template_path().exists()}")
        print(f"📁 .pypirc exists: {check_existing_pypirc()}")
        print("\n🔗 Token generation URLs:")
        print("   PyPI: https://pypi.org/manage/account/#api-tokens")
        print("   TestPyPI: https://test.pypi.org/manage/account/#api-tokens")
        return
    
    print("🔧 Configuring PyPI Authentication")
    print("=" * 40)
    
    # Check if .pypirc already exists
    if check_existing_pypirc() and not args.force:
        print(f"❌ .pypirc already exists at: {get_pypirc_path()}")
        print("   Use --force to overwrite or edit the file manually")
        print("   Use --show-info to see current configuration")
        return
    
    # Backup existing file if it exists
    if check_existing_pypirc():
        print("📄 Existing .pypirc file detected...")
        if not backup_existing_pypirc():
            print("❌ Failed to backup existing file. Aborting.")
            return
    
    # Create .pypirc from template
    print("📋 Creating .pypirc from template...")
    success = create_pypirc_from_template(
        pypi_token=args.pypi_token,
        testpypi_token=args.testpypi_token
    )
    
    if success:
        print(f"✅ Successfully created .pypirc at: {get_pypirc_path()}")
        
        # Check if tokens were provided
        if not args.pypi_token or not args.testpypi_token:
            print("\n⚠️  NEXT STEPS:")
            print("1. Edit the .pypirc file and replace the token placeholders:")
            if not args.pypi_token:
                print("   - Replace 'YOUR_PYPI_TOKEN_HERE' with your PyPI token")
            if not args.testpypi_token:
                print("   - Replace 'YOUR_TESTPYPI_TOKEN_HERE' with your "
                      "TestPyPI token")
            print("2. Get tokens from:")
            print("   - PyPI: https://pypi.org/manage/account/#api-tokens")
            print("   - TestPyPI: https://test.pypi.org/manage/account/#api-tokens")
        
        print("\n📦 Upload commands:")
        print("   Test upload: twine upload --repository testpypi dist/*")
        print("   Production:  twine upload --repository pypi dist/*")
        
    else:
        print("❌ Failed to create .pypirc file")


if __name__ == "__main__":
    main()
