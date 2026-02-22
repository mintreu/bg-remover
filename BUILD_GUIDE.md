# Mintreu BG Remover - Complete Build Guide

**Version:** 1.0.0
**Company:** Mintreu
**Developer:** Krishanu Bhattacharya
**License:** MIT

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Build Methods](#build-methods)
5. [Distribution Types](#distribution-types)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [Deployment](#deployment)

---

## Overview

This project provides **complete offline-capable** distribution builds for the Mintreu BG Remover Tool. The build system creates:

- ✅ **Portable ZIP** with embedded Python (no installation required)
- ✅ **Windows Installer** (Inno Setup)
- ✅ **Single EXE** (PyInstaller)
- ✅ **Offline pip packages** bundle

All distributions are **100% self-contained** and work without internet connection after initial setup.

---

## Prerequisites

### Required Software

1. **Python 3.10 or higher**
   - Download from: https://www.python.org/downloads/
   - Add to PATH during installation

2. **Git** (optional, for version control)
   - Download from: https://git-scm.com/downloads

3. **Inno Setup** (optional, for Windows installer)
   - Download from: https://jrsoftware.org/isinfo.php
   - Only needed if building .exe installer

### System Requirements

- **OS:** Windows 10/11 (64-bit)
- **RAM:** 8GB minimum (16GB recommended for building)
- **Disk:** 5GB free space for build artifacts
- **Internet:** Required for downloading Python embedded and packages

---

## Quick Start

### Method 1: Automated Complete Build (Recommended)

```bash
# 1. Clone or extract the project
cd BgRemover

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the complete build script
python build_complete_offline.py
```

This will:
- Download Python embedded distribution
- Download all required packages for offline use
- Create portable ZIP distribution
- Generate Inno Setup installer script
- Optionally build single EXE

**Output:** All distributions in `distributions/` folder

---

### Method 2: Quick Development Build

For testing during development:

```bash
# 1. Install dependencies
pip install -e .

# 2. Run directly
python main.py
```

---

## Build Methods

### 1. Portable Distribution (Recommended for Users)

**Advantages:**
- ✅ No installation required
- ✅ Fully portable - runs from USB drive
- ✅ Includes embedded Python 3.11
- ✅ All packages pre-downloaded for offline install
- ✅ Can be copied to any Windows machine

**Build Command:**
```bash
python build_complete_offline.py
```

**Output:**
- `distributions/MintreuBgRemover_v1.0.0_Portable.zip`
- Size: ~100-150 MB (without models)

**Contents:**
```
MintreuBgRemover/
├── MintreuBgRemover.bat     (Main launcher)
├── install_dependencies.bat  (Offline installer)
├── main.py                   (Application code)
├── python/                   (Embedded Python 3.11)
├── offline_packages/         (Pre-downloaded packages)
├── models/                   (AI models folder)
├── assets/                   (Icons, resources)
├── LICENSE.txt
└── README.txt
```

**Usage for End Users:**
1. Extract ZIP to any folder
2. Run `MintreuBgRemover.bat`
3. First run: Dependencies auto-install (offline, 2-3 min)
4. Download AI models when prompted (one-time, requires internet)
5. Done! Runs 100% offline after setup

---

### 2. Windows Installer

**Advantages:**
- ✅ Professional installation experience
- ✅ Start menu shortcuts
- ✅ Desktop icon option
- ✅ Proper uninstaller
- ✅ Registry integration

**Build Steps:**

1. Build portable distribution first:
   ```bash
   python build_complete_offline.py
   ```

2. Install Inno Setup from https://jrsoftware.org/isinfo.php

3. Open the generated script:
   ```
   distributions/installer/MintreuBgRemover_installer.iss
   ```

4. In Inno Setup: **Build → Compile**

**Output:**
- `distributions/installer/MintreuBgRemover_v1.0.0_Setup.exe`
- Size: ~100-150 MB

**Features:**
- Silent installation support: `/SILENT` or `/VERYSILENT`
- Custom install directory
- Auto-runs dependency installer
- Creates uninstaller

---

### 3. Single EXE (PyInstaller)

**Advantages:**
- ✅ Single file distribution
- ✅ No visible Python installation
- ✅ Models can be bundled

**Disadvantages:**
- ❌ Larger file size (~300-500 MB with models)
- ❌ Slower startup (extracts to temp)
- ❌ Antivirus false positives possible

**Build Command:**
```bash
# Ensure dependencies installed
pip install -r requirements.txt
pip install pyinstaller

# Build
python installMaker.py --build-type file

# Or use the complete builder
python build_complete_offline.py
# When prompted, choose "y" to build PyInstaller EXE
```

**Output:**
- `distributions/exe/MintreuBgRemover.exe`
- Size: 300-500 MB (depending on bundled content)

---

### 4. Developer Build

For development and testing:

```bash
# Install in development mode
pip install -e .

# Run directly
python main.py

# Or use the batch file
run.bat
```

---

## Distribution Types Comparison

| Feature | Portable ZIP | Installer | Single EXE | Developer |
|---------|-------------|-----------|------------|-----------|
| File Size | ~150 MB | ~150 MB | ~400 MB | - |
| Startup Speed | Fast | Fast | Slow | Fast |
| Installation | Extract | Install | None | None |
| Portable | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| Professional | ✅ | ✅✅ | ⚠️ | ❌ |
| Offline Capable | ✅ | ✅ | ✅ | ❌ |
| Update Friendly | ✅ | ✅ | ❌ | ✅ |
| Recommended For | Most Users | Enterprise | Quick Demo | Development |

---

## Testing

### Pre-Build Testing

Before building distributions, test the application:

```bash
# Run unit tests (if available)
pytest tests/

# Run application in dev mode
python main.py

# Test with sample images
# 1. Add images to test_images/
# 2. Process them
# 3. Check output/ folder
```

### Post-Build Testing

After building, test each distribution:

#### Test Portable ZIP

```bash
# 1. Extract to C:\Temp\TestPortable\
# 2. Run MintreuBgRemover.bat
# 3. Verify dependency installation works
# 4. Test image processing
# 5. Check offline capability (disconnect internet)
```

#### Test Installer

```bash
# 1. Run MintreuBgRemover_v1.0.0_Setup.exe
# 2. Follow installation wizard
# 3. Check Start Menu shortcut
# 4. Run application
# 5. Test uninstaller
```

#### Test Single EXE

```bash
# 1. Copy MintreuBgRemover.exe to clean folder
# 2. Run it
# 3. Test all features
# 4. Check if models bundle works
```

### Testing Checklist

- [ ] Application launches without errors
- [ ] UI loads correctly (dark theme)
- [ ] Can add images via "Add Images" button
- [ ] Can add images via drag & drop
- [ ] Can add folder of images
- [ ] Can download models (internet required)
- [ ] Can process single image
- [ ] Can process batch (multiple images)
- [ ] Output files are created correctly
- [ ] Output files have transparency
- [ ] Can open output folder
- [ ] Can change output directory
- [ ] Image preview works
- [ ] Zoom in/out works in preview
- [ ] Progress bar updates correctly
- [ ] Can stop processing mid-batch
- [ ] Health check runs correctly
- [ ] Logs are created
- [ ] Works offline after setup
- [ ] Tutorial/Help menu works
- [ ] About dialog shows correct version

---

## Troubleshooting

### Build Issues

**Problem:** Python not found
```bash
# Solution: Install Python and add to PATH
# Or use full path
C:\Python311\python.exe build_complete_offline.py
```

**Problem:** pip install fails
```bash
# Solution: Upgrade pip
python -m pip install --upgrade pip

# Install dependencies manually
pip install onnxruntime numpy pillow opencv-python-headless PySide6 requests tqdm
```

**Problem:** PyInstaller build fails
```bash
# Solution: Clean and rebuild
rmdir /s /q build dist
rmdir /s /q __pycache__
python build_complete_offline.py
```

**Problem:** Download fails
```bash
# Solution: Check internet connection
# Or download manually:
# 1. Download from URLs in build script
# 2. Place in build/ folder
# 3. Run build again
```

### Runtime Issues

**Problem:** Application won't start
```
# Check logs
type %USERPROFILE%\.mintreu_bg_remover\app.log

# Run with console to see errors
python main.py
```

**Problem:** Models not found
```
# Download models manually:
# 1. System → Download Models
# 2. Or place model files in models/ folder
```

**Problem:** Slow processing
```
# Reduce worker threads
# Close other applications
# Use faster model
```

---

## Deployment

### For End Users

**Recommended Distribution:** Portable ZIP

1. Build portable distribution
2. Test thoroughly
3. Host on your website or CDN
4. Provide download link
5. Include README and quick start guide

**Example Download Page:**
```html
<h2>Download Mintreu BG Remover v1.0.0</h2>
<ul>
  <li><a href="MintreuBgRemover_v1.0.0_Portable.zip">
    Portable Version (150 MB) - Recommended
  </a></li>
  <li><a href="MintreuBgRemover_v1.0.0_Setup.exe">
    Windows Installer (150 MB)
  </a></li>
</ul>

<h3>Requirements:</h3>
<ul>
  <li>Windows 10/11 (64-bit)</li>
  <li>4GB RAM minimum</li>
  <li>Internet for first-time setup only</li>
</ul>
```

### For Enterprise

**Recommended:** Windows Installer

1. Build installer
2. Test on clean Windows VMs
3. Document system requirements
4. Provide silent install command
5. Include IT deployment guide

**Silent Installation:**
```bash
MintreuBgRemover_v1.0.0_Setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /DIR="C:\Program Files\MintreuBgRemover"
```

### Version Updates

When releasing new version:

1. Update version in:
   - `main.py` → `APP_VERSION`
   - `pyproject.toml` → `version`
   - `build_complete_offline.py` → `APP_VERSION`

2. Update changelog

3. Rebuild all distributions

4. Test all distributions

5. Upload to distribution server

6. Update download links

---

## Advanced Configuration

### Custom Build Options

Edit `build_complete_offline.py`:

```python
# Change Python version
PYTHON_VERSION = "3.11.9"  # Use different version

# Add more packages
REQUIRED_PACKAGES = [
    "onnxruntime>=1.19.0",
    # Add your packages here
]

# Change app name
APP_NAME = "CustomName"
```

### PyInstaller Optimization

For smaller EXE size:

```python
# In installMaker.py, add:
"--exclude-module", "tkinter",
"--exclude-module", "unittest",
"--exclude-module", "test",
```

### Include Custom Models

```python
# Copy models to models/ folder before building
# They will be automatically included in portable ZIP
# For PyInstaller, they're added via --add-data
```

---

## Build Automation

### CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/build.yml`:

```yaml
name: Build Distributions

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Build distributions
      run: python build_complete_offline.py

    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: distributions
        path: distributions/
```

### Batch Build Script

Create `build_all.bat`:

```batch
@echo off
echo Building all distributions...

echo.
echo [1/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Building portable distribution...
python build_complete_offline.py

echo.
echo [3/3] Building PyInstaller EXE...
python installMaker.py --build-type file

echo.
echo All builds complete!
pause
```

---

## Support and Maintenance

### Updating Dependencies

```bash
# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade onnxruntime

# Update all
pip install --upgrade -r requirements.txt

# Freeze new versions
pip freeze > requirements.txt
```

### Model Updates

To update the AI model:

1. Find new model URL
2. Update `MODELS` dict in `main.py`
3. Test model loads and works
4. Rebuild distributions

### License and Credits

This build system is part of the Mintreu BG Remover Tool.

- **Company:** Mintreu
- **Developer:** Krishanu Bhattacharya
- **Website:** https://mintreu.com
- **License:** MIT

**Dependencies:**
- Python 3.11
- PySide6 (Qt for Python)
- ONNX Runtime
- OpenCV
- Pillow
- NumPy

**AI Model:**
- RMBG v1.4 by BRIA AI (Hugging Face)

---

## Frequently Asked Questions

### Q: Why is the portable ZIP so large?
**A:** It includes Python 3.11 embedded (~50 MB) plus all dependencies (~100 MB). This makes it fully self-contained.

### Q: Can I reduce the EXE size?
**A:** Yes, exclude unused modules in PyInstaller spec. See Advanced Configuration section.

### Q: Does it work on Windows 7?
**A:** No, requires Windows 10 or newer. Python 3.11+ doesn't support Windows 7.

### Q: Can I build for Linux/Mac?
**A:** The build scripts are Windows-specific. For Linux/Mac, use standard Python packaging or modify the build scripts.

### Q: How do I update the application?
**A:** For portable: Extract new version. For installer: Run new installer (auto-uninstalls old version).

### Q: Can users install without admin rights?
**A:** Yes! The portable version works without admin rights. Installer may require admin for Program Files installation.

### Q: How do I include pre-downloaded models?
**A:** Place model files in `models/` folder before building. They'll be included automatically.

---

## Changelog

### Version 1.0.0 (2025-01-XX)
- ✅ Initial production release
- ✅ Complete offline capability
- ✅ Portable distribution
- ✅ Windows installer
- ✅ Single EXE option
- ✅ Dark mode UI
- ✅ Batch processing
- ✅ Auto-dependency installation
- ✅ Enterprise-grade build system

---

**End of Build Guide**

For support: contact@mintreu.com
For updates: https://mintreu.com
