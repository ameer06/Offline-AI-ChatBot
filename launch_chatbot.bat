@echo off
REM =====================================================
REM AI Chatbot - One-Click Launch Script
REM This script starts backend AND opens frontend automatically
REM Perfect for presentations!
REM =====================================================

echo.
echo ========================================
echo   AI CHATBOT - LAUNCHING APPLICATION
echo ========================================
echo.

REM Navigate to project root
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please run install.bat first.
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo [1/3] Checking dependencies...
cd backend
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Dependencies not found. Installing...
    pip install -r requirements.txt
)
echo [OK] Dependencies ready!

REM Start the Flask backend in a new window
echo.
echo [2/3] Starting backend server...
start "AI Chatbot Backend" cmd /k "python app.py"

REM Wait for backend to start (3 seconds)
echo [OK] Backend starting...
timeout /t 3 /nobreak >nul

REM Open frontend in default browser
echo.
echo [3/3] Opening chatbot in browser...
cd ..
start "" "frontend\index.html"

echo.
echo ========================================
echo   CHATBOT LAUNCHED SUCCESSFULLY!
echo ========================================
echo.
echo Your chatbot is now running!
echo.
echo - Backend: http://localhost:5000
echo - Frontend: Opened in your browser
echo.
echo IMPORTANT: 
echo - Keep the backend window open while using the chatbot
echo - Close the backend window to stop the server
echo.

pause
