"""
Mintreu BG Remover - Complete Offline Distribution Builder
===========================================================
Creates fully self-contained, offline-ready distributions:
1. Portable ZIP with embedded Python
2. Windows Installer (Inno Setup)
3. Single EXE with PyInstaller
4. Offline pip packages bundle

Author: Krishanu Bhattacharya
Company: Mintreu
License: MIT
"""

import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile
import json
from pathlib import Path
from typing import List, Dict

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_NAME = "MintreuBgRemover"
APP_VERSION = "1.0.0"
COMPANY_NAME = "Mintreu"
DEVELOPER_NAME = "Krishanu Bhattacharya"
WEBSITE = "https://mintreu.com"

PROJECT_ROOT = Path(__file__).parent
DIST_ROOT = PROJECT_ROOT / "distributions"
BUILD_DIR = PROJECT_ROOT / "build"

# Python embedded version to download
PYTHON_VERSION = "3.11.9"
PYTHON_EMBED_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"

# Required packages
REQUIRED_PACKAGES = [
    "onnxruntime>=1.19.0",
    "numpy>=1.24.0,<2.0.0",
    "pillow>=10.0.0",
    "opencv-python-headless>=4.8.0",
    "PySide6>=6.6.0",
    "requests>=2.31.0",
    "tqdm>=4.66.0",
    "pyinstaller>=6.0.0"
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_header(text: str):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(text: str):
    """Print step information."""
    print(f"\n▶ {text}")

def print_success(text: str):
    """Print success message."""
    print(f"✅ {text}")

def print_error(text: str):
    """Print error message."""
    print(f"❌ {text}")

def run_command(cmd: List[str], description: str, cwd=None) -> bool:
    """Run command and return success status."""
    print_step(description)
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        print_success(description)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed: {e.stderr}")
        return False
    except FileNotFoundError:
        print_error(f"Command not found: {cmd[0]}")
        return False

def download_file(url: str, dest: Path, description: str):
    """Download file with progress."""
    print_step(f"Downloading {description}")

    try:
        with urllib.request.urlopen(url) as response:
            total_size = int(response.headers.get('content-length', 0))

            with open(dest, 'wb') as f:
                downloaded = 0
                chunk_size = 8192

                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break

                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r  Progress: {percent:.1f}% ({downloaded / (1024*1024):.1f} MB)", end='')

        print()
        print_success(f"Downloaded {description}")
        return True
    except Exception as e:
        print()
        print_error(f"Download failed: {e}")
        return False

# ============================================================================
# BUILD FUNCTIONS
# ============================================================================

def clean_build():
    """Clean previous build artifacts."""
    print_header("Cleaning Previous Builds")

    folders_to_clean = [DIST_ROOT, BUILD_DIR]
    for folder in folders_to_clean:
        if folder.exists():
            shutil.rmtree(folder)
            print_success(f"Cleaned {folder}")

    # Create fresh directories
    DIST_ROOT.mkdir(parents=True, exist_ok=True)
    print_success("Build directories ready")

def download_python_embedded():
    """Download Python embedded distribution."""
    print_header("Downloading Python Embedded Distribution")

    python_dir = BUILD_DIR / "python_embedded"
    python_zip = BUILD_DIR / "python_embedded.zip"

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    if not python_zip.exists():
        if not download_file(PYTHON_EMBED_URL, python_zip, f"Python {PYTHON_VERSION} Embedded"):
            return None
    else:
        print_success("Python embedded already downloaded")

    # Extract
    print_step("Extracting Python embedded")
    python_dir.mkdir(exist_ok=True)

    with zipfile.ZipFile(python_zip, 'r') as zip_ref:
        zip_ref.extractall(python_dir)

    print_success("Python embedded extracted")

    # Enable pip by modifying python311._pth
    pth_file = python_dir / f"python{PYTHON_VERSION.replace('.', '')[:3]}._pth"
    if pth_file.exists():
        content = pth_file.read_text()
        content = content.replace("#import site", "import site")
        pth_file.write_text(content)
        print_success("Enabled pip in embedded Python")

    return python_dir

def download_pip_packages(python_dir: Path):
    """Download all required packages for offline installation."""
    print_header("Downloading Pip Packages for Offline Use")

    packages_dir = DIST_ROOT / "offline_packages"
    packages_dir.mkdir(parents=True, exist_ok=True)

    # Download get-pip.py
    get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
    get_pip_path = packages_dir / "get-pip.py"

    if not get_pip_path.exists():
        download_file(get_pip_url, get_pip_path, "get-pip.py")

    # Install pip in embedded Python
    python_exe = python_dir / "python.exe"
    run_command(
        [str(python_exe), str(get_pip_path)],
        "Installing pip in embedded Python"
    )

    # Download all packages
    print_step("Downloading all required packages")

    cmd = [
        str(python_exe),
        "-m", "pip", "download",
        "--dest", str(packages_dir),
        "--prefer-binary"
    ] + REQUIRED_PACKAGES

    run_command(cmd, "Downloading packages")

    return packages_dir

def create_portable_distribution():
    """Create portable ZIP distribution with embedded Python."""
    print_header("Creating Portable Distribution")

    portable_dir = DIST_ROOT / "portable"
    portable_dir.mkdir(parents=True, exist_ok=True)

    app_dir = portable_dir / APP_NAME
    app_dir.mkdir(exist_ok=True)

    # Download Python embedded
    python_dir = download_python_embedded()
    if not python_dir:
        print_error("Failed to download Python embedded")
        return False

    # Copy Python to app directory
    print_step("Copying Python to portable directory")
    python_dest = app_dir / "python"
    shutil.copytree(python_dir, python_dest, dirs_exist_ok=True)
    print_success("Python copied")

    # Download packages
    packages_dir = download_pip_packages(python_dest)

    # Copy application files
    print_step("Copying application files")

    # Copy main.py
    shutil.copy2(PROJECT_ROOT / "main.py", app_dir / "main.py")

    # Copy updater.py
    updater_src = PROJECT_ROOT / "updater.py"
    if updater_src.exists():
        shutil.copy2(updater_src, app_dir / "updater.py")

    # Copy config_loader.py
    config_loader_src = PROJECT_ROOT / "config_loader.py"
    if config_loader_src.exists():
        shutil.copy2(config_loader_src, app_dir / "config_loader.py")

    # Copy config.ini
    config_src = PROJECT_ROOT / "config.ini"
    if config_src.exists():
        shutil.copy2(config_src, app_dir / "config.ini")

    # Copy models directory
    models_src = PROJECT_ROOT / "models"
    if models_src.exists():
        shutil.copytree(models_src, app_dir / "models", dirs_exist_ok=True)
    else:
        (app_dir / "models").mkdir(exist_ok=True)

    # Copy assets
    assets_src = PROJECT_ROOT / "assets"
    if assets_src.exists():
        shutil.copytree(assets_src, app_dir / "assets", dirs_exist_ok=True)

    # Copy license
    license_src = PROJECT_ROOT / "LICENSE.txt"
    if license_src.exists():
        shutil.copy2(license_src, app_dir / "LICENSE.txt")

    print_success("Application files copied")

    # Create launcher script
    create_launcher_script(app_dir, python_dest)

    # Create install script
    create_install_script(app_dir, python_dest, packages_dir)

    # Create README
    create_readme(app_dir)

    # Zip the portable directory
    print_step("Creating portable ZIP archive")
    zip_path = DIST_ROOT / f"{APP_NAME}_v{APP_VERSION}_Portable.zip"

    shutil.make_archive(
        str(zip_path.with_suffix('')),
        'zip',
        portable_dir
    )

    print_success(f"Portable distribution created: {zip_path}")

    # Calculate size
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"  📦 Size: {size_mb:.1f} MB")

    return True

