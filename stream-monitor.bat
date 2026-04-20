@echo off
REM VartaPravah Stream Monitor for Windows
REM Continuously monitors FFmpeg process and restarts streamer if needed
REM Usage: stream-monitor.bat

setlocal enabledelayedexpansion
set LOG_FILE=logs\stream-monitor.log
set CHECK_INTERVAL=15
set RESTART_DELAY=5

if not exist logs mkdir logs

echo [%date% %time%] Stream Monitor started >> "%LOG_FILE%"

:loop
tasklist /FI "IMAGENAME eq ffmpeg.exe" 2>NUL | find /I /N "ffmpeg.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo [%date% %time%] WARNING: FFmpeg process not found - stream appears to have stopped >> "%LOG_FILE%"
    echo [%date% %time%] Attempting to restart vartapravah_stream service... >> "%LOG_FILE%"
    
    docker restart vartapravah_stream >> "%LOG_FILE%" 2>&1
    
    if %ERRORLEVEL% equ 0 (
        echo [%date% %time%] SUCCESS: Streamer service restarted >> "%LOG_FILE%"
    ) else (
        echo [%date% %time%] ERROR: Failed to restart streamer service >> "%LOG_FILE%"
    )
    
    timeout /t %RESTART_DELAY% /nobreak
) else (
    echo [%date% %time%] Stream active >> "%LOG_FILE%"
)

timeout /t %CHECK_INTERVAL% /nobreak
goto loop