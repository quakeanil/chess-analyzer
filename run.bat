@echo off
title Chess Diagnostic Copilot
echo ========================================================
echo Starting Chess Diagnostic Copilot for 0kanil...
echo ========================================================
if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" main.py
) else (
    python main.py
)
pause