def create_launcher_script(app_dir: Path, python_dir: Path):
    """Create launcher script for the application."""
    print_step("Creating launcher script")

    launcher_content = f"""@echo off
REM Mintreu BG Remover - Launcher
REM Automatically installs dependencies on first run

title {APP_NAME} - Launcher
cd /d "%~dp0"

echo.
echo ========================================
echo   {APP_NAME} v{APP_VERSION}
echo   {COMPANY_NAME}
echo ========================================
echo.

REM Check if dependencies are installed
if not exist "python\\Lib\\site-packages\\onnxruntime" (
    echo First time setup detected...
    echo Installing dependencies offline...
    echo.
    call install_dependencies.bat
)

echo Starting application...
echo.

REM Run the application
python\\python.exe main.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERROR: Application failed to start
    echo ========================================
    echo.
    echo Please check:
    echo 1. Dependencies are installed correctly
    echo 2. Models are downloaded in models folder
    echo.
    pause
)

exit
"""

    launcher_path = app_dir / f"{APP_NAME}.bat"
    launcher_path.write_text(launcher_content, encoding='utf-8')
    print_success("Launcher script created")

def create_install_script(app_dir: Path, python_dir: Path, packages_dir: Path):
    """Create dependency installation script."""
    print_step("Creating installation script")

    install_content = f"""@echo off
REM Mintreu BG Remover - Offline Dependency Installer

title {APP_NAME} - Installing Dependencies
cd /d "%~dp0"

echo.
echo ========================================
echo   {APP_NAME} v{APP_VERSION}
echo   Offline Dependency Installation
echo ========================================
echo.

REM Check if pip is installed
python\\python.exe -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Installing pip...
    python\\python.exe offline_packages\\get-pip.py
    echo.
)

echo Installing application dependencies...
echo This may take 2-5 minutes...
echo.

REM Install from offline packages
python\\python.exe -m pip install --no-index --find-links=offline_packages {' '.join(REQUIRED_PACKAGES)}

if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERROR: Installation failed
    echo ========================================
    echo.
    echo Please check your internet connection or contact support.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo You can now run {APP_NAME}.bat to start the application.
echo.

pause
"""

    install_path = app_dir / "install_dependencies.bat"
    install_path.write_text(install_content, encoding='utf-8')
    print_success("Installation script created")

