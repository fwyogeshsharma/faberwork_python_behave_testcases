@echo off
REM ===================================================================
REM Generate HTML Report from JSON Test Results
REM ===================================================================

echo.
echo ===================================================================
echo   HTML Report Generator
echo ===================================================================
echo.

REM Activate virtual environment
echo [1/2] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Please run: py -m venv venv
    pause
    exit /b 1
)

REM Generate HTML report
echo.
echo [2/2] Generating HTML report from JSON...
echo.
py generate_html_report.py reports/test_results.json reports/test_report.html

REM Keep window open
echo.
echo Done!
echo.
pause
