# Mintreu BG Remover - Auto-Update System

## ✅ Complete! Auto-Update Feature Added

Your application now has a **professional auto-update system** that checks for updates from `mintreu.com` and handles updates intelligently based on installation type.

---

## 🎯 Features Implemented

### ✅ **Automatic Update Checking**
- Background check on application startup
- Non-blocking, silent check
- Manual check via "System → Check for Updates" menu

### ✅ **Smart Update Handling**

#### For **Installed Version** (via Windows Installer):
- **Silent auto-update** in background
- Downloads installer automatically
- Installs with `/VERYSILENT` flag
- Restarts application after update
- Zero user intervention required (if enabled)

#### For **Portable Version**:
- **Download notification** with changelog
- Downloads new portable ZIP to Downloads folder
- Opens Downloads folder automatically
- User extracts and runs new version

### ✅ **Update API Integration**
- Checks `https://mintreu.com/api/bg-remover/version.json`
- Fallback URLs for high availability
- Timeout handling
- Error recovery

---

## 📁 Files Created

### 1. `updater.py` (500+ lines)
Complete update system with:
- `UpdateChecker` - Checks for updates from server
- `InstalledUpdater` - Handles silent updates for installed version
- `PortableUpdater` - Handles downloads for portable version
- `UpdateManager` - Main coordinator
- `BackgroundUpdateChecker` - Background thread checker
- Version comparison logic
- Download progress tracking
- Installation detection

### 2. `API_UPDATE_DOCUMENTATION.md`
Complete API documentation including:
- API endpoint specification
- JSON response format
- Implementation examples (PHP, Node.js, Python)
- Security considerations
- Testing instructions
- Deployment checklist

### 3. `version.json.example`
Sample version file to upload to server

### 4. Updated `main.py`
Integrated update system into main application:
- Import updater module
- Initialize UpdateManager
- Background update check on startup
- Menu item "Check for Updates"
- Update notification dialogs
- Download progress for portable version

---

## 🚀 How It Works

### On Application Startup

```
1. Application starts
2. Background thread checks mintreu.com API
3. If update available:
   - Installed version: Shows "Update Available" dialog
   - Portable version: Shows "Download New Version" dialog
4. User can choose to update now or later
```

### For Installed Version

```
User clicks "Install Now"
  ↓
Downloads installer from mintreu.com
  ↓
Runs installer with /VERYSILENT flag
  ↓
Application exits
  ↓
Installer updates application
  ↓
Application auto-restarts
```

### For Portable Version

```
User clicks "Download"
  ↓
Downloads portable ZIP from mintreu.com
  ↓
Saves to Downloads folder
  ↓
Opens Downloads folder
  ↓
User extracts new version manually
```

---

## 🌐 Server Setup Required

To enable auto-updates, you need to host a JSON file at:

```
https://mintreu.com/api/bg-remover/version.json
```

### Step 1: Create version.json

Use the provided `version.json.example` as template:

```json
{
  "version": "1.0.0",
  "release_date": "2025-01-01",
  "download_url_installer": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.0.0_Setup.exe",
  "download_url_portable": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.0.0_Portable.zip",
  "changelog": "Initial release with AI background removal",
  "critical": false,
  "min_version": "0.0.0"
}
```

### Step 2: Upload to Server

```bash
# Upload version.json
scp version.json user@mintreu.com:/var/www/mintreu.com/api/bg-remover/

# Upload distribution files
scp MintreuBgRemover_v1.0.0_Setup.exe user@mintreu.com:/var/www/mintreu.com/downloads/bg-remover/
scp MintreuBgRemover_v1.0.0_Portable.zip user@mintreu.com:/var/www/mintreu.com/downloads/bg-remover/
```

### Step 3: Test

```bash
# Test API endpoint
curl https://mintreu.com/api/bg-remover/version.json

# Test in application
# 1. Launch application
# 2. Go to System → Check for Updates
# 3. Should show "No updates" if server has same version
```

---

## 📝 When Releasing New Version

### 1. Build New Version

```bash
# Update version in main.py
APP_VERSION = "1.1.0"

# Build distributions
python build_complete_offline.py
```

### 2. Upload Distribution Files

```bash
# Upload to server
scp distributions/installer/MintreuBgRemover_v1.1.0_Setup.exe \
    user@mintreu.com:/var/www/mintreu.com/downloads/bg-remover/

scp distributions/MintreuBgRemover_v1.1.0_Portable.zip \
    user@mintreu.com:/var/www/mintreu.com/downloads/bg-remover/
```

### 3. Update version.json

```json
{
  "version": "1.1.0",
  "release_date": "2025-02-01",
  "download_url_installer": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.1.0_Setup.exe",
  "download_url_portable": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.1.0_Portable.zip",
  "changelog": "- Added GPU acceleration\n- Improved speed by 50%\n- Bug fixes",
  "critical": false
}
```

### 4. Upload Updated version.json

```bash
scp version.json user@mintreu.com:/var/www/mintreu.com/api/bg-remover/
```

### 5. Done!

All users will see update notification on next application startup or manual check.

---

## 🔧 Configuration Options

### Update Check URL

