@echo off
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "%~dp0dashboard.html"
if %ERRORLEVEL% NEQ 0 (
    start "" "msedge" "%~dp0dashboard.html"
)
