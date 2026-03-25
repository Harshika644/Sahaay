@echo off
setlocal

cd /d "%~dp0"

echo Starting Sahaay local server...
start "" http://127.0.0.1:8000/index.html
python app.py

endlocal