def create_readme(app_dir: Path):
    """Create README file."""
    print_step("Creating README")

    readme_content = f"""# {APP_NAME} v{APP_VERSION}

**Professional AI Background Removal Tool - 100% Offline Capable**

Company: {COMPANY_NAME}
Developer: {DEVELOPER_NAME}
Website: {WEBSITE}
License: MIT

## Features

✅ AI-powered background removal using RMBG v1.4 model
✅ 100% offline operation (no internet required after setup)
✅ Batch processing support
✅ Dark mode UI
✅ Drag & drop interface
✅ Multiple format support (PNG, JPG, JPEG, WEBP, BMP, TIFF)
✅ Portable - runs without installation

## Quick Start

### First Time Setup (5 minutes)

1. Extract the ZIP file to any location
2. Double-click `{APP_NAME}.bat` to launch
3. Dependencies will auto-install on first run (offline, no internet needed)
4. Download AI models when prompted (requires internet, one-time only)

### Subsequent Use

- Just double-click `{APP_NAME}.bat` to start
- No internet connection required after initial setup

## Manual Installation (If Needed)

If automatic installation fails:

1. Run `install_dependencies.bat` manually
2. Then run `{APP_NAME}.bat`

## System Requirements

- Windows 10/11 (64-bit)
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space (+ space for your images)
- Internet connection only for first-time model download

## Directory Structure

```
{APP_NAME}/
├── {APP_NAME}.bat          (Main launcher)
├── install_dependencies.bat (Manual installer)
├── main.py                  (Application code)
├── python/                  (Embedded Python {PYTHON_VERSION})
├── offline_packages/        (Pre-downloaded dependencies)
├── models/                  (AI models - download on first run)
├── assets/                  (Application assets)
├── output/                  (Processed images saved here)
└── README.txt               (This file)
```

## Usage

1. Launch the application
2. Add images using "Add Images" or drag & drop
3. Select AI model (RMBG v1.4 Fast recommended)
4. Click "Start Processing"
5. Processed images will be saved in the `output` folder

## Troubleshooting

**Application won't start:**
- Run `install_dependencies.bat` manually
- Check that `python/python.exe` exists
- Make sure you extracted all files

**Models not found:**
- Click "System" → "Download Models" in the menu
- Requires internet connection for one-time download
- Models are ~176 MB

**Slow processing:**
- Close other applications to free up RAM
- Use RMBG v1.4 Fast model for better speed
- Reduce number of worker threads in settings

## Support

- Website: {WEBSITE}
- Email: contact@mintreu.com
- Issues: Check logs in `%USERPROFILE%\\.mintreu_bg_remover\\app.log`

## License

MIT License - See LICENSE.txt

Copyright (c) 2025 {COMPANY_NAME}
Developed by {DEVELOPER_NAME}

---

Thank you for using {APP_NAME}!
"""

    readme_path = app_dir / "README.txt"
    readme_path.write_text(readme_content, encoding='utf-8')
    print_success("README created")

def create_pyinstaller_exe():
    """Create single EXE using PyInstaller."""
    print_header("Creating PyInstaller Single EXE")

    # Check if pyinstaller is installed
    try:
        import PyInstaller
        print_success(f"PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print_step("Installing PyInstaller")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    exe_dir = DIST_ROOT / "exe"
    exe_dir.mkdir(parents=True, exist_ok=True)

    # Run PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "main.py",
        "--name", APP_NAME,
        "--onefile",
        "--windowed",
        "--noconfirm",
        f"--icon={PROJECT_ROOT / 'assets' / 'favicon.ico'}",
        f"--distpath={exe_dir}",
        f"--workpath={BUILD_DIR / 'pyinstaller_work'}",
        f"--specpath={BUILD_DIR}",
        "--collect-all", "PySide6",
        "--collect-all", "onnxruntime",
        "--collect-all", "cv2",
        "--collect-all", "PIL",
        "--collect-all", "numpy",
        "--hidden-import", "PySide6.QtOpenGL",
        "--hidden-import", "PySide6.QtSvg",
    ]

    # Add models and assets as data
    models_dir = PROJECT_ROOT / "models"
    assets_dir = PROJECT_ROOT / "assets"

    if models_dir.exists():
        cmd.extend(["--add-data", f"{models_dir}{os.pathsep}models"])
    if assets_dir.exists():
        cmd.extend(["--add-data", f"{assets_dir}{os.pathsep}assets"])

    success = run_command(cmd, "Building single EXE with PyInstaller", cwd=PROJECT_ROOT)

    if success:
        exe_file = exe_dir / f"{APP_NAME}.exe"
        if exe_file.exists():
            size_mb = exe_file.stat().st_size / (1024 * 1024)
            print_success(f"EXE created: {exe_file}")
            print(f"  📦 Size: {size_mb:.1f} MB")
            return True

    return False

