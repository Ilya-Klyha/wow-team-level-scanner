@echo off
REM DoR Compliance Analysis Runner
REM Executes the DoR analysis script and generates Report.xlsx

echo ========================================
echo DoR Compliance Analysis - Step 11
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    echo Please install Python 3.7 or later
    pause
    exit /b 1
)

echo Running DoR analysis...
echo.

cd /d "%~dp0"
python generate_dor_report.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo Generated files:
    echo   - Report.xlsx
    echo   - DOR_ANALYSIS_SUMMARY.md
    echo   - teams.json (updated)
    echo.
) else (
    echo.
    echo ERROR: Analysis failed
    echo Check the error messages above
)

pause
