@echo off
REM VartaPravah Broadcast System Startup Script for Windows

echo ================================
echo VartaPravah TV Broadcast System
echo ================================
echo.

REM Check if .env exists
if not exist .env (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and fill in your YouTube Stream Key
    echo Copy-Item -Path .env.example -Destination .env
    pause
    exit /b 1
)

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

echo OK: Docker is installed
echo.

REM Build images
echo Building Docker images...
docker-compose build

echo.
echo Starting VartaPravah services...
docker-compose up -d

echo.
echo OK: Services started!
echo.
echo Monitor logs with:
echo    docker-compose logs -f app
echo.
echo API available at: http://localhost:8000
echo API documentation: http://localhost:8000/docs
echo.
echo To stop services:
echo    docker-compose down
echo.
pause