Default: `https://mintreu.com/api/bg-remover/version.json`

To change, edit `updater.py`:

```python
UPDATE_CHECK_URL = "https://your-domain.com/api/version.json"
```

### Fallback URLs

Edit in `updater.py`:

```python
FALLBACK_URLS = [
    "https://updates.your-domain.com/version.json",
    "https://cdn.your-domain.com/version.json"
]
```

### Timeouts

```python
UPDATE_CHECK_TIMEOUT = 10  # seconds for version check
DOWNLOAD_TIMEOUT = 300      # seconds for downloading updates
```

---

## 🧪 Testing

### Test Update Checker

```bash
# Run updater tests
python updater.py

# Output:
# Testing Mintreu BG Remover Update System
# [1] Testing version comparison... ✓
# [2] Testing update checker... ✓
# [3] Testing installation detection... ✓
```

### Test in Application

1. **Launch application**
2. **Check menu:** "System → Check for Updates"
3. **Click it**
4. **Expected behaviors:**
   - If no server: "Could not check for updates"
   - If same version: "You are running the latest version"
   - If newer version: Shows update dialog

---

## 📊 Update Flow Diagrams

### Installed Version Update Flow

```
┌─────────────────┐
│ App Starts      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Background      │
│ Update Check    │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Update? │
    └────┬────┘
         │ Yes
         ▼
┌─────────────────┐
│ Show Dialog:    │
│ "Update to 1.1" │
│ [Now] [Later]   │
└────────┬────────┘
         │ Now
         ▼
┌─────────────────┐
│ Download        │
│ Installer       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Run Installer   │
│ /VERYSILENT     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ App Exits       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Installer       │
│ Updates App     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ App Restarts    │
│ (Updated!)      │
└─────────────────┘
```

### Portable Version Update Flow

```
┌─────────────────┐
│ App Starts      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Background      │
│ Update Check    │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Update? │
    └────┬────┘
         │ Yes
         ▼
┌─────────────────┐
│ Show Dialog:    │
│ "New v1.1"      │
│ [Download][Later│
└────────┬────────┘
         │ Download
         ▼
┌─────────────────┐
│ Download ZIP    │
│ to Downloads/   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Open Downloads  │
│ Folder          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ User Extracts   │
│ & Runs New Ver  │
└─────────────────┘
```

---

## 🛡️ Security Features

### ✅ HTTPS Required
All update checks and downloads use HTTPS to prevent MITM attacks.

### ✅ Version Validation
Semantic versioning ensures only newer versions trigger updates.

### ✅ Silent Errors
Failed update checks don't interrupt user workflow.

### ✅ Fallback URLs
Multiple update servers for high availability.

### ✅ Timeout Protection
Network timeouts prevent hanging.

---

## 🐛 Troubleshooting

### Update Check Fails

**Problem:** "Could not check for updates"

**Solutions:**
1. Check internet connection
2. Verify server is online: `curl https://mintreu.com/api/bg-remover/version.json`
3. Check firewall isn't blocking
4. Verify HTTPS certificate is valid

---

### Download Fails

**Problem:** "Failed to download update"

**Solutions:**
1. Check download URLs are correct
2. Verify files exist on server
3. Check sufficient disk space
4. Try manual download from provided URL

---

### Installed Version Won't Update

**Problem:** Silent update doesn't work

**Solutions:**
1. Check user has permissions to run installer
2. Verify installer flags are correct
3. Try manual update
4. Check logs: `%USERPROFILE%\.mintreu_bg_remover\app.log`

---

## 📚 Documentation Files

1. **API_UPDATE_DOCUMENTATION.md** - Complete API specification
2. **version.json.example** - Sample version file
3. **AUTO_UPDATE_README.md** - This file
4. **updater.py** - Update system code
5. **main.py** - Integration with application

---

## ✅ Deployment Checklist

Server Setup:
- [ ] Create version.json file
- [ ] Upload to https://mintreu.com/api/bg-remover/version.json
- [ ] Verify HTTPS works
- [ ] Test endpoint returns valid JSON
- [ ] Upload distribution files to downloads/
- [ ] Verify download URLs work
- [ ] Set up fallback URLs (optional)
- [ ] Configure caching headers
- [ ] Set up monitoring

Application:
- [ ] Update version in main.py
- [ ] Build distributions
- [ ] Test update check locally
- [ ] Test on clean machine
- [ ] Verify portable version shows download option
- [ ] Verify installed version can auto-update

---

## 🎉 Summary

Your application now has a **production-ready auto-update system** that:

✅ Checks for updates automatically
✅ Handles installed vs portable versions intelligently
✅ Downloads and installs updates silently (installed version)
✅ Guides users through manual update (portable version)
✅ Provides fallback mechanisms
✅ Includes comprehensive documentation

**Next Steps:**
1. Set up the API endpoint on mintreu.com
2. Upload initial version.json
3. Test with a fake newer version
4. Deploy to production

---

**Questions?**

- Read: `API_UPDATE_DOCUMENTATION.md`
- Email: contact@mintreu.com
- Website: https://mintreu.com

---

**Auto-Update System v1.0.0**
**Author:** Krishanu Bhattacharya
**Company:** Mintreu
