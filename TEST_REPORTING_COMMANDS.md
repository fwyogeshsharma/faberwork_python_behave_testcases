# Test Reporting Commands - Quick Reference

## Complete Setup and Execution Guide

### Prerequisites (One-Time Setup)

1. **Install Python Dependencies:**
```bash
source venv/Scripts/activate
pip install allure-behave
```

2. **Install Allure CLI (for viewing reports):**

**Windows (Scoop - Recommended):**
```bash
scoop install allure
```

**Windows (Chocolatey):**
```bash
choco install allure
```

**Verify:**
```bash
allure --version
```

---

## Running Tests with Allure Reports

### Method 1: Easy Batch Files (Windows)

**Smoke Tests:**
```bash
run_smoke_tests.bat
```

**All Tests:**
```bash
run_all_tests.bat
```

### Method 2: Python Scripts

**Smoke Tests:**
```bash
source venv/Scripts/activate
py run_smoke_tests_with_report.py
```

**All Tests:**
```bash
source venv/Scripts/activate
py run_all_tests_with_report.py
```

### Method 3: Direct Commands

**Smoke Tests:**
```bash
source venv/Scripts/activate

# Run tests and generate Allure results
behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# View report (opens browser automatically)
allure serve reports/allure-results
```

**All Tests:**
```bash
source venv/Scripts/activate

# Run tests and generate Allure results
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# View report
allure serve reports/allure-results
```

---

## Complete Command Reference

### 1. Run Smoke Tests with Allure

```bash
source venv/Scripts/activate
behave --tags=@smoke \
  -f allure_behave.formatter:AllureFormatter \
  -o reports/allure-results \
  --no-capture
```

### 2. Run All Tests with Allure

```bash
source venv/Scripts/activate
behave \
  -f allure_behave.formatter:AllureFormatter \
  -o reports/allure-results \
  --no-capture
```

### 3. View Allure Report (Serve - Recommended)

```bash
allure serve reports/allure-results
```

This will:
- Generate the HTML report
- Start a web server
- Open your browser automatically
- Press Ctrl+C to stop

### 4. Generate Static HTML Report

```bash
allure generate reports/allure-results \
  -o reports/allure-report \
  --clean
```

### 5. Open Static Report

```bash
allure open reports/allure-report
```

### 6. Run Tests with Multiple Formatters

```bash
source venv/Scripts/activate
behave --tags=@smoke \
  -f allure_behave.formatter:AllureFormatter \
  -o reports/allure-results \
  -f pretty
```

---

## Alternative Reporting Formats

### JSON Report

```bash
source venv/Scripts/activate
behave --tags=@smoke -f json -o reports/smoke-results.json
```

### JUnit XML Report

```bash
source venv/Scripts/activate
behave --tags=@smoke --junit --junit-directory reports
```

### Pretty Console Output (No Report)

```bash
source venv/Scripts/activate
behave --tags=@smoke -f pretty
```

---

## Tag-Based Test Execution

### Run by Severity

```bash
# Critical tests
behave --tags=@critical -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# High priority tests
behave --tags=@high -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

### Run by Feature

```bash
# Smoke tests
behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Form tests
behave --tags=@form -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Navigation tests
behave --tags=@navigation -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

### Run by Page

```bash
# Homepage tests
behave --tags=@homepage -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Contact page tests
behave --tags=@contact -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

### Combine Tags

```bash
# Smoke AND critical
behave --tags=@smoke --tags=@critical -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Form OR contact
behave --tags=@form,@contact -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

---

## CI/CD Integration Commands

### GitHub Actions Example

```bash
# Run tests
behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Generate static report
allure generate reports/allure-results -o reports/allure-report --clean

# Upload artifact (GitHub Actions specific)
# Report will be in: reports/allure-report
```

### Jenkins Example

```bash
# Run tests
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Jenkins Allure Plugin will automatically pick up results from:
# reports/allure-results/
```

---

## Cleanup Commands

### Clean All Reports

```bash
# Windows
rmdir /S /Q reports\allure-results
rmdir /S /Q reports\allure-report

# Linux/Mac
rm -rf reports/allure-results
rm -rf reports/allure-report
```

