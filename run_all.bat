@echo off
title HireFlow - Original Web App
echo ===================================================
echo             HireFlow AI Hiring Platform
echo ===================================================
echo.

cd /d "%~dp0"

echo [1/2] Checking Streamlit AI Engine (port 8501)...
netstat -ano | findstr :8501 >nul
if %errorlevel% neq 0 (
    echo Starting Streamlit backend on http://localhost:8501...
    start /min "HireFlow Streamlit" python -m streamlit run app.py --server.port 8501 --server.headless true
) else (
    echo Streamlit backend is active on http://localhost:8501.
)

echo.
echo [2/2] Checking HireFlow Web App (port 5000)...
netstat -ano | findstr :5000 >nul
if %errorlevel% neq 0 (
    echo Starting Web Server on http://localhost:5000...
    start /min "HireFlow Web" python -m http.server 5000 --directory "%~dp0"
) else (
    echo Web Server is active on http://localhost:5000.
)

echo.
echo Opening HireFlow in your browser...
timeout /t 1 /nobreak >nul
start http://localhost:5000

echo.
echo ===================================================
echo HireFlow is running!
echo Web App:          http://localhost:5000
echo Streamlit Engine: http://localhost:8501
echo ===================================================
echo.
pause
