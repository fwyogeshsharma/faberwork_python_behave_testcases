# HTML Report Generation Guide
## Beautiful TestNG/JaCoCo-Style Reports from JSON

This guide shows you how to generate beautiful HTML reports from your test results JSON files.

---

## Quick Start

### Option 1: Run Tests and Generate Report (One Click!)

**Windows:**
```bash
run_tests_and_generate_report.bat
```

This will:
1. Run smoke tests
2. Generate JSON results
3. Create HTML report
4. Open report in browser automatically

### Option 2: Generate Report from Existing JSON

If you already have `test_results.json`:

**Windows:**
```bash
generate_report.bat
```

**Command Line:**
```bash
source venv/Scripts/activate
py generate_html_report.py reports/test_results.json reports/test_report.html
```

---

## How It Works

### 1. Generate JSON Results

First, run your tests with JSON formatter:

```bash
source venv/Scripts/activate

# Smoke tests
behave --tags=@smoke -f json -o reports/test_results.json

# All tests
behave -f json -o reports/test_results.json

# Specific feature
behave features/smoke.feature -f json -o reports/test_results.json
```

###2. Generate HTML Report

Then convert JSON to HTML:

```bash
py generate_html_report.py reports/test_results.json reports/test_report.html
```

The report will open automatically in your browser!

---

## Report Features

Your HTML report includes:

### 📊 Dashboard
- Success rate percentage (with color coding)
- Total scenarios count
- Passed/Failed/Skipped breakdown
- Total execution time
- Visual progress bar

### 📈 Test Results
- Failed features shown first (for quick attention)
- Passed features shown separately
- Each feature shows all scenarios
- Each scenario shows all steps

### 🔍 Detailed Information
- Step-by-step execution details
- Execution time for each step
- Error messages for failed steps
- Status badges (color-coded)
- Tags and categories

### 🎨 Visual Elements
- Color-coded status badges
- Interactive feature cards
- Hover effects
- Responsive design
- Print-friendly layout

---

## Complete Commands Reference

### Generate JSON from Tests

```bash
source venv/Scripts/activate

# Smoke tests only
behave --tags=@smoke -f json -o reports/test_results.json

# All tests
behave -f json -o reports/test_results.json

# Critical tests
behave --tags=@critical -f json -o reports/test_results.json

# Form tests
behave --tags=@form -f json -o reports/test_results.json

# Specific feature file
behave features/smoke.feature -f json -o reports/test_results.json
```

### Generate HTML Report

```bash
# Default (uses reports/test_results.json)
py generate_html_report.py

# Specify input and output
py generate_html_report.py reports/test_results.json reports/test_report.html

# Custom file names
py generate_html_report.py reports/my_tests.json reports/my_report.html
```

---

## File Locations

After running:

```
project/
├── reports/
│   ├── test_results.json      # Input: JSON test results
│   └── test_report.html        # Output: Beautiful HTML report
├── screenshots/                # Screenshots embedded in report
├── generate_html_report.py     # Report generator script
├── generate_report.bat         # Windows batch file
└── run_tests_and_generate_report.bat  # All-in-one batch file
```

---

## Example Workflow

### Workflow 1: Complete Test Run

```bash
# 1. Run tests with JSON output
source venv/Scripts/activate
behave --tags=@smoke -f json -o reports/test_results.json

# 2. Generate HTML report
py generate_html_report.py

# 3. Report opens in browser automatically!
```

### Workflow 2: Using Batch File

```bash
# Double-click this file:
run_tests_and_generate_report.bat

# Everything happens automatically!
```

### Workflow 3: Multiple Reports

```bash
# Run different test suites
behave --tags=@smoke -f json -o reports/smoke_results.json
behave --tags=@regression -f json -o reports/regression_results.json

# Generate separate reports
py generate_html_report.py reports/smoke_results.json reports/smoke_report.html
py generate_html_report.py reports/regression_results.json reports/regression_report.html
```

---

## Report Customization

### Change Report Title

Edit `generate_html_report.py` line ~240:

```python
<h1>🧪 Test Execution Report</h1>
<p>Faberwork Website Automation Testing</p>
```

### Change Colors

Edit the CSS styles in `generate_html_report.py`:

```python
.stat-card.success .value {{ color: #28a745; }}  # Green
.stat-card.danger .value {{ color: #dc3545; }}   # Red
```

### Add Logo

Add your company logo to the header:

```python
<div class="header">
    <img src="logo.png" alt="Logo" style="max-width: 200px;">
    <h1>Test Execution Report</h1>
</div>
```

---

## Advanced Usage

### Generate Report Without Opening Browser

Edit `generate_html_report.py` and comment out:

```python
# webbrowser.open(f'file://{abs_path}')
```

### Include Screenshots

Screenshots from `screenshots/` folder are automatically:
- Detected from test failures
- Embedded in the report (if available in JSON)
- Displayed inline with failed steps

