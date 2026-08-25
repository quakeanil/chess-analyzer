@echo off
title Chess Analyzer - Mobile Server (Xiaomi 17 Ultra)
cd /d "%~dp0"
echo Starting Chess Analyzer Mobile Server...
"C:\Users\okanil\AppData\Local\Programs\Python\Python314\python.exe" serve_mobile.py
pause
