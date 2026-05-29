@echo off
setlocal

:: Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

title Scenic Digital Backend Builder

echo.
echo ============================================================
echo   Scenic Digital - Backend Builder
echo ============================================================
echo.

cd /d %~dp0..

echo [INFO] Project: %CD%
echo.

:: Step 1: Check environment
echo [STEP 1/3] Checking environment...
echo.

python --version
if errorlevel 1 (
    echo [ERROR] Python not found
    echo Please install Python 3.8+
    goto :end
)
echo   [OK] Python

python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo   Installing PyInstaller...
    python -m pip install pyinstaller -q
)
echo   [OK] PyInstaller

echo.

:: Step 2: Build backend
echo [STEP 2/3] Building backend...
echo.

cd backend

:: Clean old files
if exist dist (
    echo Cleaning dist...
    rd /s /q dist
)
if exist build (
    echo Cleaning build...
    rd /s /q build
)
if exist *.spec (
    echo Cleaning spec...
    del /q *.spec
)

echo.
echo Packaging backend...
echo.

pyinstaller --name=scenic-backend --onefile --console --clean --add-data=app;app --add-data=config.py;. --hidden-import=flask --hidden-import=flask_cors --hidden-import=pymysql --hidden-import=dotenv --hidden-import=werkzeug --hidden-import=werkzeug.security run.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed
    cd ..
    goto :end
)

echo.
echo [OK] Backend built: backend\dist\scenic-backend.exe

cd ..

:: Step 3: Copy .env
echo.
echo [STEP 3/3] Copying config...
echo.

if exist backend\.env (
    copy /y backend\.env backend\dist\.env >nul
    echo   [OK] .env copied to backend\dist\
) else (
    echo   [WARN] backend\.env not found
    echo   Please create .env in backend\dist\ before running
)

if not exist backend\dist\uploads mkdir backend\dist\uploads
echo   [OK] uploads dir created

:: Done
echo.
echo ============================================================
echo   Build completed!
echo ============================================================
echo.
echo Output: backend\dist\scenic-backend.exe
echo.
echo To run:
echo   cd backend\dist
echo   scenic-backend.exe
echo.
echo Make sure .env is in the same directory as scenic-backend.exe
echo.

:end
echo ============================================================
echo.
pause
