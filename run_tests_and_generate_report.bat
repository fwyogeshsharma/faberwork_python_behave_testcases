@echo off
REM ===================================================================
REM Run Smoke Tests and Generate HTML Report
REM ===================================================================

echo.
echo ===================================================================
echo   Run Tests and Generate HTML Report
echo ===================================================================
echo.

REM Activate virtual environment
echo [1/3] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Please run: py -m venv venv
    pause
    exit /b 1
)

REM Run smoke tests with JSON output
echo.
echo [2/3] Running smoke tests...
echo.
behave --tags=@smoke -f json -o reports/test_results.json --no-capture
if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed, but continuing to generate report...
    echo.
)

REM Generate HTML report
echo.
echo [3/3] Generating HTML report...
echo.
py generate_html_report.py reports/test_results.json reports/test_report.html

REM Keep window open
echo.
echo Complete!
echo.
pause
