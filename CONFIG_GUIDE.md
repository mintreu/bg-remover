# Mintreu BG Remover - Configuration Guide

## Overview

The application uses a `config.ini` file for all configurable settings including update URLs, timeouts, and application preferences.

---

## Configuration File Location

The application searches for `config.ini` in these locations (in order):

1. **Application directory** (same folder as executable/script)
2. **User home directory:** `%USERPROFILE%\.mintreu_bg_remover\config.ini`
3. **Current working directory**

---

## Quick Start

### 1. Locate config.ini

After installation or extraction, you'll find `config.ini` in the application folder.

### 2. Edit with Text Editor

```bash
# Windows
notepad config.ini

# Or use any text editor
```

### 3. Change Settings

Example - Change update URL:

```ini
[UPDATE]
update_check_url = https://your-domain.com/api/version.json
```

### 4. Save and Restart Application

Changes take effect on next application start.

---

## Configuration Sections

### [UPDATE] - Update System Settings

Controls how the application checks for and downloads updates.

```ini
[UPDATE]
# Main update check URL
update_check_url = https://mintreu.com/api/bg-remover/version.json

# Backup URLs (comma-separated)
fallback_urls = https://updates.mintreu.com/bg-remover/version.json,https://cdn.mintreu.com/bg-remover/version.json

# Timeout for checking updates (seconds)
update_check_timeout = 10

# Timeout for downloading updates (seconds)
download_timeout = 300

# Enable automatic update checking on startup
auto_check_updates = true

# Check updates in background (non-blocking)
background_update_check = true
```

**Key Settings:**

| Setting | Description | Default |
|---------|-------------|---------|
| `update_check_url` | Main URL to check for updates | mintreu.com API |
| `fallback_urls` | Backup URLs if main fails | 2 fallback URLs |
| `update_check_timeout` | How long to wait for response | 10 seconds |
| `download_timeout` | How long to wait for download | 300 seconds (5 min) |
| `auto_check_updates` | Check on startup | true |
| `background_update_check` | Non-blocking check | true |

---

### [DOWNLOAD] - Download Settings

Controls where updates and files are downloaded.

```ini
[DOWNLOAD]
# Base URL for downloading distribution files
download_base_url = https://mintreu.com/downloads/bg-remover

# Custom download folder (leave empty for default Downloads folder)
download_folder =
```

**Key Settings:**

| Setting | Description | Default |
|---------|-------------|---------|
| `download_base_url` | URL prefix for downloads | mintreu.com downloads |
| `download_folder` | Custom download location | (empty = Downloads folder) |

**Example - Custom Download Folder:**

```ini
download_folder = C:\MyDownloads\BgRemover
```

---

### [APPLICATION] - Application Info

Company and support information displayed in the app.

```ini
[APPLICATION]
app_name = Mintreu BG Remover
company_name = Mintreu
company_website = https://mintreu.com
support_email = contact@mintreu.com
support_url = https://mintreu.com/support
```

**Usage:** These values appear in:
- About dialog
- Error messages
- Support links
- Application title

---

### [MODELS] - AI Model Settings

Controls AI model download behavior.

```ini
[MODELS]
# Base URL for model downloads
model_base_url = https://huggingface.co

# Automatically download models on first run
auto_download_models = true
```

**Key Settings:**

| Setting | Description | Default |
|---------|-------------|---------|
| `model_base_url` | Where to download models from | Hugging Face |
| `auto_download_models` | Auto-download on first run | true |

---

### [LOGGING] - Logging Configuration

Controls application logging behavior.

```ini
[LOGGING]
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
log_level = INFO

# Enable logging to file
enable_file_logging = true

# Custom log file path (leave empty for default)
log_file =
```

**Key Settings:**

| Setting | Description | Default |
|---------|-------------|---------|
| `log_level` | Verbosity of logs | INFO |
| `enable_file_logging` | Save logs to file | true |
| `log_file` | Custom log location | (empty = default) |

