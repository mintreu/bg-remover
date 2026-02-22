@echo off
SETLOCAL EnableDelayedExpansion

echo.
echo ========================================
echo   Mintreu BG Remover Tool v0.1
echo   Auto-Install and Run
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    echo Install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Python found
python --version

:: Create venv if needed
if not exist "venv\" (
    echo.
    echo [2/3] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create venv!
        pause
        exit /b 1
    )
) else (
    echo.
    echo [2/3] Virtual environment exists
)

:: Activate venv
call venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip --quiet

:: Install from pyproject.toml ONLY
echo.
echo [3/3] Installing dependencies from pyproject.toml...
pip install -e . --quiet

if errorlevel 1 (
    echo [WARNING] pip install -e . failed, trying direct install...
    pip install onnxruntime numpy pillow opencv-python-headless PySide6 requests tqdm --quiet
)

echo.
echo ========================================
echo   Starting Application...
echo ========================================
echo.

:: Run app
python main.py

:: Cleanup
deactivate
pause
