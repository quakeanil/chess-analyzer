@echo off
title Scandinavian Defense Live Mentor - Antigravity
echo ========================================================
echo Starting Scandinavian Defense AI Mentor Server...
echo ========================================================
if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    start "" "http://localhost:5050/mentor"
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" mentor_server.py
) else (
    start "" "http://localhost:5050/mentor"
    python mentor_server.py
)
pause