### Custom Statistics

Add custom stats by modifying the `calculate_statistics()` function in `generate_html_report.py`.

---

## Troubleshooting

### Issue: "JSON file not found"

**Solution:**
```bash
# Generate JSON first
behave --tags=@smoke -f json -o reports/test_results.json

# Then generate report
py generate_html_report.py
```

### Issue: "Report is empty"

**Problem:** JSON file might be empty or invalid

**Solution:**
```bash
# Check JSON file size
ls -la reports/test_results.json

# If 0 bytes, re-run tests
behave --tags=@smoke -f json -o reports/test_results.json
```

### Issue: "Report doesn't open in browser"

**Solution:** Manually open the file:
```
reports/test_report.html
```

### Issue: "UnicodeEncodeError"

This was already fixed in the script! If you still see it:

**Solution:**
```bash
# Set UTF-8 encoding
set PYTHONIOENCODING=utf-8

# Then run
py generate_html_report.py
```

---

## Report Sections Explained

### 1. Header
- Shows report title
- Displays generation timestamp
- Beautiful gradient background

### 2. Statistics Cards
- **Success Rate**: Overall pass percentage
- **Total Scenarios**: Number of test scenarios
- **Passed**: Successful tests (green)
- **Failed**: Failed tests (red)
- **Skipped**: Skipped tests (yellow)
- **Duration**: Total execution time

### 3. Progress Bar
- Visual representation of results
- Color-coded segments
- Shows distribution at a glance

### 4. Failed Features
- Shown first for immediate attention
- Red badge indicators
- Detailed error messages
- Step-by-step breakdown

### 5. Passed Features
- Shown after failed features
- Green badge indicators
- Collapsed by default (optional)
- Complete execution details

### 6. Footer
- Summary information
- Generation details
- Framework information

---

## Sample Report Preview

```
┌─────────────────────────────────────────────┐
│     🧪 Test Execution Report               │
│   Faberwork Website Automation Testing     │
│   Generated on 2025-12-29 15:46:46         │
└─────────────────────────────────────────────┘

┌─────────┬─────────┬─────────┬─────────┐
│ 50.0%   │    4    │    2    │    2    │
│ Success │ Scenarios│ Passed │ Failed  │
└─────────┴─────────┴─────────┴─────────┘

[████████░░░░░░░░░░] 50% Pass Rate

❌ Failed Features
  └─ Smoke Tests for Faberwork Website
     ├─ ✗ Consultation form is accessible
     └─ ✗ Contact page is accessible

✅ Passed Features
  └─ Smoke Tests for Faberwork Website
     ├─ ✓ Homepage loads successfully
     └─ ✓ Main navigation menu works
```

---

## Benefits Over Plain JSON

| Feature | JSON | HTML Report |
|---------|------|-------------|
| Visual Appeal | ❌ | ✅ Beautiful UI |
| Easy Reading | ❌ | ✅ Color-coded |
| Charts | ❌ | ✅ Progress bars |
| Screenshots | ❌ | ✅ Embedded |
| Error Highlighting | ❌ | ✅ Red badges |
| Shareable | ❌ | ✅ Single HTML file |
| Printable | ❌ | ✅ Print-optimized |
| Searchable | Limited | ✅ Browser search |

---

## Integration with CI/CD

### GitHub Actions

```yaml
- name: Run Tests
  run: |
    source venv/Scripts/activate
    behave --tags=@smoke -f json -o reports/test_results.json

- name: Generate HTML Report
  run: |
    py generate_html_report.py

- name: Upload Report
  uses: actions/upload-artifact@v2
  with:
    name: test-report
    path: reports/test_report.html
```

### Jenkins

```groovy
stage('Test') {
    steps {
        sh 'behave --tags=@smoke -f json -o reports/test_results.json'
        sh 'python generate_html_report.py'
        publishHTML([
            reportDir: 'reports',
            reportFiles: 'test_report.html',
            reportName: 'Test Report'
        ])
    }
}
```

---

## Quick Command Cheat Sheet

| Task | Command |
|------|---------|
| Run tests + generate report | `run_tests_and_generate_report.bat` |
| Generate from existing JSON | `generate_report.bat` |
| Manual JSON generation | `behave --tags=@smoke -f json -o reports/test_results.json` |
| Manual HTML generation | `py generate_html_report.py` |
| Custom files | `py generate_html_report.py input.json output.html` |
| View report | Open `reports/test_report.html` in browser |

---

## Next Steps

1. ✅ Run tests with JSON output
2. ✅ Generate HTML report
3. ✅ View beautiful report in browser
4. Share report with team
5. Integrate with CI/CD
6. Customize styling (optional)

---

**Generated:** December 29, 2025
**Version:** 1.0
**Script:** `generate_html_report.py`
