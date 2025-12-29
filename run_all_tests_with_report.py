#!/usr/bin/env python3
"""
Complete Test Suite Runner with Allure Report Generation
Run all tests and generate beautiful HTML reports
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Project directories
PROJECT_ROOT = Path(__file__).parent
ALLURE_RESULTS_DIR = PROJECT_ROOT / "reports" / "allure-results"
ALLURE_REPORT_DIR = PROJECT_ROOT / "reports" / "allure-report"


def print_banner(message):
    """Print a formatted banner"""
    width = 80
    print("\n" + "=" * width)
    print(f"  {message}")
    print("=" * width + "\n")


def clean_previous_results():
    """Clean previous Allure results"""
    print_banner("Cleaning Previous Results")

    if ALLURE_RESULTS_DIR.exists():
        shutil.rmtree(ALLURE_RESULTS_DIR)
        print(f"✓ Removed old results: {ALLURE_RESULTS_DIR}")

    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created results directory: {ALLURE_RESULTS_DIR}")


def run_all_tests():
    """Run complete test suite with Allure formatter"""
    print_banner("Running Complete Test Suite")

    # Behave command with Allure formatter
    cmd = [
        "behave",
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", str(ALLURE_RESULTS_DIR),
        "-f", "pretty",  # Also show pretty output in console
        "--no-capture",
        "--no-skipped"  # Don't show skipped tests in output
    ]

    print(f"Command: {' '.join(cmd)}\n")

    # Run tests
    start_time = datetime.now()
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\n✓ Test execution completed in {duration}")
    print(f"✓ Results saved to: {ALLURE_RESULTS_DIR}")

    return result.returncode


def generate_allure_report():
    """Generate Allure HTML report"""
    print_banner("Generating Allure Report")

    # Check if Allure is installed
    try:
        subprocess.run(["allure", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ERROR: Allure CLI is not installed!")
        print("\nTo install Allure CLI:")
        print("  Windows (using Scoop):")
        print("    scoop install allure")
        print("\n  Windows (using Chocolatey):")
        print("    choco install allure")
        print("\n  macOS:")
        print("    brew install allure")
        print("\n  Linux:")
        print("    Download from: https://github.com/allure-framework/allure2/releases")
        print("\nAlternatively, view results online using:")
        print("  allure serve reports/allure-results")
        return False

    # Generate report
    if ALLURE_REPORT_DIR.exists():
        shutil.rmtree(ALLURE_REPORT_DIR)

    cmd = [
        "allure",
        "generate",
        str(ALLURE_RESULTS_DIR),
        "-o", str(ALLURE_REPORT_DIR),
        "--clean"
    ]

    print(f"Command: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)

    if result.returncode == 0:
        print(f"\n✓ Report generated successfully!")
        print(f"✓ Report location: {ALLURE_REPORT_DIR}")
        return True
    else:
        print("\n❌ Failed to generate report")
        return False


def open_report():
    """Open the generated report in browser"""
    print_banner("Opening Report")

    cmd = ["allure", "open", str(ALLURE_REPORT_DIR)]

    print(f"Command: {' '.join(cmd)}\n")
    print("Opening report in your default browser...")
    print("Press Ctrl+C to stop the server when done.\n")

    try:
        subprocess.run(cmd, cwd=PROJECT_ROOT)
    except KeyboardInterrupt:
        print("\n\n✓ Report server stopped")


def serve_report():
    """Serve the Allure report (alternative to generate + open)"""
    print_banner("Serving Allure Report")

    cmd = ["allure", "serve", str(ALLURE_RESULTS_DIR)]

    print(f"Command: {' '.join(cmd)}\n")
    print("Starting Allure report server...")
    print("Report will open in your browser automatically.")
    print("Press Ctrl+C to stop the server when done.\n")

    try:
        subprocess.run(cmd, cwd=PROJECT_ROOT)
    except KeyboardInterrupt:
        print("\n\n✓ Report server stopped")


def main():
    """Main execution flow"""
    print_banner("Complete Test Suite Execution with Allure Reporting")

    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Results Directory: {ALLURE_RESULTS_DIR}")
    print(f"Report Directory: {ALLURE_REPORT_DIR}\n")

    # Step 1: Clean previous results
    clean_previous_results()

    # Step 2: Run all tests
    test_result = run_all_tests()

    # Step 3: Check if we have results
    if not ALLURE_RESULTS_DIR.exists() or not list(ALLURE_RESULTS_DIR.glob("*.json")):
        print("\n❌ ERROR: No test results found!")
        print("Make sure behave executed successfully and allure-behave is installed.")
        sys.exit(1)

    # Step 4: Generate and serve report
    print("\n" + "=" * 80)
    print("  Report Options")
    print("=" * 80)
    print("\n1. Generate static report and open in browser (requires Allure CLI)")
    print("2. Serve report with built-in server (recommended - requires Allure CLI)")
    print("3. Skip report generation (results saved, generate later)")

    choice = input("\nSelect option (1/2/3) [default: 2]: ").strip() or "2"

    if choice == "1":
        if generate_allure_report():
            open_report()
    elif choice == "2":
        serve_report()
    else:
        print("\n✓ Test results saved. Generate report later using:")
        print(f"  allure serve {ALLURE_RESULTS_DIR}")
        print(f"  or")
        print(f"  allure generate {ALLURE_RESULTS_DIR} -o {ALLURE_REPORT_DIR} --clean")

    # Final summary
    print_banner("Execution Summary")
    print(f"Test Exit Code: {test_result}")
    print(f"Results Location: {ALLURE_RESULTS_DIR}")
    print(f"Report Location: {ALLURE_REPORT_DIR}")

    if test_result == 0:
        print("\n✓ All tests PASSED!")
    else:
        print("\n⚠ Some tests FAILED - check the report for details")

    sys.exit(test_result)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
