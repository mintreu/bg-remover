# Mintreu BG Remover - Update API Documentation

**Version:** 1.0.0
**Author:** Krishanu Bhattacharya
**Company:** Mintreu

---

## Overview

This document describes the update check API that must be hosted at `https://mintreu.com/api/bg-remover/version.json` to enable auto-update functionality.

---

## API Endpoint

### Version Check Endpoint

**URL:** `https://mintreu.com/api/bg-remover/version.json`

**Method:** `GET`

**Authentication:** None (public endpoint)

**Rate Limiting:** Recommended 100 requests/minute per IP

---

## Response Format

The endpoint must return a JSON object with the following structure:

```json
{
  "version": "1.1.0",
  "release_date": "2025-02-01",
  "download_url_installer": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.1.0_Setup.exe",
  "download_url_portable": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.1.0_Portable.zip",
  "changelog": "## What's New in v1.1.0\n\n- Added GPU acceleration support\n- Improved processing speed by 50%\n- Fixed memory leak in batch processing\n- Updated AI model to RMBG v1.5\n- Added support for WebP format",
  "critical": false,
  "min_version": "1.0.0"
}
```

---

## Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Yes | Latest version number in semver format (e.g., "1.1.0") |
| `release_date` | string | Yes | Release date in YYYY-MM-DD format |
| `download_url_installer` | string | Yes | Direct download URL for Windows installer (.exe) |
| `download_url_portable` | string | Yes | Direct download URL for portable ZIP |
| `changelog` | string | Yes | Markdown-formatted changelog (max 1000 chars recommended) |
| `critical` | boolean | No | If true, update is critical (default: false) |
| `min_version` | string | No | Minimum version that can auto-update (default: "0.0.0") |

---

## Response Headers

Recommended headers:

```
Content-Type: application/json
Cache-Control: public, max-age=3600
Access-Control-Allow-Origin: *
```

---

## Example Responses

### Scenario 1: Normal Update Available

```json
{
  "version": "1.1.0",
  "release_date": "2025-02-01",
  "download_url_installer": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.1.0_Setup.exe",
  "download_url_portable": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.1.0_Portable.zip",
  "changelog": "### New Features\n- GPU acceleration\n- Faster processing\n\n### Bug Fixes\n- Fixed memory leak\n- Improved stability",
  "critical": false,
  "min_version": "1.0.0"
}
```

### Scenario 2: Critical Security Update

```json
{
  "version": "1.0.1",
  "release_date": "2025-01-15",
  "download_url_installer": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.0.1_Setup.exe",
  "download_url_portable": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.0.1_Portable.zip",
  "changelog": "### Critical Security Update\n\n- Fixed security vulnerability CVE-2025-XXXX\n- All users must update immediately",
  "critical": true,
  "min_version": "0.0.0"
}
```

---

## Client Behavior

### Update Check Process

1. **Startup Check:**
   - Application checks for updates in background on startup
   - Non-blocking, silent check
   - Results displayed as notification if update available

2. **Manual Check:**
   - User clicks "System → Check for Updates"
   - Shows checking dialog
   - Displays results immediately

3. **Version Comparison:**
   - Client compares `version` field with current version
   - Uses semantic versioning rules (major.minor.patch)
   - Update available if server version > current version

### Installed Version Behavior

**When update is available:**

1. Shows update notification dialog with:
   - Current version
   - New version
   - Release date
   - Changelog (first 200 chars)
   - "Install Now" or "Later" option

2. If user clicks "Install Now":
   - Downloads installer from `download_url_installer`
   - Runs installer with `/VERYSILENT` flag
   - Application exits to allow update
   - Installer automatically restarts application

3. If user clicks "Later":
   - Notification dismissed
   - User can check again later from menu

### Portable Version Behavior

**When update is available:**

1. Shows update notification dialog with:
   - Current version
   - New version
   - Release date
   - Changelog (first 200 chars)
   - "Download" or "Later" option

2. If user clicks "Download":
   - Downloads portable ZIP from `download_url_portable`
   - Saves to Downloads folder
   - Opens Downloads folder
   - Shows instructions to extract and run

3. If user clicks "Later":
   - Notification dismissed
   - User can download later from menu

---

## Fallback URLs

If main URL fails, client tries these fallback URLs in order:

1. `https://updates.mintreu.com/bg-remover/version.json`
2. `https://cdn.mintreu.com/bg-remover/version.json`

**Recommendation:** Set up mirrors for high availability

---

## Implementation Guide

### Option 1: Static JSON File

**Simplest approach** - Host a static JSON file:

```bash
# Create version.json
cat > version.json << 'EOF'
{
  "version": "1.0.0",
  "release_date": "2025-01-01",
  "download_url_installer": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.0.0_Setup.exe",
  "download_url_portable": "https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.0.0_Portable.zip",
  "changelog": "Initial release",
  "critical": false
}
EOF

# Upload to server
scp version.json user@mintreu.com:/var/www/mintreu.com/api/bg-remover/
```

**To update:**
1. Edit version.json
2. Upload new version
3. Client will see update on next check

---

### Option 2: Dynamic API (PHP)

Create `/api/bg-remover/version.php`:

```php
<?php
header('Content-Type: application/json');
header('Cache-Control: public, max-age=3600');
header('Access-Control-Allow-Origin: *');

$version_info = [
    'version' => '1.0.0',
    'release_date' => '2025-01-01',
    'download_url_installer' => 'https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.0.0_Setup.exe',
    'download_url_portable' => 'https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.0.0_Portable.zip',
    'changelog' => 'Initial release',
    'critical' => false,
    'min_version' => '0.0.0'
];

echo json_encode($version_info, JSON_PRETTY_PRINT);
?>
```

**URL Rewrite** (Apache .htaccess):
```apache
RewriteEngine On
RewriteRule ^api/bg-remover/version\.json$ /api/bg-remover/version.php [L]
```

---

### Option 3: Dynamic API (Node.js/Express)

```javascript
const express = require('express');
const app = express();

app.get('/api/bg-remover/version.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'public, max-age=3600');

  const versionInfo = {
    version: '1.0.0',
    release_date: '2025-01-01',
    download_url_installer: 'https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.0.0_Setup.exe',
    download_url_portable: 'https://mintreu.com/downloads/bg-remover/MintreuBgRemover_v1.0.0_Portable.zip',
    changelog: 'Initial release',
    critical: false,
    min_version: '0.0.0'
  };

  res.json(versionInfo);
});

app.listen(3000);
```

---

### Option 4: Database-Driven (Recommended for Production)

```python
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/bg-remover/version.json')
def get_version():
    # Fetch from database
    version_info = {
        'version': get_latest_version_from_db(),
        'release_date': get_release_date_from_db(),
        'download_url_installer': get_download_url('installer'),
        'download_url_portable': get_download_url('portable'),
        'changelog': get_changelog_from_db(),
        'critical': is_critical_update(),
        'min_version': get_min_version()
    }

    response = jsonify(version_info)
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response

if __name__ == '__main__':
    app.run()
```

---

## Download URLs Setup

### File Hosting

Place distribution files at these URLs:

```
https://mintreu.com/downloads/bg-remover/
├── MintreuBgRemover_v1.0.0_Setup.exe
├── MintreuBgRemover_v1.0.0_Portable.zip
├── MintreuBgRemover_v1.1.0_Setup.exe
├── MintreuBgRemover_v1.1.0_Portable.zip
└── ...
```

### CDN Recommendation

Use CDN for better performance:

```
https://cdn.mintreu.com/bg-remover/
https://downloads.mintreu.com/bg-remover/
```

---

## Security Considerations

### 1. HTTPS Required

**Always use HTTPS** for API and download URLs to prevent MITM attacks.

### 2. File Integrity

Consider adding SHA256 checksums:

```json
{
  "version": "1.0.0",
  "download_url_installer": "...",
  "installer_sha256": "abc123...",
  "download_url_portable": "...",
  "portable_sha256": "def456..."
}
```

### 3. Code Signing

Sign executables with code signing certificate to reduce antivirus false positives.

### 4. Rate Limiting

Implement rate limiting to prevent abuse:

```nginx
limit_req_zone $binary_remote_addr zone=update_api:10m rate=10r/m;

location /api/bg-remover/version.json {
    limit_req zone=update_api burst=5;
    # ... rest of config
}
```

---

## Monitoring and Analytics

### Track Update Checks

Log update checks for analytics:

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "client_version": "1.0.0",
  "user_agent": "MintreuBgRemover/1.0.0",
  "ip": "1.2.3.4",
  "update_available": true,
  "latest_version": "1.1.0"
}
```

### Track Downloads

```json
{
  "timestamp": "2025-01-15T10:31:00Z",
  "file": "MintreuBgRemover_v1.1.0_Setup.exe",
  "version": "1.1.0",
  "client_version": "1.0.0",
  "ip": "1.2.3.4"
}
```

---

## Testing

### Test Update Check

```bash
# Test API endpoint
curl https://mintreu.com/api/bg-remover/version.json

# Expected output:
{
  "version": "1.0.0",
  "release_date": "2025-01-01",
  ...
}
```

### Test Client

```bash
# Run updater test
python updater.py

# Manual test in application:
# 1. Launch application
# 2. Go to System → Check for Updates
# 3. Verify notification appears
```

---

## Deployment Checklist

- [ ] Create version.json file
- [ ] Upload to https://mintreu.com/api/bg-remover/version.json
- [ ] Verify HTTPS works
- [ ] Test endpoint returns valid JSON
- [ ] Upload distribution files
- [ ] Verify download URLs work
- [ ] Test update check in application
- [ ] Test installer download
- [ ] Test portable download
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Set up fallback URLs

---

## Troubleshooting

### Issue: Client can't reach API

**Check:**
- HTTPS certificate valid
- CORS headers set correctly
- Firewall not blocking
- DNS resolves correctly

### Issue: Downloads fail

**Check:**
- Download URLs are correct
- Files exist on server
- Sufficient bandwidth
- HTTPS for download URLs

### Issue: Updates not detected

**Check:**
- Version number format correct (semver)
- Server version > client version
- JSON format valid
- No caching issues

---

## Support

For API setup assistance:
- **Email:** contact@mintreu.com
- **Website:** https://mintreu.com/support

---

**Document Version:** 1.0.0
**Last Updated:** 2025-01
**Author:** Krishanu Bhattacharya @ Mintreu