### Clean Screenshots

```bash
# Windows
del /Q screenshots\*.png

# Linux/Mac
rm -f screenshots/*.png
```

---

## Troubleshooting Commands

### Check Allure Installation

```bash
allure --version
```

### Check allure-behave Installation

```bash
source venv/Scripts/activate
pip show allure-behave
```

### Reinstall allure-behave

```bash
source venv/Scripts/activate
pip uninstall allure-behave
pip install allure-behave
```

### List Generated Results

```bash
# Windows
dir reports\allure-results

# Linux/Mac
ls -la reports/allure-results/
```

### Check if Tests Ran

```bash
# Should show multiple *.json files and *.png files
ls reports/allure-results/*.json
ls reports/allure-results/*.png
```

---

## Advanced Commands

### Run with Custom Allure Properties

```bash
behave --tags=@smoke \
  -f allure_behave.formatter:AllureFormatter \
  -o reports/allure-results \
  -D env.Browser=Chrome \
  -D env.Environment=Production \
  -D env.URL=https://www.faberwork.com
```

### Run Tests in Parallel (Requires behave-parallel)

```bash
pip install behave-parallel

behave-parallel \
  --tags=@smoke \
  --processes 4 \
  -f allure_behave.formatter:AllureFormatter \
  -o reports/allure-results
```

### Generate Report with Historical Data

```bash
# Don't use --clean to keep history
allure generate reports/allure-results -o reports/allure-report

# Run tests multiple times to see trends
```

---

## Complete Workflow Example

```bash
# Step 1: Activate environment
source venv/Scripts/activate

# Step 2: Clean previous results (optional)
rm -rf reports/allure-results/*

# Step 3: Run smoke tests
behave --tags=@smoke \
  -f allure_behave.formatter:AllureFormatter \
  -o reports/allure-results \
  --no-capture

# Step 4: View report
allure serve reports/allure-results

# Step 5: When done viewing, press Ctrl+C
```

---

## Files Created for You

- `run_smoke_tests_with_report.py` - Python script for smoke tests
- `run_all_tests_with_report.py` - Python script for all tests
- `run_smoke_tests.bat` - Windows batch file for smoke tests
- `run_all_tests.bat` - Windows batch file for all tests
- `REPORTING_GUIDE.md` - Comprehensive reporting guide
- `QUICK_START_REPORTING.md` - Quick start guide
- `TEST_REPORTING_COMMANDS.md` - This file

---

## What You Get in Allure Report

✅ **Dashboard**
- Total tests, passed, failed, broken, skipped
- Success rate percentage
- Execution time
- Historical trends

✅ **Test Results**
- Step-by-step execution details
- Screenshots on failures (automatic)
- Error messages and stack traces
- Execution time per test

✅ **Graphs**
- Test status distribution (pie chart)
- Severity distribution
- Duration trends
- Success rate over time

✅ **BDD View**
- Features and scenarios organized
- Gherkin syntax preserved
- Tags visible

✅ **Timeline**
- Visual execution timeline
- Test duration analysis

---

## Report Locations

After running tests:

```
project/
├── reports/
│   ├── allure-results/        # Raw JSON results
│   │   ├── *-result.json      # Test results
│   │   └── *-attachment.png   # Screenshots
│   └── allure-report/         # Generated HTML
│       └── index.html         # Main report page
├── screenshots/               # Failure screenshots
└── logs/                      # Execution logs
```

---

## Quick Command Cheat Sheet

| Task | Command |
|------|---------|
| Run smoke tests | `behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results` |
| Run all tests | `behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results` |
| View report (serve) | `allure serve reports/allure-results` |
| Generate static | `allure generate reports/allure-results -o reports/allure-report --clean` |
| Open static | `allure open reports/allure-report` |
| Clean results | `rm -rf reports/allure-results/*` |
| Check Allure CLI | `allure --version` |
| Check package | `pip show allure-behave` |

---

**Last Updated:** December 29, 2025
**Version:** 1.0
