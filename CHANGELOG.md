# Changelog

All notable changes to Mintreu BG Remover will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-01-XX

### Added

#### Core Features
- ✨ AI-powered background removal using RMBG v1.4 model
- ✨ Batch processing with multi-threading support
- ✨ Drag & drop interface for files and folders
- ✨ Image preview with zoom functionality
- ✨ Progress tracking for individual files and batch operations
- ✨ Configurable output directory
- ✨ Multiple image format support (PNG, JPG, JPEG, WEBP, BMP, TIFF)
- ✨ Auto-save with transparency preserved

#### UI/UX
- 🎨 Professional dark mode theme
- 🎨 Modern gradient buttons and styling
- 🎨 Rich file information display (size, resolution, format)
- 🎨 Interactive image viewer with pan and zoom
- 🎨 Splash screen with branding
- 🎨 Menu bar with Help, System, and About sections
- 🎨 Status bar with real-time information
- 🎨 Tooltips and keyboard shortcuts

#### System Features
- 🔧 System health check on startup
- 🔧 Auto-repair for missing directories
- 🔧 Model auto-download from Hugging Face
- 🔧 Offline capability (after initial setup)
- 🔧 Configuration persistence
- 🔧 Comprehensive logging
- 🔧 Error handling and recovery

#### Distribution
- 📦 Portable ZIP with embedded Python 3.11
- 📦 Windows Installer (Inno Setup)
- 📦 Single EXE option (PyInstaller)
- 📦 Offline pip packages bundle
- 📦 Self-contained distributions
- 📦 No admin rights required (portable version)

#### Documentation
- 📚 Comprehensive README with quick start
- 📚 Detailed BUILD_GUIDE for developers
- 📚 DEPLOYMENT guide for various scenarios
- 📚 In-app tutorial and help system
- 📚 License information dialog
- 📚 System health report

#### Build System
- 🛠️ Automated build script for all distribution types
- 🛠️ Python embedded download and configuration
- 🛠️ Offline package downloader
- 🛠️ PyInstaller spec generator
- 🛠️ Inno Setup script generator
- 🛠️ Build verification and testing

#### Testing
- ✅ Comprehensive test suite (test_application.py)
- ✅ Import verification
- ✅ Path validation
- ✅ Configuration tests
- ✅ Model verification
- ✅ System health checks
- ✅ Image processing tests
- ✅ UI component tests
- ✅ Integration tests
- ✅ Test runner batch script

### Technical Specifications

#### Dependencies
- Python 3.10+ (embedded 3.11 in portable)
- PySide6 >= 6.6.0
- ONNX Runtime >= 1.19.0
- NumPy >= 1.24.0, < 2.0.0
- Pillow >= 10.0.0
- OpenCV-python-headless >= 4.8.0
- Requests >= 2.31.0
- tqdm >= 4.66.0

#### AI Model
- Model: RMBG v1.4 by BRIA AI
- Format: ONNX
- Size: 176 MB
- Input: RGB images (any resolution)
- Output: Alpha masks (transparency)
- Performance: ~1-2 seconds per image (CPU)

#### System Requirements
- OS: Windows 10/11 (64-bit)
- RAM: 4GB minimum, 8GB recommended
- Disk: 500MB minimum
- Internet: One-time for model download

### Performance
- Startup time: 2-3 seconds
- Processing speed: 1-2 images/second (CPU, depends on resolution)
- Memory usage: 500MB-1GB during processing
- Multi-threading: Configurable workers (default: CPU cores - 1)

### Security
- No telemetry or tracking
- No internet required after setup
- All processing local
- Open source (MIT License)
- No external API calls

### Known Limitations
- Windows only (current version)
- CPU processing only (no GPU acceleration yet)
- Model download requires internet (one-time)
- Large images (>4K) may be slow on low-end CPUs

---

## [Unreleased]

### Planned for 1.1.0
- GPU acceleration support (CUDA, DirectML)
- Additional AI models (U2Net, MODNet)
- Batch folder monitoring
- Command-line interface
- Performance optimizations
- Memory usage improvements

### Planned for 1.2.0
- macOS support
- Linux support
- API server mode
- Web-based UI option
- Auto-update mechanism

### Planned for 2.0.0
- Cloud sync (optional)
- Plugin system
- Custom model training
- Advanced editing tools
- Multi-language support

---

## Version History

### Version Numbering

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
  - **MAJOR:** Breaking changes, major redesigns
  - **MINOR:** New features, backward compatible
  - **PATCH:** Bug fixes, minor improvements

### Release Tags

Git tags follow the format `v{MAJOR}.{MINOR}.{PATCH}`

Example:
```bash
git tag -a v1.0.0 -m "Initial production release"
git push origin v1.0.0
```

---

## Migration Guide

### From Pre-release to 1.0.0

If upgrading from a pre-release version:

1. **Backup your data:**
   ```bash
   # Backup output folder
   xcopy /E /I output output_backup
   ```

2. **Uninstall old version** (if using installer)

3. **Install 1.0.0** using preferred method

4. **Models:** Old models are compatible, will auto-detect

5. **Config:** Settings will reset to defaults (config location changed)

---

## Contributing

To contribute to this changelog:

1. Follow [Keep a Changelog](https://keepachangelog.com/) format
2. Use these categories:
   - **Added** for new features
   - **Changed** for changes in existing functionality
   - **Deprecated** for soon-to-be removed features
   - **Removed** for now removed features
   - **Fixed** for any bug fixes
   - **Security** for vulnerability fixes

3. Add entries under `[Unreleased]` section
4. On release, move to new version section with date

---

## Support

For issues, questions, or suggestions:

- **Email:** contact@mintreu.com
- **Website:** https://mintreu.com
- **GitHub:** (if public repo)

---

**Project:** Mintreu BG Remover
**Developer:** Krishanu Bhattacharya
**Company:** Mintreu
**License:** MIT
