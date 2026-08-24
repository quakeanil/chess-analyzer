@echo off
title Chess Diagnostic Copilot
echo ========================================================
echo Starting Chess Diagnostic Copilot for 0kanil...
echo ========================================================
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying with full Python path...
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" main.py
)
pause
