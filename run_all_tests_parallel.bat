@echo off
REM ===================================================================
REM Run All Tests in Parallel and Generate HTML Report
REM ===================================================================

echo.
echo ===================================================================
echo   Parallel Test Execution - Full Suite
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

REM Run all tests in parallel
echo.
echo [2/3] Running all tests in parallel...
echo This may take several minutes...
echo.
py -B run_tests_parallel.py --format json --clean --generate-report
if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed, but report was generated
    echo.
) else (
    echo.
    echo SUCCESS: All tests passed!
    echo.
)

REM Generate HTML report from merged results
echo.
echo [3/3] Generating HTML report from merged results...
echo.
py generate_html_report.py reports/test_results.json reports/test_report.html

REM Keep window open
echo.
echo Complete!
echo Check reports/test_report.html for detailed results
echo Check reports/parallel_execution_summary.json for execution statistics
echo.
pause
