# ✅ Configuration System Complete!

## What Was Added

Your Mintreu BG Remover now has a **complete configuration system** using `config.ini` file that allows you to customize all URLs and settings **without editing code**.

---

## 📁 Files Created

### 1. **`config.ini`** - Main Configuration File
- All settings in one place
- Easy to edit with any text editor
- Included in all distributions
- Can be customized before/after installation

### 2. **`config_loader.py`** - Configuration Loader Module
- Loads settings from config.ini
- Provides defaults if file not found
- Type-safe property accessors
- Can be tested independently

### 3. **`CONFIG_GUIDE.md`** - Complete Documentation
- How to edit configuration
- All settings explained
- Common scenarios
- Troubleshooting guide

---

## 🎯 Key Features

### ✅ **Easy URL Configuration**

```ini
[UPDATE]
# Simply change this URL to your own domain!
update_check_url = https://mintreu.com/api/bg-remover/version.json

# Or use your custom server
update_check_url = https://your-domain.com/api/version.json
```

### ✅ **Multiple Fallback URLs**

```ini
[UPDATE]
fallback_urls = https://backup1.com/version.json,https://backup2.com/version.json
```

### ✅ **Flexible Configuration Locations**

The app searches for `config.ini` in:
1. Application directory (portable/installed)
2. User home: `%USERPROFILE%\.mintreu_bg_remover\`
3. Current working directory

### ✅ **No Code Changes Required**

Just edit `config.ini` and restart the app!

---

## 📝 How to Use

### For End Users (Portable)

1. **Extract ZIP** file
2. **Open config.ini** in Notepad
3. **Change URLs** if needed:
   ```ini
   [UPDATE]
   update_check_url = https://your-url.com/version.json
   ```
4. **Save** and close
5. **Run** the application

### For Administrators (Installed)

**Option 1: Pre-configure before deployment**

1. Edit `config.ini` before building installer
2. Build distributions with your settings
3. Deploy to users

**Option 2: Post-installation configuration**

1. Navigate to install directory
2. Edit `config.ini`
3. Restart application

**Option 3: User-specific config**

Create config in user folder:
```
%USERPROFILE%\.mintreu_bg_remover\config.ini
```

---

## 🌐 Changing Update URL

### Quick Change

Edit `config.ini`:

```ini
[UPDATE]
# Change from:
update_check_url = https://mintreu.com/api/bg-remover/version.json

# To your URL:
update_check_url = https://your-company.com/api/version.json
```

### Full Corporate Setup

```ini
[UPDATE]
update_check_url = https://updates.company.com/bg-remover/version.json
fallback_urls = https://backup.company.com/bg-remover/version.json
download_base_url = https://downloads.company.com/bg-remover

[APPLICATION]
company_name = Your Company Name
company_website = https://your-company.com
support_email = support@your-company.com
```

---

## 🔧 All Configurable Settings

### Update System
- ✅ Update check URL
- ✅ Fallback URLs
- ✅ Check timeout
- ✅ Download timeout
- ✅ Auto-check on startup
- ✅ Background checking

### Downloads
- ✅ Base download URL
- ✅ Custom download folder

### Application
- ✅ App name
- ✅ Company name
- ✅ Website URL
- ✅ Support email
- ✅ Support URL

### Models
- ✅ Model download URL
- ✅ Auto-download setting

### Logging
- ✅ Log level (DEBUG/INFO/WARNING/ERROR)
- ✅ Enable file logging
- ✅ Custom log location

### Advanced
- ✅ Worker threads
- ✅ GPU acceleration
- ✅ Cache directory
- ✅ Output directory

---

## 📂 File Locations

### Config File Search Order

```
1. C:\YourApp\config.ini                    (app directory)
2. C:\Users\You\.mintreu_bg_remover\config.ini  (user directory)
3. C:\CurrentDir\config.ini                 (working directory)
```

### Default Locations

| Item | Location |
|------|----------|
| Config | `[app]\config.ini` |
| Logs | `%USERPROFILE%\.mintreu_bg_remover\app.log` |
| Cache | `[app]\cache\` |
| Output | `[app]\output\` |
| Models | `[app]\models\` |

---

## 🚀 Deployment Scenarios

### Scenario 1: Use Mintreu Servers (Default)

**No changes needed!** Just use as-is.

```ini
[UPDATE]
update_check_url = https://mintreu.com/api/bg-remover/version.json
```

---

### Scenario 2: Use Your Own Server

**Edit config.ini before distribution:**

```ini
[UPDATE]
update_check_url = https://your-domain.com/api/version.json
fallback_urls = https://backup.your-domain.com/api/version.json
download_base_url = https://your-domain.com/downloads/bg-remover

[APPLICATION]
company_website = https://your-domain.com
support_email = support@your-domain.com
```

**Then build distributions:**
```bash
python build_complete_offline.py
```

All built distributions will include your customized config!

---

### Scenario 3: Corporate Internal Network

```ini
[UPDATE]
update_check_url = http://internal-server.company.local/bg-remover/version.json
fallback_urls =
auto_check_updates = true

[DOWNLOAD]
download_base_url = http://internal-server.company.local/downloads

[APPLICATION]
company_name = Acme Corporation
support_email = it-support@acme.com
```

---

### Scenario 4: Offline Environment

```ini
[UPDATE]
auto_check_updates = false
background_update_check = false

[MODELS]
auto_download_models = false
```

---

## 🧪 Testing Configuration

### Test Config Loader

```bash
python config_loader.py
```

**Output:**
```
Testing Configuration Loader
======================================================================

