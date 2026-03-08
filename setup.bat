@echo off
REM DevForge Setup Script for Windows
REM This script sets up the entire DevForge system

echo.
echo ================================================
echo    DevForge Setup Script
echo ================================================
echo.

REM Check prerequisites
echo Checking prerequisites...

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed. Please install Python 3.11 or higher.
    exit /b 1
)

where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18 or higher.
    exit /b 1
)

where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] npm is not installed. Please install npm.
    exit /b 1
)

echo [OK] All prerequisites are installed
echo.

REM Setup Backend
echo Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo [WARNING] Please edit backend\.env and add your OPENAI_API_KEY
)

cd ..
echo [OK] Backend setup complete
echo.

REM Setup Frontend
echo Setting up frontend...
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
call npm install

REM Create .env.local if it doesn't exist
if not exist ".env.local" (
    echo Creating .env.local file...
    copy .env.local.example .env.local
)

cd ..
echo [OK] Frontend setup complete
echo.

REM Create generated_projects directory
if not exist "generated_projects" (
    mkdir generated_projects
    echo [OK] Created generated_projects directory
)

REM Summary
echo.
echo ================================================
echo    Setup Complete!
echo ================================================
echo.
echo Next steps:
echo.
echo 1. Add your OpenAI API key to backend\.env
echo    OPENAI_API_KEY=sk-your-key-here
echo.
echo 2. Start the backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python main.py
echo.
echo 3. In a new terminal, start the frontend:
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open your browser to http://localhost:3000
echo.
echo For more information, see:
echo   - docs\GETTING_STARTED.md
echo   - docs\SETUP.md
echo.
echo Happy building!
echo.
pause
