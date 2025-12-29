@echo off
REM ===================================================================
REM Run Tests in Parallel with Custom Options
REM Usage: run_parallel.bat [workers] [tag]
REM Example: run_parallel.bat 4 smoke
REM ===================================================================

echo.
echo ===================================================================
echo   Parallel Test Execution - Custom Configuration
echo ===================================================================
echo.

REM Activate virtual environment
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Parse arguments
set WORKERS=%1
set TAG=%2

REM Build command
set CMD=py run_tests_parallel.py --format json --clean --generate-report

if not "%WORKERS%"=="" (
    set CMD=%CMD% --workers %WORKERS%
    echo Workers: %WORKERS%
)

if not "%TAG%"=="" (
    set CMD=%CMD% --tag %TAG%
    echo Tag Filter: @%TAG%
)

echo.
echo Running: %CMD%
echo.

REM Run tests
%CMD%

REM Generate HTML report
echo.
echo Generating HTML report...
py generate_html_report.py reports/test_results.json reports/test_report.html

echo.
echo Complete!
echo.
pause
