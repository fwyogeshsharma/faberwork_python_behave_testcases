# Quick Start: Test Reporting

## TL;DR - Just Run Tests with Reports

### Option 1: Double-Click (Windows - Easiest!)

1. **Smoke Tests:** Double-click `run_smoke_tests.bat`
2. **All Tests:** Double-click `run_all_tests.bat`

That's it! The script will:
- ✓ Run the tests
- ✓ Generate results
- ✓ Open the report in your browser automatically

---

### Option 2: Command Line (All Platforms)

**Smoke Tests:**
```bash
# Windows
source venv/Scripts/activate
py run_smoke_tests_with_report.py

# Linux/Mac
source venv/bin/activate
python3 run_smoke_tests_with_report.py
```

**All Tests:**
```bash
# Windows
source venv/Scripts/activate
py run_all_tests_with_report.py

# Linux/Mac
source venv/bin/activate
python3 run_all_tests_with_report.py
```

---

## Prerequisites

### 1. Python Dependencies (One-time setup)

```bash
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

This installs `allure-behave` and other required packages.

### 2. Allure CLI (One-time setup)

**Windows - Using Scoop (Recommended):**
```bash
# Install Scoop (if not installed)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install Allure
scoop install allure
```

**Windows - Using Chocolatey:**
```bash
choco install allure
```

**macOS:**
```bash
brew install allure
```

**Verify Installation:**
```bash
allure --version
```

---

## What You Get

### Allure Report Features

Your test reports will include:

✅ **Dashboard Overview**
- Total tests: Passed, Failed, Broken, Skipped
- Success rate percentage
- Execution duration
- Historical trends

✅ **Detailed Test Results**
- Step-by-step execution
- Screenshots on failures (automatically attached)
- Error messages and stack traces
- Execution time per test

✅ **Visual Charts**
- Test status distribution (pie chart)
- Severity distribution
- Duration trends
- Success rate trends

✅ **BDD View**
- Features and scenarios organized hierarchically
- Gherkin syntax preserved
- Tags visible

✅ **Timeline View**
- Visual execution timeline
- Test duration analysis

✅ **Categorization**
- By feature
- By severity
- By tag
- By status

---

## Manual Commands (If You Prefer)

### Run Smoke Tests Only

```bash
source venv/Scripts/activate

# Generate results
behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# View report (opens browser automatically)
allure serve reports/allure-results
```

### Run All Tests

```bash
source venv/Scripts/activate

# Generate results
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# View report
allure serve reports/allure-results
```

### Run Specific Feature

```bash
source venv/Scripts/activate

# Run specific feature file
behave features/smoke.feature -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# View report
allure serve reports/allure-results
```

### Run Tests with Specific Tags

```bash
source venv/Scripts/activate

# Run tests with @critical tag
behave --tags=@critical -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# View report
allure serve reports/allure-results
```

---

## Report Location

After running tests:

- **Results (JSON):** `reports/allure-results/`
- **HTML Report:** `reports/allure-report/` (if generated statically)
- **Screenshots:** `screenshots/` (also embedded in report)

---

## Viewing Reports

### Method 1: Serve Report (Recommended)

```bash
allure serve reports/allure-results
```

This will:
1. Generate the report
2. Start a local web server
3. Open your browser automatically
4. Press Ctrl+C to stop when done

### Method 2: Generate Static Report

```bash
# Generate
allure generate reports/allure-results -o reports/allure-report --clean

# Open
allure open reports/allure-report
```

### Method 3: Open HTML Directly

After generating static report, open manually:
```
reports/allure-report/index.html
```

---

## Troubleshooting

### "allure: command not found"

**Solution:** Install Allure CLI (see Prerequisites above)

### "format=allure_behave.formatter:AllureFormatter is unknown"

**Solution:**
```bash
source venv/Scripts/activate
pip install allure-behave
```

### Tests run but no report shows

**Solution:** Check if results were generated:
```bash
ls reports/allure-results/
```

You should see multiple `.json` files. If not, the formatter didn't run properly.

### Port already in use

**Solution:**
```bash
# Kill existing Allure server
# Windows:
taskkill /F /IM java.exe

# Linux/Mac:
killall java
```

---

## Complete Example

Here's a complete workflow:

```bash
# 1. Activate virtual environment
source venv/Scripts/activate

# 2. Run smoke tests with Allure reporting
behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# 3. View the report (opens browser)
allure serve reports/allure-results

# 4. When done viewing, press Ctrl+C to stop the server
```

---

## Need More Help?

See the comprehensive guide: **[REPORTING_GUIDE.md](REPORTING_GUIDE.md)**

---

**Quick Reference Card:**

| Task | Command |
|------|---------|
| Smoke tests | `run_smoke_tests.bat` |
| All tests | `run_all_tests.bat` |
| View results | `allure serve reports/allure-results` |
| Generate static | `allure generate reports/allure-results -o reports/allure-report --clean` |
| Open static | `allure open reports/allure-report` |

---

**Last Updated:** December 29, 2025
