# Mintreu BG Remover - Deployment Guide

**Version:** 1.0.0
**Date:** 2025-01
**Author:** Krishanu Bhattacharya
**Company:** Mintreu

---

## Overview

This document provides step-by-step instructions for deploying the Mintreu BG Remover application in various environments.

---

## Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All tests pass (`python test_application.py`)
- [ ] Application runs without errors
- [ ] Models download correctly
- [ ] Image processing works
- [ ] UI displays properly
- [ ] Logs are being generated
- [ ] All documentation is up-to-date
- [ ] Version numbers are correct
- [ ] License file is present

---

## Deployment Scenarios

### Scenario 1: End User Distribution

**Target:** General public
**Method:** Portable ZIP + Installer
**Platform:** Website download

**Steps:**

1. Build portable distribution:
   ```bash
   python build_complete_offline.py
   ```

2. Build Windows installer:
   ```bash
   # After portable build completes
   # Open: distributions/installer/MintreuBgRemover_installer.iss
   # In Inno Setup: Build → Compile
   ```

3. Test both distributions on clean Windows VMs

4. Upload to hosting:
   ```bash
   # Upload to S3, CDN, or web host
   aws s3 cp distributions/MintreuBgRemover_v1.0.0_Portable.zip s3://your-bucket/downloads/
   aws s3 cp distributions/installer/MintreuBgRemover_v1.0.0_Setup.exe s3://your-bucket/downloads/
   ```

5. Update website download links

6. Announce release

---

### Scenario 2: Enterprise Deployment

**Target:** Corporate environment
**Method:** Silent installer
**Platform:** Internal network

**Steps:**

1. Build Windows installer (see Scenario 1)

2. Create deployment package:
   ```
   deployment/
   ├── MintreuBgRemover_v1.0.0_Setup.exe
   ├── install_silent.bat
   ├── config.json (pre-configured settings)
   └── README_Enterprise.txt
   ```

3. Create silent install script (`install_silent.bat`):
   ```batch
   @echo off
   REM Silent installation for enterprise deployment

   MintreuBgRemover_v1.0.0_Setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /DIR="C:\Program Files\MintreuBgRemover" /LOG="install.log"

   if errorlevel 1 (
       echo Installation failed. Check install.log
       exit /b 1
   )

   echo Installation successful
   exit /b 0
   ```

4. Distribute via:
   - Group Policy
   - SCCM/Intune
   - Network share
   - USB drives

5. Provide IT documentation

---

### Scenario 3: Developer Distribution

**Target:** Developers/Contributors
**Method:** Source code + build scripts
**Platform:** GitHub/GitLab

**Steps:**

1. Prepare repository:
   ```bash
   # Ensure .gitignore excludes:
   # - venv/
   # - build/
   # - dist/
   # - distributions/
   # - __pycache__/
   # - *.pyc
   # - .env
   ```

2. Tag release:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. Create GitHub release with:
   - Release notes
   - Changelog
   - Pre-built distributions (portable ZIP, installer)
   - Source code archive

4. Update documentation

---

### Scenario 4: Portable USB Distribution

**Target:** Trade shows, demos, offline use
**Method:** USB drive with portable version
**Platform:** Physical media

**Steps:**

1. Build portable distribution

2. Create USB structure:
   ```
   USB_Drive/
   ├── MintreuBgRemover/        (Extracted portable app)
   ├── Sample_Images/            (Demo images)
   ├── README.txt                (Quick start guide)
   └── Support_Info.txt          (Contact information)
   ```

3. Pre-install dependencies:
   ```bash
   # On USB, run once to install dependencies
   cd MintreuBgRemover
   install_dependencies.bat
   ```

4. Optionally pre-download models:
   ```bash
   # Place rmbg_v14.onnx in MintreuBgRemover/models/
   ```

5. Test on multiple machines

6. Create multiple copies for distribution

---

## Hosting Options

### Option 1: Direct Download (Website)

**Pros:** Simple, full control
**Cons:** Bandwidth costs

