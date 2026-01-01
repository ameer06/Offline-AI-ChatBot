@echo off
REM =====================================================
REM AI Chatbot - Automatic Installation Script
REM This script will install everything automatically
REM =====================================================

echo.
echo ========================================
echo   AI CHATBOT - INSTALLATION SCRIPT
echo ========================================
echo.

REM Check if Python is installed
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
echo [OK] Python is installed!

REM Check if Ollama is installed
echo.
echo [2/4] Checking Ollama installation...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Ollama is not installed!
    echo.
    echo Please install Ollama from: https://ollama.com/download
    echo After installation, restart your computer and run this script again.
    echo.
    pause
    exit /b 1
)
echo [OK] Ollama is installed!

REM Install Python dependencies
echo.
echo [3/4] Installing Python dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
cd ..
echo [OK] Dependencies installed!

REM Check if model is downloaded
echo.
echo [4/4] Checking for AI model...
ollama list | find "llama3.2" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Llama3.2 model not found. Downloading now...
    echo This will take 5-15 minutes depending on your internet speed.
    echo.
    ollama pull llama3.2
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to download model!
        pause
        exit /b 1
    )
)
echo [OK] AI model is ready!

echo.
echo ========================================
echo   INSTALLATION COMPLETE!
echo ========================================
echo.
echo Your chatbot is ready to use!
echo.
echo To start the chatbot:
echo   1. Run: start_chatbot.bat
echo   2. Wait for "Running on http://localhost:5000"
echo   3. Open frontend/index.html in your browser
echo.
pause
