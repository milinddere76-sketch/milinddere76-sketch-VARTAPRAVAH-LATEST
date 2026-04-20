@echo off
REM VartaPravah Pre-Deployment Sanity Check
REM Run this script to verify your system is ready for deployment

cls
echo ==================================
echo VartaPravah Sanity Check
echo ==================================
echo.

setlocal enabledelayedexpansion
set CHECKS_PASSED=0
set CHECKS_FAILED=0
set CHECKS_WARNING=0

echo 1. Checking Docker Installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Docker not installed
    set /a CHECKS_FAILED+=1
) else (
    for /f "tokens=*" %%i in ('docker --version') do echo [PASS] %%i
    set /a CHECKS_PASSED+=1
)

echo.
echo 2. Checking Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Docker Compose not installed
    set /a CHECKS_FAILED+=1
) else (
    for /f "tokens=*" %%i in ('docker-compose --version') do echo [PASS] %%i
    set /a CHECKS_PASSED+=1
)

echo.
echo 3. Checking Docker Daemon...
docker ps >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Docker daemon is not running
    set /a CHECKS_FAILED+=1
) else (
    echo [PASS] Docker daemon is running
    set /a CHECKS_PASSED+=1
)

echo.
echo 4. Checking Configuration...
if exist .env (
    echo [PASS] .env file exists
    set /a CHECKS_PASSED+=1
    findstr "YOUTUBE_STREAM_KEY=" .env >nul 2>&1
    if errorlevel 1 (
        echo [FAIL] YOUTUBE_STREAM_KEY not found in .env
        set /a CHECKS_FAILED+=1
    ) else (
        echo [PASS] YouTube Stream Key configured
        set /a CHECKS_PASSED+=1
    )
) else (
    echo [FAIL] .env file not found
    set /a CHECKS_FAILED+=1
)

echo.
echo 5. Checking Docker Compose Configuration...
if exist docker-compose.yml (
    echo [PASS] docker-compose.yml exists
    set /a CHECKS_PASSED+=1
    docker-compose config >nul 2>&1
    if errorlevel 1 (
        echo [FAIL] docker-compose.yml validation failed
        set /a CHECKS_FAILED+=1
    ) else (
        echo [PASS] docker-compose.yml is valid
        set /a CHECKS_PASSED+=1
    )
) else (
    echo [FAIL] docker-compose.yml not found
    set /a CHECKS_FAILED+=1
)

echo.
echo 6. Checking Project Files...
for %%F in (main.py requirements.txt Dockerfile) do (
    if exist %%F (
        echo [PASS] %%F exists
        set /a CHECKS_PASSED+=1
    ) else (
        echo [FAIL] %%F missing
        set /a CHECKS_FAILED+=1
    )
)

echo.
echo 7. Checking Asset Directories...
for %%D in (app\assets app\assets\fonts app\assets\anchors app\encoder) do (
    if exist %%D (
        echo [PASS] %%D exists
        set /a CHECKS_PASSED+=1
    ) else (
        echo [FAIL] %%D missing
        set /a CHECKS_FAILED+=1
    )
)

echo.
echo 8. Checking Asset Files...
if exist "app\assets\fonts\NotoSansDevanagari-Bold.ttf" (
    echo [PASS] Devanagari font found
    set /a CHECKS_PASSED+=1
) else (
    echo [WARN] Devanagari font not found
    set /a CHECKS_WARNING+=1
)

if exist "app\assets\anchors\male.png" (
    echo [PASS] Male anchor image found
    set /a CHECKS_PASSED+=1
) else (
    echo [WARN] Male anchor image not found
    set /a CHECKS_WARNING+=1
)

if exist "app\assets\anchors\female.png" (
    echo [PASS] Female anchor image found
    set /a CHECKS_PASSED+=1
) else (
    echo [WARN] Female anchor image not found
    set /a CHECKS_WARNING+=1
)

echo.
echo 9. Checking Port Availability...
netstat -ano | findstr :8000 >nul 2>&1
if errorlevel 1 (
    echo [PASS] Port 8000 is available
    set /a CHECKS_PASSED+=1
) else (
    echo [FAIL] Port 8000 is already in use
    set /a CHECKS_FAILED+=1
)

echo.
echo ==================================
echo Summary:
echo Passed:  !CHECKS_PASSED!
echo Failed:  !CHECKS_FAILED!
echo Warnings: !CHECKS_WARNING!
echo ==================================
echo.

if %CHECKS_FAILED% equ 0 (
    echo [PASS] System is ready for deployment!
    echo.
    echo Next steps:
    echo 1. Start services:
    echo    docker-compose up -d
    echo.
    echo 2. Check API:
    echo    http://localhost:8000/docs
    echo.
    pause
    exit /b 0
) else (
    echo [FAIL] System is not ready. Fix the errors above and run again.
    pause
    exit /b 1
)