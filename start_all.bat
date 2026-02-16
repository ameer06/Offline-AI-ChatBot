@echo off
REM =====================================================
REM AI Chatbot - COMPLETE Launch Script
REM This starts Ollama AND Backend AND Frontend
REM =====================================================

echo.
echo ========================================
echo   AI CHATBOT - COMPLETE STARTUP
echo ========================================
echo.

cd /d "%~dp0"

REM Step 1: Start Ollama
echo [1/4] Starting Ollama AI service...
start "Ollama AI Service" cmd /c "ollama serve"
timeout /t 3 /nobreak >nul
echo [OK] Ollama started!

REM Step 2: Check Python
echo.
echo [2/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please run install.bat first.
    pause
    exit /b 1
)
echo [OK] Python is installed!

REM Step 3: Start Backend Server
echo.
echo [3/4] Starting Flask backend server...
cd backend
start "AI Chatbot Backend" cmd /k "python app.py"
cd ..
timeout /t 5 /nobreak >nul
echo [OK] Backend server started!

REM Step 4: Open Frontend
echo.
echo [4/4] Opening chatbot in browser...
start "" "frontend\index.html"

echo.
echo ========================================
echo   ALL SERVICES STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Your chatbot is now fully running!
echo.
echo Services:
echo  - Ollama AI:  http://localhost:11434
echo  - Backend:    http://localhost:5000  
echo  - Frontend:   Opened in browser
echo.
echo IMPORTANT: 
echo  - Keep ALL windows open while using the chatbot
echo  - Close windows to stop the services
echo  - If you see errors, check the other windows
echo.

pause
