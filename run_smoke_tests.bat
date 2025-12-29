@echo off
REM ===================================================================
REM Run Smoke Tests with Allure Report
REM ===================================================================

echo.
echo ===================================================================
echo   Faberwork Smoke Test Suite with Allure Reporting
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

REM Run the Python script
echo.
echo [2/3] Running smoke tests...
echo.
py run_smoke_tests_with_report.py

REM Keep window open
echo.
echo [3/3] Done!
echo.
pause
