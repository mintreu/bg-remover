# Mintreu BG Remover

**Enterprise-Grade AI Background Removal Tool**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

---

## 🌟 Features

✅ **100% Offline Capable** - Works without internet after initial setup
✅ **AI-Powered** - Uses RMBG v1.4 state-of-the-art model
✅ **Batch Processing** - Process multiple images simultaneously
✅ **Dark Mode UI** - Professional, modern interface
✅ **Drag & Drop** - Easy to use interface
✅ **Portable** - No installation required (portable version)
✅ **Multi-threaded** - Fast parallel processing
✅ **Image Preview** - View and zoom images before processing
✅ **Format Support** - PNG, JPG, JPEG, WEBP, BMP, TIFF
✅ **Self-Contained** - Includes embedded Python and all dependencies

---

## 📸 Screenshots

```
┌─────────────────────────────────────────────────────────────┐
│  🎨 Mintreu BG Remover Tool                                │
├─────────────────────────────────────────────────────────────┤
│  ⚙️ Settings                                               │
│  Model: RMBG v1.4 (Fast & Accurate)  Workers: 7           │
│                                                             │
│  📁 Add Images   📂 Add Folder   🗑️ Clear                 │
│                                                             │
│  💡 Drag & drop images or folders here                     │
│                                                             │
│  ┌───────────────────────────────┐  ┌──────────────────┐  │
│  │  📄 File List                 │  │  🖼️ Preview      │  │
│  │                               │  │                  │  │
│  │  🖼️ image1.jpg               │  │                  │  │
│  │  📊 2.5 MB • 1920x1080 • JPG │  │                  │  │
│  │                               │  │                  │  │
│  │  ✅ image2.png               │  │                  │  │
│  │  📊 1.8 MB • 1280x720 • PNG  │  │                  │  │
│  └───────────────────────────────┘  └──────────────────┘  │
│                                                             │
│  ▶️ Start Processing      📂 Open Output Folder           │
│                                                             │
│  Mintreu © 2025 | Developed by Krishanu Bhattacharya      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### For End Users

1. **Download** the portable version (150 MB)
2. **Extract** to any folder
3. **Run** `MintreuBgRemover.bat`
4. **First time**: Dependencies auto-install (2-3 minutes, offline)
5. **Download** AI models when prompted (one-time, requires internet)
6. **Done!** Start removing backgrounds

### For Developers

```bash
# Clone repository
git clone https://github.com/yourorg/mintreu-bg-remover.git
cd mintreu-bg-remover

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

---

## 📦 Distribution Options

### 1. Portable ZIP (Recommended)

- **No installation required**
- **Fully portable** - Run from USB drive
- **Includes embedded Python 3.11**
- **All packages pre-downloaded**
- **Size:** ~150 MB (without models)

**Download:** `MintreuBgRemover_v1.0.0_Portable.zip`

### 2. Windows Installer

- **Professional installation**
- **Start menu shortcuts**
- **Desktop icon option**
- **Proper uninstaller**
- **Size:** ~150 MB

**Download:** `MintreuBgRemover_v1.0.0_Setup.exe`

### 3. Single EXE (Optional)

- **Single file distribution**
- **No visible Python**
- **Slower startup**
- **Size:** ~400 MB

---

## 💻 System Requirements

### Minimum

- **OS:** Windows 10 (64-bit)
- **RAM:** 4GB
- **Disk:** 500MB free space
- **Internet:** One-time for model download

### Recommended

- **OS:** Windows 11 (64-bit)
- **RAM:** 8GB+
- **Disk:** 2GB free space
- **CPU:** Multi-core processor

---

## 🎯 Usage

### Basic Workflow

1. **Launch** the application
2. **Add Images:**
   - Click "Add Images" button
   - Or drag & drop files
   - Or add entire folder
3. **Select Model:** RMBG v1.4 (default)
4. **Adjust Workers:** More = faster (uses more CPU)
5. **Click** "Start Processing"
6. **Wait** for completion
7. **Open Output Folder** to see results

### Tips & Tricks

- **Batch Processing:** Add multiple images for faster overall processing
- **Image Preview:** Click any image in list to preview
- **Zoom:** Use mouse wheel to zoom in preview
- **Output Location:** Click 📁 icon to change output folder
- **Offline Use:** After first setup, no internet required
- **Models:** Download once, use forever offline

---

## 🛠️ Building from Source

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- 5GB free disk space (for build artifacts)

### Build Portable Distribution

```bash
# Install dependencies
pip install -r requirements.txt

# Build portable distribution
python build_complete_offline.py

# Output: distributions/MintreuBgRemover_v1.0.0_Portable.zip
```

### Build Windows Installer

```bash
# 1. Build portable distribution first
python build_complete_offline.py

# 2. Install Inno Setup from https://jrsoftware.org/isinfo.php

# 3. Open generated script
distributions/installer/MintreuBgRemover_installer.iss

# 4. In Inno Setup: Build → Compile
```

### Build Single EXE

```bash
# Install PyInstaller
pip install pyinstaller

# Build
python installMaker.py --build-type file

# Output: dist/MintreuBgRemover.exe
```

For detailed build instructions, see [BUILD_GUIDE.md](BUILD_GUIDE.md)

---

## 🧪 Testing

Run the test suite to verify everything works:

```bash
# Run all tests
python test_application.py

# Output shows:
# ✅ Imports test
# ✅ Paths test
# ✅ Configuration test
# ✅ Models test
# ✅ System health test
# ✅ Image processing test
# ✅ UI components test
# ✅ Build scripts test
# ✅ Integration test
```

---

## 📁 Project Structure

