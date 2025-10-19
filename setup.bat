@echo off
REM Setup script for Windows

echo ========================================
echo Kids Coloring Page Generator - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip

echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [5/5] Setting up environment file...
if not exist .env (
    copy env.example .env
    echo Created .env file. Please edit it and add your API keys!
) else (
    echo .env file already exists. Skipping...
)

REM Create necessary directories
if not exist "static\uploads" mkdir "static\uploads"
if not exist "static\outputs" mkdir "static\outputs"

echo.
echo ========================================
echo Setup Complete! ✓
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your API keys
echo    - Get Stability AI key: https://platform.stability.ai/
echo    - Get OpenAI key (optional): https://platform.openai.com/
echo 2. Run the application:
echo    - venv\Scripts\activate
echo    - python run.py
echo.
pause

