@echo off
cd /d "%~dp0"
echo Installing libraries...
py -m pip install -r requirements.txt --quiet
echo.
py main.py
echo.
pause