def create_inno_setup_script():
    """Create Inno Setup installer script."""
    print_header("Creating Inno Setup Installer Script")

    inno_dir = DIST_ROOT / "installer"
    inno_dir.mkdir(parents=True, exist_ok=True)

    # Get portable dir path
    portable_dir = DIST_ROOT / "portable" / APP_NAME

    if not portable_dir.exists():
        print_error("Portable distribution not found. Build it first.")
        return False

    inno_script = f"""
; Mintreu BG Remover - Inno Setup Installer Script
; Generated by build_complete_offline.py

#define MyAppName "{APP_NAME}"
#define MyAppVersion "{APP_VERSION}"
#define MyAppPublisher "{COMPANY_NAME}"
#define MyAppURL "{WEBSITE}"
#define MyAppExeName "{APP_NAME}.bat"

[Setup]
AppId={{{{B8E9D2F1-5C4A-4B8E-9F7A-3D6C8E9A1B2C}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
LicenseFile={PROJECT_ROOT / 'LICENSE.txt'}
OutputDir={inno_dir}
OutputBaseFilename={APP_NAME}_v{APP_VERSION}_Setup
SetupIconFile={PROJECT_ROOT / 'assets' / 'favicon.ico'}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
Source: "{portable_dir}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\install_dependencies.bat"; Description: "Install dependencies"; Flags: postinstall runhidden
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Installation complete!' + #13#10#13#10 +
           'On first launch:' + #13#10 +
           '1. Dependencies will auto-install' + #13#10 +
           '2. Download AI models when prompted' + #13#10 +
           '3. Internet required only for first setup',
           mbInformation, MB_OK);
  end;
end;
"""

    script_path = inno_dir / f"{APP_NAME}_installer.iss"
    script_path.write_text(inno_script, encoding='utf-8')

    print_success(f"Inno Setup script created: {script_path}")
    print()
    print("  📋 To build the installer:")
    print("  1. Install Inno Setup from https://jrsoftware.org/isinfo.php")
    print(f"  2. Open {script_path}")
    print("  3. Click Build → Compile")
    print()

    return True

# ============================================================================
# MAIN BUILD ORCHESTRATOR
# ============================================================================

def build_all_distributions():
    """Build all distribution formats."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║         Mintreu BG Remover - Complete Build System              ║
║                                                                  ║
║         Building fully offline-capable distributions             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")

    print(f"Project: {APP_NAME} v{APP_VERSION}")
    print(f"Company: {COMPANY_NAME}")
    print(f"Developer: {DEVELOPER_NAME}")
    print()

    # Clean
    clean_build()

    # Build portable distribution (includes embedded Python + offline packages)
    success_portable = create_portable_distribution()

    # Create Inno Setup script
    if success_portable:
        create_inno_setup_script()

    # Build single EXE
    print()
    print("Would you like to build a single EXE with PyInstaller? (slower, larger file)")
    print("This requires all dependencies installed in current Python environment.")
    response = input("Build PyInstaller EXE? (y/n): ").strip().lower()

    if response == 'y':
        create_pyinstaller_exe()

    # Summary
    print_header("Build Complete!")
    print()
    print("📦 Distribution files created in:", DIST_ROOT)
    print()

    if success_portable:
        portable_zip = DIST_ROOT / f"{APP_NAME}_v{APP_VERSION}_Portable.zip"
        if portable_zip.exists():
            size_mb = portable_zip.stat().st_size / (1024 * 1024)
            print(f"✅ Portable ZIP: {portable_zip.name} ({size_mb:.1f} MB)")

    inno_script = DIST_ROOT / "installer" / f"{APP_NAME}_installer.iss"
    if inno_script.exists():
        print(f"✅ Inno Setup Script: {inno_script}")

    exe_file = DIST_ROOT / "exe" / f"{APP_NAME}.exe"
    if exe_file.exists():
        size_mb = exe_file.stat().st_size / (1024 * 1024)
        print(f"✅ Single EXE: {exe_file.name} ({size_mb:.1f} MB)")

    print()
    print("🎉 All distributions are 100% offline-capable!")
    print("   Users only need internet for first-time AI model download.")
    print()

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        build_all_distributions()
    except KeyboardInterrupt:
        print()
        print_error("Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Build failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