Update Check URL: https://your-url.com/version.json
Fallback URLs: ['https://backup.com/...']
Update Timeout: 10s
Auto-check Updates: True

App Name: Mintreu BG Remover
Company: Your Company
Website: https://your-company.com

Log Level: INFO
Enable File Logging: True

Config File: C:\...\config.ini

======================================================================
✓ Configuration test complete!
```

### Test in Application

1. Edit `config.ini` with test URL
2. Run application
3. Go to **System → Check for Updates**
4. Verify it tries your URL

---

## 📖 Configuration Examples

### Example 1: Minimal Config

```ini
[UPDATE]
update_check_url = https://your-domain.com/version.json
```

### Example 2: Complete Corporate Config

```ini
[UPDATE]
update_check_url = https://updates.acme.com/bg-remover/version.json
fallback_urls = https://backup.acme.com/bg-remover/version.json,https://cdn.acme.com/bg-remover/version.json
update_check_timeout = 15
download_timeout = 600
auto_check_updates = true
background_update_check = true

[DOWNLOAD]
download_base_url = https://downloads.acme.com/bg-remover
download_folder = C:\AcmeDownloads

[APPLICATION]
app_name = Acme BG Remover
company_name = Acme Corporation
company_website = https://acme.com
support_email = support@acme.com
support_url = https://acme.com/support

[LOGGING]
log_level = WARNING
log_file = C:\ProgramData\AcmeBGRemover\app.log

[ADVANCED]
default_workers = 8
output_directory = C:\AcmeOutput
```

### Example 3: Development Config

```ini
[UPDATE]
update_check_url = http://localhost:8000/version.json
auto_check_updates = false

[LOGGING]
log_level = DEBUG

[ADVANCED]
default_workers = 1
cache_directory = C:\Dev\cache
output_directory = C:\Dev\output
```

---

## 🔒 Security Notes

### Always Use HTTPS

```ini
✅ GOOD: https://mintreu.com/api/version.json
❌ BAD:  http://mintreu.com/api/version.json (insecure!)
```

### Protect Configuration

For sensitive deployments:

```bash
# Windows - Restrict access
icacls config.ini /inheritance:r /grant:r "%USERNAME%:F"
```

---

## 📋 Integration with Build System

The build script (`build_complete_offline.py`) automatically:

✅ Copies `config.ini` to portable distribution
✅ Includes `config_loader.py` module
✅ Updates `updater.py` with config integration
✅ Includes in Windows installer

**Your customized config.ini will be in all distributions!**

---

## 🎯 How It Works

```
Application Starts
       ↓
Searches for config.ini
  (3 locations)
       ↓
  Found? → Load settings
       ↓
Not found? → Use defaults
       ↓
Apply settings to:
  - Update checker
  - Downloader
  - UI
  - Logger
```

---

## 📚 Documentation Files

1. **`config.ini`** - The configuration file itself
2. **`config_loader.py`** - Python module that loads config
3. **`CONFIG_GUIDE.md`** - Complete configuration guide
4. **`CONFIGURATION_SUMMARY.md`** - This file
5. **`AUTO_UPDATE_README.md`** - Update system overview
6. **`API_UPDATE_DOCUMENTATION.md`** - API specifications

---

## ✅ Benefits

### For Developers
- ✅ No hardcoded URLs
- ✅ Easy to customize
- ✅ Type-safe configuration
- ✅ Comprehensive defaults

### For Administrators
- ✅ Central configuration
- ✅ Easy deployment
- ✅ No code changes needed
- ✅ Per-user overrides

### For End Users
- ✅ Simple text file
- ✅ Human-readable
- ✅ Edit with Notepad
- ✅ Clear documentation

---

## 🚀 Quick Start

### 1. Edit Configuration

```bash
notepad config.ini
```

### 2. Change URL

```ini
[UPDATE]
update_check_url = https://your-domain.com/api/version.json
```

### 3. Build Distributions

```bash
python build_complete_offline.py
```

### 4. Done!

All distributions will use your custom URL!

---

## 💡 Pro Tips

### Tip 1: Version Control

```bash
# Keep original
copy config.ini config.ini.original

# Create environment-specific configs
config.dev.ini
config.staging.ini
config.production.ini
```

### Tip 2: Template Configs

Create templates for different scenarios:

```
config.corporate.ini
config.offline.ini
config.highperformance.ini
```

### Tip 3: Documentation

Document your custom URLs in deployment guide:

```markdown
## Update Server

Our update server: https://updates.our-company.com
API endpoint: /bg-remover/version.json
```

---

## 🐛 Troubleshooting

### Config Not Loading?

**Check:**
1. File exists in searched locations
2. File has correct INI syntax
3. Section names match (case-sensitive)
4. Application restarted after changes

**Test:**
```bash
python config_loader.py
```

### URL Not Working?

**Check:**
1. URL is correct (test in browser)
2. Using HTTPS (not HTTP)
3. Server is accessible
4. Firewall not blocking
5. Valid JSON response

---

## 📞 Support

For configuration help:

- **Read:** `CONFIG_GUIDE.md` (detailed guide)
- **Email:** contact@mintreu.com
- **Website:** https://mintreu.com

---

## ✅ Summary

You now have a **complete configuration system** that:

✅ Stores all settings in `config.ini`
✅ Allows easy URL customization
✅ Works with portable and installed versions
✅ Supports multiple configuration locations
✅ Includes comprehensive documentation
✅ Integrates with build system
✅ Requires no code changes

**Just edit config.ini and you're done!**

---

**Configuration System v1.0.0**
**Complete and Ready to Use!**

**Author:** Krishanu Bhattacharya @ Mintreu
