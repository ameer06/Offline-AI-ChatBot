@echo off
REM =====================================================
REM AI Chatbot - Quick Start Script
REM Double-click this file to start the chatbot server
REM =====================================================

echo.
echo ========================================
echo      AI CHATBOT - STARTING SERVER
echo ========================================
echo.

REM Navigate to backend folder
cd backend

REM Check if dependencies are installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Dependencies not installed!
    echo Installing now...
    pip install -r requirements.txt
)

echo.
echo Starting the backend server...
echo.
echo IMPORTANT: Keep this window open!
echo Close this window to stop the server.
echo.
echo Next step: Open frontend/index.html in your browser
echo.
echo ========================================
echo.

REM Start the Flask server
python app.py

pause