**Log Levels:**

- `DEBUG` - Very detailed (for development)
- `INFO` - General information (recommended)
- `WARNING` - Only warnings and errors
- `ERROR` - Only errors
- `CRITICAL` - Only critical errors

**Default Log Location:**
`%USERPROFILE%\.mintreu_bg_remover\app.log`

---

### [ADVANCED] - Advanced Settings

Advanced settings for power users.

```ini
[ADVANCED]
# Number of worker threads (0 = auto-detect)
default_workers = 0

# Enable GPU acceleration [Future feature]
enable_gpu = false

# Custom cache directory
cache_directory =

# Custom output directory
output_directory =
```

**Key Settings:**

| Setting | Description | Default |
|---------|-------------|---------|
| `default_workers` | Processing threads | 0 (auto) |
| `enable_gpu` | GPU acceleration | false |
| `cache_directory` | Custom cache folder | (empty = default) |
| `output_directory` | Custom output folder | (empty = default) |

**Worker Threads:**
- `0` = Auto-detect (CPU cores - 1)
- `1` = Single-threaded (slowest, safest)
- `2+` = Multi-threaded (faster)

---

## Common Configuration Scenarios

### Scenario 1: Corporate Deployment (Custom Update Server)

```ini
[UPDATE]
update_check_url = https://corporate-updates.company.com/bg-remover/version.json
fallback_urls = https://backup.company.com/bg-remover/version.json
auto_check_updates = true

[DOWNLOAD]
download_base_url = https://corporate-downloads.company.com/bg-remover

[LOGGING]
log_level = WARNING
log_file = C:\ProgramData\MintreuyBGRemover\logs\app.log
```

---

### Scenario 2: Offline Environment (No Updates)

```ini
[UPDATE]
auto_check_updates = false
background_update_check = false

[MODELS]
auto_download_models = false

[ADVANCED]
output_directory = C:\BgRemover\Output
```

---

### Scenario 3: Development/Testing

```ini
[UPDATE]
update_check_url = http://localhost:8000/version.json
fallback_urls =
update_check_timeout = 5

[LOGGING]
log_level = DEBUG
enable_file_logging = true

[ADVANCED]
default_workers = 1
cache_directory = C:\Dev\BgRemover\cache
output_directory = C:\Dev\BgRemover\output
```

---

### Scenario 4: High-Performance Setup

```ini
[ADVANCED]
default_workers = 12
enable_gpu = true

[UPDATE]
download_timeout = 600
```

---

## Editing During Installation

### For Portable Version

1. Extract ZIP file
2. Open `config.ini` in text editor
3. Modify settings
4. Save file
5. Run application

### For Installer Version

**Option 1: Pre-configure before installation**

1. Extract installer contents with 7-Zip
2. Edit `config.ini`
3. Repackage or deploy modified files

**Option 2: Post-installation configuration**