```
BgRemover/
├── main.py                          # Main application
├── build_complete_offline.py        # Complete build system
├── installMaker.py                  # PyInstaller builder
├── test_application.py              # Test suite
├── run.bat                          # Quick run script
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project metadata
├── LICENSE.txt                      # MIT License
├── README.md                        # This file
├── BUILD_GUIDE.md                   # Detailed build guide
│
├── assets/                          # Application assets
│   └── favicon.ico                  # Application icon
│
├── models/                          # AI models (auto-download)
│   └── rmbg_v14.onnx               # RMBG v1.4 model (176 MB)
│
├── hooks/                           # PyInstaller hooks
│   └── hook-onnxruntime.py         # ONNX Runtime hook
│
├── output/                          # Processed images (created at runtime)
├── cache/                           # Application cache (created at runtime)
│
├── venv/                            # Virtual environment (dev only)
│
├── build/                           # Build artifacts (generated)
└── distributions/                   # Distribution files (generated)
    ├── portable/                    # Portable ZIP contents
    ├── installer/                   # Inno Setup scripts
    ├── exe/                         # Single EXE
    └── offline_packages/            # Pre-downloaded packages
```

---

## 🔧 Configuration

### Model Configuration

Edit `main.py` to add or modify models:

```python
MODELS = {
    "rmbg_v14": ModelConfig(
        name="RMBG v1.4 (Fast & Accurate)",
        filename="rmbg_v14.onnx",
        description="Production-ready, fast processing",
        model_type="bg_removal",
        size_mb=176,
        download_url="https://huggingface.co/..."
    ),
}
```

### UI Theme

Customize colors in `main.py`:

```python
class DarkTheme:
    BG_DARK = "#0a0e27"
    PRIMARY = "#667eea"
    SUCCESS = "#10b981"
    # ... more colors
```

### Output Settings

Default output location: `%PROJECT_DIR%/output/`

To change, use the 📁 button in the UI or edit `Config` class.

---

## 🐛 Troubleshooting

### Application Won't Start

```bash
# Check logs
type %USERPROFILE%\.mintreu_bg_remover\app.log

# Run with console to see errors
python main.py
```

### Models Not Found

1. Go to **System → Download Models**
2. Click **Download Models**
3. Wait for download to complete
4. Restart application

### Slow Processing

- Reduce number of worker threads
- Close other applications
- Process fewer images at once
- Use SSD instead of HDD

### Installation Failed

```bash
# Manually install dependencies
cd BgRemover
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Antivirus False Positive

Some antivirus software may flag the EXE as suspicious:

- This is a false positive (common with PyInstaller)
- Use portable ZIP version instead
- Add exception in your antivirus
- Build from source to verify authenticity

---

## 📋 Technical Details

### Technologies Used

- **Language:** Python 3.11
- **UI Framework:** PySide6 (Qt for Python)
- **AI Model:** RMBG v1.4 (ONNX)
- **Image Processing:** OpenCV, Pillow
- **Numerical Computing:** NumPy
- **Build Tools:** PyInstaller, Inno Setup

### Model Details

- **Name:** RMBG v1.4
- **Source:** BRIA AI (Hugging Face)
- **Format:** ONNX
- **Size:** 176 MB
- **Input:** RGB images
- **Output:** Alpha masks
- **Performance:** ~1-2 seconds per image (CPU)

### Performance Metrics

- **Startup Time:** ~2-3 seconds
- **Processing Speed:** 1-2 images/second (CPU)
- **Memory Usage:** 500MB-1GB
- **Disk Usage:** 500MB base + images

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run test suite
6. Submit pull request

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourorg/mintreu-bg-remover.git
cd mintreu-bg-remover

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies + dev tools
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
python test_application.py

# Format code
black main.py

# Run linter
flake8 main.py
```

---

## 📜 License

**MIT License**

Copyright (c) 2025 Mintreu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 👤 Author

**Krishanu Bhattacharya**

- Company: [Mintreu](https://mintreu.com)
- Email: contact@mintreu.com
- Website: https://mintreu.com

---

## 🙏 Acknowledgments

- **BRIA AI** for the RMBG v1.4 model
- **PySide6** for the UI framework
- **ONNX Runtime** for model inference
- **OpenCV** for image processing
- **Python Community** for excellent tools

---

## 📞 Support

- **Website:** https://mintreu.com
- **Email:** contact@mintreu.com
- **Issues:** GitHub Issues (if public repo)
- **Logs:** `%USERPROFILE%\.mintreu_bg_remover\app.log`

---

## 🗺️ Roadmap

### Version 1.1.0 (Planned)

- [ ] GPU acceleration support
- [ ] Additional AI models
- [ ] Batch folder monitoring
- [ ] API server mode
- [ ] Command-line interface
- [ ] macOS support
- [ ] Linux support

### Version 2.0.0 (Future)

- [ ] Web-based UI option
- [ ] Cloud sync
- [ ] Plugins system
- [ ] Custom model training
- [ ] Advanced editing tools

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

## 📈 Changelog

### Version 1.0.0 (2025-01-XX)

**Initial Production Release**

✅ Complete background removal with AI
✅ Dark mode UI with professional design
✅ Batch processing with multi-threading
✅ Drag & drop support
✅ Image preview with zoom
✅ System health check
✅ Model auto-download
✅ 100% offline-capable
✅ Portable distribution
✅ Windows installer
✅ Single EXE option
✅ Comprehensive documentation
✅ Full test suite
✅ Enterprise-grade build system

---

**Thank you for using Mintreu BG Remover!**

Made with ❤️ by Krishanu Bhattacharya at Mintreu
