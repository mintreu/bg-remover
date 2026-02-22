@echo off
REM Mintreu BG Remover - Test Runner
REM Runs comprehensive test suite before deployment

title Mintreu BG Remover - Test Suite
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║        Mintreu BG Remover - Comprehensive Test Suite            ║
echo ║                                                                  ║
echo ║                      Version 1.0.0                               ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo [1/5] Checking Python version...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
echo.

echo [2/5] Checking dependencies...
python -c "import onnxruntime, numpy, PIL, cv2, PySide6, requests, tqdm" 2>nul
if errorlevel 1 (
    echo [WARNING] Some dependencies missing. Installing...
    pip install -q -r requirements.txt
)
echo ✓ Dependencies OK
echo.

echo [3/5] Running application tests...
python test_application.py
if errorlevel 1 (
    echo.
    echo [ERROR] Tests failed!
    echo Please fix errors before deploying.
    pause
    exit /b 1
)
echo.

echo [4/5] Checking code quality...
echo   - Checking for syntax errors...
python -m py_compile main.py 2>nul
if errorlevel 1 (
    echo   [ERROR] Syntax errors found in main.py
    pause
    exit /b 1
)
python -m py_compile build_complete_offline.py 2>nul
if errorlevel 1 (
    echo   [ERROR] Syntax errors found in build_complete_offline.py
    pause
    exit /b 1
)
echo   ✓ No syntax errors
echo.

echo [5/5] Verification complete!
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║                    ✅ ALL TESTS PASSED ✅                        ║
echo ║                                                                  ║
echo ║        Application is ready for distribution!                   ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo Next steps:
echo   1. Build portable distribution: python build_complete_offline.py
echo   2. Test distributions on clean Windows VM
echo   3. Deploy to production
echo.

pause
