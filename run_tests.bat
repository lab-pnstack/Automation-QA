@echo off
REM Windows CI Test Runner
REM Usage: run_tests.bat [chrome|firefox|all] [headless|headed]

setlocal

set BROWSER=%1
if "%BROWSER%"=="" set BROWSER=chrome

set MODE=%2
if "%MODE%"=="" set MODE=headless

echo ==========================================
echo Starting CI Test Execution
echo ==========================================
echo Browser: %BROWSER%
echo Mode: %MODE%
echo ==========================================

if "%MODE%"=="headless" (
    set HEADLESS=true
) else (
    set HEADLESS=false
)

if not exist reports mkdir reports
if not exist screenshots mkdir screenshots

if "%BROWSER%"=="all" (
    echo Running tests on Chrome...
    set BROWSER=chrome
    pytest tests/ -v -n auto --html=reports/report_chrome.html --self-contained-html

    echo Running tests on Firefox...
    set BROWSER=firefox
    pytest tests/ -v -n auto --html=reports/report_firefox.html --self-contained-html
) else (
    echo Running tests on %BROWSER%...
    pytest tests/ -v -n auto --html=reports/report_%BROWSER%.html --self-contained-html
)

echo ==========================================
echo Test Execution Completed
echo ==========================================
echo.
echo Reports available in: reports/
echo Screenshots available in: screenshots/

endlocal
