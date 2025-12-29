# Test Reporting Guide
## Beautiful TestNG/JaCoCo-Style Reports for Python Behave Tests

This guide explains how to run tests and generate professional HTML reports using Allure Framework (Python equivalent of TestNG reports).

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Running Tests with Reports](#running-tests-with-reports)
4. [Report Features](#report-features)
5. [Manual Commands](#manual-commands)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Option 1: Using Batch Files (Windows - Easiest)

**Run Smoke Tests:**
```bash
run_smoke_tests.bat
```

**Run All Tests:**
```bash
run_all_tests.bat
```

### Option 2: Using Python Scripts

**Run Smoke Tests:**
```bash
source venv/Scripts/activate  # Windows
py run_smoke_tests_with_report.py
```

**Run All Tests:**
```bash
source venv/Scripts/activate  # Windows
py run_all_tests_with_report.py
```

---

## Installation

### Step 1: Install Python Dependencies (Already Done)

The required Python packages are already in `requirements.txt`:
```bash
source venv/Scripts/activate
pip install -r requirements.txt
```

This includes:
- `allure-behave` - Allure formatter for Behave
- `behave` - BDD test framework
- `selenium` - Browser automation

### Step 2: Install Allure CLI (Required for Report Generation)

Allure CLI is needed to generate and view the HTML reports.

#### Windows (Scoop - Recommended)
```bash
# Install Scoop if you don't have it
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install Allure
scoop install allure
```

#### Windows (Chocolatey)
```bash
choco install allure
```

#### macOS
```bash
brew install allure
```

#### Linux (Manual)
```bash
# Download from GitHub
wget https://github.com/allure-framework/allure2/releases/latest/download/allure-2.x.x.zip
unzip allure-2.x.x.zip
sudo mv allure-2.x.x /opt/allure
echo 'export PATH="/opt/allure/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Verify Installation
```bash
allure --version
```

You should see something like: `2.24.0` or similar

---

## Running Tests with Reports

### 1. Run Smoke Tests with Report

**Method A: Batch File (Windows)**
```bash
run_smoke_tests.bat
```

**Method B: Python Script**
```bash
source venv/Scripts/activate
py run_smoke_tests_with_report.py
```

**Method C: Direct Command**
```bash
source venv/Scripts/activate
behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results -f pretty
allure serve reports/allure-results
```

### 2. Run Complete Test Suite with Report

**Method A: Batch File (Windows)**
```bash
run_all_tests.bat
```

**Method B: Python Script**
```bash
source venv/Scripts/activate
py run_all_tests_with_report.py
```

**Method C: Direct Command**
```bash
source venv/Scripts/activate
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results -f pretty
allure serve reports/allure-results
```

### 3. Run Specific Feature

```bash
source venv/Scripts/activate
behave features/smoke.feature -f allure_behave.formatter:AllureFormatter -o reports/allure-results
allure serve reports/allure-results
```

### 4. Run Tests with Specific Tags

```bash
source venv/Scripts/activate
behave --tags=@critical -f allure_behave.formatter:AllureFormatter -o reports/allure-results
allure serve reports/allure-results
```

---

## Report Features

### What You Get with Allure Reports

Allure provides comprehensive test reporting similar to TestNG with:

1. **Overview Dashboard**
   - Total tests, passed, failed, broken, skipped
   - Success rate percentage
   - Execution time
   - Historical trends (if running multiple times)

2. **Detailed Test Results**
   - Step-by-step execution details
   - Execution time per test
   - Error messages and stack traces
   - Screenshots on failures (automatically attached)
   - Logs and attachments

3. **Categorization**
   - Tests grouped by features
   - Tests grouped by severity
   - Tests grouped by tags
   - Failed tests categorized by error type

4. **Timeline View**
   - Visual timeline of test execution
   - Parallel execution visualization
   - Duration analysis

5. **Graphs and Charts**
   - Success rate trends
   - Test duration trends
   - Test result distribution
   - Test severity distribution

6. **Behaviors (BDD View)**
   - Tests organized by user stories
   - Feature -> Scenario hierarchy
   - Gherkin syntax preserved

7. **Test Suites**
   - All test suites listed
   - Filter by status
   - Search functionality

---

## Manual Commands Reference

### Generate Results Only (No Report)

```bash
source venv/Scripts/activate
behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

### Generate HTML Report from Results

```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

### Open Generated Report

```bash
allure open reports/allure-report
```

### Serve Report (Generate + Open)

```bash
allure serve reports/allure-results
```
This is the recommended way - it generates and opens the report in one command.

### Generate JSON Report (Alternative)

```bash
behave --tags=@smoke -f json -o reports/test-results.json
```

### Generate JUnit XML Report

```bash
behave --tags=@smoke --junit --junit-directory reports
```

---

## Report Customization

### Add Custom Properties to Report

Edit `features/environment.py` to add custom properties:

```python
def before_all(context):
    # Add environment info to Allure report
    context.config.userdata.setdefault('env.Browser', 'Chrome')
    context.config.userdata.setdefault('env.Environment', 'Production')
    context.config.userdata.setdefault('env.URL', 'https://www.faberwork.com')
```

### Add Severity to Tests

Add severity decorator in feature files:

```gherkin
@smoke @critical @severity.critical
Scenario: Homepage loads successfully
```

### Add Links to Tests

Add issue or test management links:

```gherkin
@smoke @issue.JIRA-123 @tms.TestRail-456
Scenario: Contact form submission
```

---

## Directory Structure

After running tests with reports:

```
project/
├── reports/
│   ├── allure-results/      # Raw test results (JSON files)
│   │   ├── *.json           # Test result files
│   │   └── *.png            # Screenshots
│   └── allure-report/       # Generated HTML report
│       └── index.html       # Open this in browser
├── run_smoke_tests_with_report.py
├── run_all_tests_with_report.py
├── run_smoke_tests.bat
└── run_all_tests.bat
```

---

## Troubleshooting

### Issue: "allure: command not found"

**Problem:** Allure CLI is not installed or not in PATH

**Solution:**
1. Install Allure CLI (see Installation section above)
2. Verify with: `allure --version`
3. Add to PATH if needed

**Workaround:** Use `allure serve` which requires less configuration:
```bash
allure serve reports/allure-results
```

### Issue: "No test results found"

**Problem:** Tests didn't execute or results directory is empty

**Solution:**
1. Check if behave ran successfully
2. Verify allure-behave is installed: `pip list | grep allure`
3. Check reports/allure-results directory has JSON files

### Issue: "Module 'allure_behave' not found"

**Problem:** allure-behave package not installed

**Solution:**
```bash
source venv/Scripts/activate
pip install allure-behave
```

### Issue: Port already in use (for allure serve)

**Problem:** Previous Allure server still running

**Solution:**
1. Press Ctrl+C to stop previous server
2. Kill process on port: `taskkill /F /IM java.exe` (Windows)
3. Try a different port: `allure serve -p 8081 reports/allure-results`

### Issue: Report shows no screenshots

**Problem:** Screenshots not being attached to Allure report

**Solution:**
Verify `features/environment.py` has screenshot capture enabled:
```python
def after_scenario(context, scenario):
    if scenario.status == 'failed':
        screenshot_path = f"screenshots/{scenario.name}.png"
        context.driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, attachment_type=allure.attachment_type.PNG)
```

### Issue: Tests run but report is empty

**Problem:** Allure formatter not properly configured

**Solution:**
Ensure you're using the correct formatter:
```bash
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

---

## Advanced Usage

### Running Tests in Parallel (Future Enhancement)

```bash
# Install behave-parallel
pip install behave-parallel

# Run tests in parallel
behave --parallel --processes 4 -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

### Historical Trends

To see historical trends in Allure reports:

1. Don't use `--clean` flag when generating reports
2. Keep previous results:
```bash
allure generate reports/allure-results -o reports/allure-report
```

3. Run tests multiple times and trends will accumulate

### CI/CD Integration

For CI/CD pipelines (GitHub Actions, Jenkins, etc.):

```yaml
# Example GitHub Actions
- name: Run Tests
  run: |
    source venv/Scripts/activate
    behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results

- name: Generate Report
  run: allure generate reports/allure-results -o reports/allure-report --clean

- name: Publish Report
  uses: actions/upload-artifact@v2
  with:
    name: allure-report
    path: reports/allure-report
```

---

## Comparison: Allure vs Other Reporters

| Feature | Allure | Behave JSON | JUnit XML | HTML (pytest-html) |
|---------|--------|-------------|-----------|-------------------|
| Visual Appeal | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| Charts/Graphs | ✓ | ✗ | ✗ | Limited |
| Screenshots | ✓ | ✗ | ✗ | ✓ |
| Historical Trends | ✓ | ✗ | ✗ | ✗ |
| BDD Support | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| Step Details | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| CI Integration | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Setup Complexity | Medium | Easy | Easy | Easy |

**Recommendation:** Use Allure for comprehensive reporting (equivalent to TestNG). It provides the best visual reports and detailed analysis.

---

## Quick Command Reference

```bash
# Smoke tests with report
run_smoke_tests.bat

# All tests with report
run_all_tests.bat

# Smoke tests (manual)
behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results && allure serve reports/allure-results

# All tests (manual)
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results && allure serve reports/allure-results

# Generate static report
allure generate reports/allure-results -o reports/allure-report --clean

# Open existing report
allure open reports/allure-report

# View results instantly (no static generation)
allure serve reports/allure-results
```

---

## Support

For issues or questions:
1. Check this guide first
2. Review Allure documentation: https://docs.qameta.io/allure/
3. Check Behave documentation: https://behave.readthedocs.io/

---

**Last Updated:** December 29, 2025
**Version:** 1.0