**Setup:**
```html
<!-- On your website -->
<a href="/downloads/MintreuBgRemover_v1.0.0_Portable.zip">
  Download Portable (150 MB)
</a>
<a href="/downloads/MintreuBgRemover_v1.0.0_Setup.exe">
  Download Installer (150 MB)
</a>
```

---

### Option 2: Cloud Storage (S3, Google Drive)

**Pros:** Scalable, reliable
**Cons:** Monthly costs

**AWS S3 Example:**
```bash
# Upload
aws s3 cp distributions/MintreuBgRemover_v1.0.0_Portable.zip s3://your-bucket/releases/v1.0.0/ --acl public-read

# Get URL
aws s3 presign s3://your-bucket/releases/v1.0.0/MintreuBgRemover_v1.0.0_Portable.zip --expires-in 604800
```

**Google Drive:**
1. Upload to Google Drive
2. Right-click → Get link
3. Make link public
4. Use in download page

---

### Option 3: GitHub Releases

**Pros:** Free, version controlled
**Cons:** Public only (unless paid)

**Setup:**
1. Go to GitHub repository
2. Releases → Create new release
3. Tag version: v1.0.0
4. Upload distribution files
5. Publish release

---

### Option 4: CDN (Cloudflare, StackPath)

**Pros:** Fast, global, often free tier
**Cons:** Setup complexity

**Cloudflare Example:**
1. Upload to Cloudflare R2
2. Configure public access
3. Use CDN URL in download links

---

## Update Strategy

### Semantic Versioning

Follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

Examples:
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.1` → `1.1.0` (new feature)
- `1.1.0` → `2.0.0` (breaking change)

---

### Update Process

1. Update version in:
   - `main.py` → `APP_VERSION`
   - `pyproject.toml` → `version`
   - `build_complete_offline.py` → `APP_VERSION`

2. Update `CHANGELOG.md`

3. Run tests:
   ```bash
   python test_application.py
   ```

4. Build distributions:
   ```bash
   python build_complete_offline.py
   ```

5. Test distributions

6. Tag release:
   ```bash
   git tag -a v1.1.0 -m "Release version 1.1.0"
   git push origin v1.1.0
   ```

7. Deploy new version

8. Notify users

---

### Auto-Update (Future Feature)

For future versions, consider:

```python
# In main.py
def check_for_updates():
    """Check for new versions."""
    current_version = APP_VERSION
    response = requests.get("https://api.mintreu.com/bg-remover/version")
    latest_version = response.json()["version"]

    if latest_version > current_version:
        notify_user_of_update(latest_version)
```

---

## Analytics and Monitoring

### Download Tracking

Track download statistics:

**Method 1: Server Logs**
```bash
# Parse Apache/Nginx logs
cat access.log | grep "MintreuBgRemover.*\.zip" | wc -l
```

**Method 2: Analytics Script**
```javascript
// On download page
function trackDownload(filename) {
    gtag('event', 'download', {
        'event_category': 'Software',
        'event_label': filename,
        'value': '1.0.0'
    });
}
```

---

### Error Reporting (Optional)

Integrate error reporting:

```python
# In main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment="production",
    release=f"bg-remover@{APP_VERSION}"
)
```

---

### Usage Statistics (Privacy-Respecting)

**Optional:** Collect anonymous usage data

```python
def send_anonymous_stats():
    """Send anonymous usage statistics (opt-in only)."""
    if config.analytics_enabled:
        data = {
            'version': APP_VERSION,
            'platform': sys.platform,
            'images_processed': session_stats.total_images
        }
        requests.post("https://api.mintreu.com/stats", json=data)
```

---

## Support Infrastructure

### Support Channels

1. **Email:** contact@mintreu.com
2. **Website:** https://mintreu.com/support
3. **Documentation:** Include in distribution
4. **FAQ:** Common questions on website

---

### Log Collection

For support requests:

1. User provides log file:
   ```
   %USERPROFILE%\.mintreu_bg_remover\app.log
   ```

2. Analyze for errors

3. Provide solution

---

### Known Issues Database

Maintain a list of known issues:

```markdown
# Known Issues