1. Install application
2. Navigate to install directory (e.g., `C:\Program Files\MintreuBgRemover\`)
3. Edit `config.ini`
4. Restart application

**Option 3: User-specific configuration**

Create config in user folder:
```
%USERPROFILE%\.mintreu_bg_remover\config.ini
```

This overrides the default configuration.

---

## Environment-Specific Configurations

### Development

```ini
[UPDATE]
update_check_url = http://localhost:8000/version.json
auto_check_updates = false

[LOGGING]
log_level = DEBUG

[ADVANCED]
default_workers = 1
```

### Staging

```ini
[UPDATE]
update_check_url = https://staging.mintreu.com/api/bg-remover/version.json
auto_check_updates = true

[LOGGING]
log_level = INFO
```

### Production

```ini
[UPDATE]
update_check_url = https://mintreu.com/api/bg-remover/version.json
fallback_urls = https://updates.mintreu.com/bg-remover/version.json,https://cdn.mintreu.com/bg-remover/version.json
auto_check_updates = true

[LOGGING]
log_level = WARNING
```

---

## Validation

### Test Configuration

Run the configuration tester:

```bash
python config_loader.py
```

**Output:**
```
Testing Configuration Loader
======================================================================

Update Check URL: https://mintreu.com/api/bg-remover/version.json
Fallback URLs: ['https://updates.mintreu.com/...', ...]
Update Timeout: 10s
Auto-check Updates: True

App Name: Mintreu BG Remover
Company: Mintreu
Website: https://mintreu.com

Log Level: INFO
Enable File Logging: True

Config File: C:\...\config.ini

======================================================================
✓ Configuration test complete!
```

---

## Troubleshooting

### Configuration Not Loading

**Problem:** Changes to config.ini don't take effect

**Solutions:**
1. Restart application
2. Check file location (must be in searched paths)
3. Check file permissions (must be readable)
4. Verify file format (valid INI syntax)

---

### Invalid Configuration

**Problem:** Application uses defaults instead of config

**Solutions:**
1. Check INI syntax is correct
2. Verify section names: `[UPDATE]`, `[DOWNLOAD]`, etc.
3. Check for typos in setting names
4. Ensure no special characters in values
5. Run `python config_loader.py` to validate

---

### Update URL Not Working

**Problem:** Can't check for updates

**Solutions:**
1. Verify URL is correct and accessible
2. Test URL in browser: should return valid JSON
3. Check firewall isn't blocking
4. Try fallback URLs
5. Set `auto_check_updates = false` if not needed

---

## Security Considerations

### Protecting Configuration

**Sensitive settings** (if any) should be protected:

```bash
# Windows - Restrict file permissions
icacls config.ini /inheritance:r /grant:r "%USERNAME%:F"

# This gives only current user full access
```

### HTTPS Requirements

**Always use HTTPS** for update URLs:

```ini
✓ update_check_url = https://mintreu.com/api/version.json
✗ update_check_url = http://mintreu.com/api/version.json (insecure)
```

---

## Template Configurations

### Minimal Configuration

```ini
[UPDATE]
update_check_url = https://mintreu.com/api/bg-remover/version.json
auto_check_updates = true
```

### Full Configuration

```ini
[UPDATE]
update_check_url = https://mintreu.com/api/bg-remover/version.json
fallback_urls = https://updates.mintreu.com/bg-remover/version.json,https://cdn.mintreu.com/bg-remover/version.json
update_check_timeout = 10
download_timeout = 300
auto_check_updates = true
background_update_check = true

[DOWNLOAD]
download_base_url = https://mintreu.com/downloads/bg-remover
download_folder =

[APPLICATION]
app_name = Mintreu BG Remover
company_name = Mintreu
company_website = https://mintreu.com
support_email = contact@mintreu.com
support_url = https://mintreu.com/support

[MODELS]
model_base_url = https://huggingface.co
auto_download_models = true

[LOGGING]
log_level = INFO
enable_file_logging = true
log_file =

[ADVANCED]
default_workers = 0
enable_gpu = false
cache_directory =
output_directory =
```

---

## Deployment Tips

### Mass Deployment

For deploying to many machines:

1. **Create master config.ini** with corporate settings
2. **Include in installer** or deployment package
3. **Use Group Policy** to distribute updates
4. **Document** for IT admins

### Configuration Management

```bash
# Backup current config
copy config.ini config.ini.backup

# Deploy new config
copy \\server\configs\bg-remover\config.ini .

# Verify
python config_loader.py
```

---

## Support

For configuration assistance:

- **Email:** contact@mintreu.com
- **Documentation:** See `AUTO_UPDATE_README.md`
- **API Docs:** See `API_UPDATE_DOCUMENTATION.md`

---

**Configuration Guide v1.0.0**
**Author:** Krishanu Bhattacharya @ Mintreu
