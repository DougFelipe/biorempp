#!/usr/bin/env python3
"""
Manual CLI Verification for BioRemPP.
"""

import subprocess
import sys


def test_command(cmd_args, description):
    """Test a single command."""
    print(f"\n{'='*50}")
    print(f"Testing: {description}")
    print(f"Command: python -m biorempp {' '.join(cmd_args)}")
    print(f"{'='*50}")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "biorempp"] + cmd_args, text=True, timeout=30
        )
        print(f"Return code: {result.returncode}")
        if result.returncode == 0:
            print("✅ Command executed successfully")
        else:
            print("❌ Command failed")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run manual verification."""
    print("🧪 BioRemPP CLI Manual Verification")
    print("This will execute each command and show the results")

    commands = [
        (["--help"], "Help command"),
        (["--list-databases"], "List all databases"),
        (["--database-info", "biorempp"], "BioRemPP database info"),
        (["--database-info", "toxcsm"], "ToxCSM database info"),
    ]

    results = []
    for cmd_args, description in commands:
        success = test_command(cmd_args, description)
        results.append((description, success))

    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")

    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description}: {status}")

    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} commands successful")

    if passed == total:
        print("\n🎉 All commands working perfectly!")
    elif passed >= total // 2:
        print("\n👍 Most commands working!")
    else:
        print("\n⚠️ Several commands having issues!")


if __name__ == "__main__":
    main()
