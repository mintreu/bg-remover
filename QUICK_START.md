# Mintreu BG Remover - Quick Start Guide

**Get started in 5 minutes!**

---

## For End Users (I just want to use the app)

### Step 1: Build the Portable Version

Open Command Prompt in the project folder and run:

```batch
python build_complete_offline.py
```

**What happens:**
- Downloads Python 3.11 embedded (~5 minutes)
- Downloads all required packages (~5 minutes)
- Creates portable ZIP (~2 minutes)
- **Total time: ~10-15 minutes**

**Output:** `distributions/MintreuBgRemover_v1.0.0_Portable.zip`

---

### Step 2: Extract and Run

1. Extract the ZIP file to any folder (e.g., `C:\Apps\MintreuBgRemover`)
2. Double-click `MintreuBgRemover.bat`
3. **First run:** Dependencies will auto-install (2-3 minutes, offline)
4. **Download models** when prompted (one-time, 176 MB)
5. **Done!** Start removing backgrounds

---

### Step 3: Use the Application

1. **Add images:**
   - Click "Add Images" button
   - Or drag & drop files/folders

2. **Configure:**
   - Select model: RMBG v1.4 (default)
   - Adjust workers: More = faster

3. **Process:**
   - Click "Start Processing"
   - Wait for completion

4. **Get results:**
   - Click "Open Output Folder"
   - Find your images with backgrounds removed (PNG with transparency)

---

## For Developers (I want to modify the code)

### Step 1: Setup Environment

```batch
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 2: Run Application

```batch
# Option 1: Direct run
python main.py

# Option 2: Use batch file
run.bat
```

---

### Step 3: Make Changes

Edit `main.py` and run again. Changes are immediate!

---

### Step 4: Test Your Changes

```batch
# Run test suite
python test_application.py

# Or use the test runner
run_tests.bat
```

---

### Step 5: Build Distribution

```batch
# Build everything
python build_complete_offline.py

# Or just PyInstaller EXE
python installMaker.py --build-type file
```

---

## For IT Administrators (I need to deploy this)

### Silent Installation

1. Build the installer (see DEPLOYMENT.md)

2. Deploy with Group Policy or SCCM:

```batch
MintreuBgRemover_v1.0.0_Setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART
```

3. Pre-configure settings by placing `config.json` in:
   ```
   %USERPROFILE%\.mintreu_bg_remover\config.json
   ```

---

### Network Deployment

1. Extract portable version to network share:
   ```
   \\server\apps\MintreuBgRemover\
   ```

2. Create shortcut on user desktops:
   ```
   Target: \\server\apps\MintreuBgRemover\MintreuBgRemover.bat
   ```

3. Users run from network (no local installation needed)

---

## Troubleshooting (Common Issues)

### Issue: Application won't start

**Solution:**
```batch
# Run in console mode to see errors
cd MintreuBgRemover
python\python.exe main.py
```

Check logs at: `%USERPROFILE%\.mintreu_bg_remover\app.log`

---

### Issue: Models not found

**Solution:**
1. Open application
2. Go to **System → Download Models**
3. Click **Download Models**
4. Wait for download to complete

---

### Issue: Slow processing

**Solution:**
- Reduce worker threads in settings
- Close other applications
- Process smaller batches
- Use faster computer

---

### Issue: Dependencies won't install

**Solution:**
```batch
# Manually run installer
cd MintreuBgRemover
install_dependencies.bat

# Check for errors in output
```

---

## Next Steps

### Just Using the App?

- Read the **Tutorial** in Help menu (F1)
- Check **README.md** for full features
- Visit https://mintreu.com for support

---

### Developing?

- Read **BUILD_GUIDE.md** for detailed build instructions
- Read **DEPLOYMENT.md** for deployment strategies
- Run `python test_application.py` before committing changes

---

### Deploying?

- Read **DEPLOYMENT.md** for enterprise deployment
- Test on clean Windows VMs first
- Plan rollout strategy
- Set up support channels

---

## Quick Reference

### File Locations

| Item | Location |
|------|----------|
| Application | `main.py` |
| Build Script | `build_complete_offline.py` |
| Test Suite | `test_application.py` |
| Config | `%USERPROFILE%\.mintreu_bg_remover\config.json` |
| Logs | `%USERPROFILE%\.mintreu_bg_remover\app.log` |
| Output | `output/` (or custom location) |
| Models | `models/` |

---

### Commands

```batch
# Run application (development)
python main.py

# Build portable distribution
python build_complete_offline.py

# Run tests
python test_application.py

# Install dependencies (manual)
pip install -r requirements.txt
```

---

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| F1 | Open tutorial |
| Ctrl+O | Add images |
| Ctrl+L | Clear list |
| Ctrl+P | Start/Stop processing |

---

## Support

**Need Help?**

- **Email:** contact@mintreu.com
- **Website:** https://mintreu.com
- **Logs:** Check `%USERPROFILE%\.mintreu_bg_remover\app.log`

---

## Version Information

- **Current Version:** 1.0.0
- **Python Required:** 3.10+ (or use portable with embedded Python)
- **Platform:** Windows 10/11 (64-bit)
- **License:** MIT

---

**That's it! You're ready to go!**

For more details, see:
- **README.md** - Full documentation
- **BUILD_GUIDE.md** - Detailed build instructions
- **DEPLOYMENT.md** - Deployment strategies
- **CHANGELOG.md** - Version history

---

**Mintreu BG Remover**
Made with ❤️ by Krishanu Bhattacharya
https://mintreu.com