## Issue: Slow processing on low-end CPUs
**Workaround:** Reduce worker threads to 1-2

## Issue: Antivirus false positive on EXE
**Workaround:** Use portable ZIP version

## Issue: Models fail to download
**Workaround:** Download manually from URL in docs
```

---

## Legal Considerations

### License Compliance

Ensure compliance with:

- **Your License:** MIT (included)
- **Dependencies:** Check all dependency licenses
- **Models:** BRIA AI model license
- **Third-party Assets:** Any icons, images

---

### Privacy Policy

If collecting any data:

1. Create privacy policy
2. Disclose data collection
3. Provide opt-out
4. Follow GDPR/CCPA if applicable

---

### Terms of Service

Consider adding:

```
SOFTWARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
User agrees not to use for malicious purposes.
User responsible for content processed.
```

---

## Marketing and Promotion

### Launch Checklist

- [ ] Press release prepared
- [ ] Social media posts scheduled
- [ ] Product Hunt submission ready
- [ ] Demo video created
- [ ] Screenshots prepared
- [ ] Landing page updated
- [ ] Email list notified
- [ ] Blog post written

---

### Landing Page Elements

Include:

1. Hero section with screenshot
2. Feature highlights
3. Download buttons (prominent)
4. System requirements
5. Quick start guide
6. Video demo
7. Testimonials (if available)
8. Support information
9. FAQ
10. Contact form

---

### SEO Keywords

Target keywords:

- Background remover
- AI background removal
- Remove image background
- Offline background remover
- Windows background removal tool
- Batch background remover
- Free background remover

---

## Backup and Disaster Recovery

### Backup Strategy

**What to backup:**

1. Source code (Git)
2. Build artifacts
3. Distribution files
4. Documentation
5. Models (cached)
6. User configs (in production)

**Backup schedule:**

- Source code: Continuous (Git)
- Distributions: Each release
- Documentation: Weekly
- Models: On acquisition

---

### Disaster Recovery

**Scenarios and responses:**

1. **Hosting down:**
   - Use backup CDN
   - Update DNS if needed

2. **Corrupted builds:**
   - Rebuild from tagged release
   - Restore from backup

3. **Model unavailable:**
   - Provide direct download link
   - Mirror model on own hosting

---

## Post-Deployment

### Monitor

- Download counts
- Error reports
- User feedback
- Performance metrics
- Support requests

---

### Iterate

1. Collect feedback
2. Prioritize fixes and features
3. Plan next release
4. Repeat deployment process

---

### Communicate

Keep users informed:

- Email newsletters
- Blog updates
- Social media
- Release notes
- Changelog

---

## Security

### Code Signing (Recommended)

Sign executables to reduce antivirus false positives:

1. Obtain code signing certificate ($100-$500/year)
2. Sign EXE with signtool:
   ```bash
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com MintreuBgRemover.exe
   ```

---

### Dependency Security

Regularly check for vulnerabilities:

```bash
# Check for known vulnerabilities
pip install safety
safety check

# Update dependencies
pip list --outdated
pip install --upgrade package_name
```

---

### Secure Distribution

- Use HTTPS for downloads
- Provide SHA256 checksums
- Consider GPG signatures
- Scan for malware before uploading

**Example checksums file:**
```
# SHA256 Checksums
abc123... MintreuBgRemover_v1.0.0_Portable.zip
def456... MintreuBgRemover_v1.0.0_Setup.exe
```

---

## Conclusion

Following this deployment guide ensures:

✅ Professional distribution
✅ Multiple deployment options
✅ Scalable infrastructure
✅ Proper support channels
✅ Security best practices
✅ Legal compliance
✅ Effective marketing
✅ Sustainable maintenance

---

**For questions or support:**

- Email: contact@mintreu.com
- Website: https://mintreu.com

---

**Document Version:** 1.0.0
**Last Updated:** 2025-01
**Author:** Krishanu Bhattacharya @ Mintreu
