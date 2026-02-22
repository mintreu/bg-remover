"""
Mintreu BG Remover - Auto-Update System
========================================
Checks for updates from mintreu.com and handles automatic updates.

For Installed Version: Silent auto-update in background
For Portable Version: Download notification with manual update

Author: Krishanu Bhattacharya
Company: Mintreu
License: MIT
"""

import sys
import os
import json
import logging
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from urllib import request, error
import threading

logger = logging.getLogger("Updater")

# ============================================================================
# UPDATE CONFIGURATION
# ============================================================================

# Import configuration loader
try:
    from config_loader import app_config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

# Load settings from config file or use defaults
if CONFIG_AVAILABLE:
    UPDATE_CHECK_URL = app_config.update_check_url
    FALLBACK_URLS = app_config.fallback_urls
    UPDATE_CHECK_TIMEOUT = app_config.update_check_timeout
    DOWNLOAD_TIMEOUT = app_config.download_timeout
    DOWNLOAD_BASE_URL = app_config.download_base_url
else:
    # Fallback to hardcoded defaults if config not available
    UPDATE_CHECK_URL = "https://mintreu.com/api/bg-remover/version.json"
    DOWNLOAD_BASE_URL = "https://mintreu.com/downloads/bg-remover"
    FALLBACK_URLS = [
        "https://updates.mintreu.com/bg-remover/version.json",
        "https://cdn.mintreu.com/bg-remover/version.json"
    ]
    UPDATE_CHECK_TIMEOUT = 10  # seconds
    DOWNLOAD_TIMEOUT = 300  # 5 minutes for downloading updates

# ============================================================================
# VERSION INFO
# ============================================================================

@dataclass
class VersionInfo:
    """Version information from server."""
    version: str
    release_date: str
    download_url_installer: str
    download_url_portable: str
    changelog: str
    critical: bool = False
    min_version: str = "0.0.0"

    @staticmethod
    def from_json(data: Dict) -> 'VersionInfo':
        """Create VersionInfo from JSON response."""
        return VersionInfo(
            version=data.get('version', '0.0.0'),
            release_date=data.get('release_date', ''),
            download_url_installer=data.get('download_url_installer', ''),
            download_url_portable=data.get('download_url_portable', ''),
            changelog=data.get('changelog', ''),
            critical=data.get('critical', False),
            min_version=data.get('min_version', '0.0.0')
        )

# ============================================================================
# VERSION COMPARISON
# ============================================================================

def parse_version(version_str: str) -> Tuple[int, int, int]:
    """Parse version string to tuple of integers."""
    try:
        parts = version_str.strip('v').split('.')
        return tuple(int(p) for p in parts[:3])
    except:
        return (0, 0, 0)

def is_newer_version(current: str, latest: str) -> bool:
    """Check if latest version is newer than current."""
    current_tuple = parse_version(current)
    latest_tuple = parse_version(latest)
    return latest_tuple > current_tuple

# ============================================================================
# UPDATE CHECKER
# ============================================================================

class UpdateChecker:
    """Check for application updates."""

    def __init__(self, current_version: str):
        self.current_version = current_version
        self._cache_file = Path.home() / ".mintreu_bg_remover" / "update_cache.json"
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)

    def check_for_updates(self, silent: bool = True) -> Optional[VersionInfo]:
        """
        Check if updates are available.

        Args:
            silent: If True, suppress error messages

        Returns:
            VersionInfo if update available, None otherwise
        """
        try:
            logger.info(f"Checking for updates (current version: {self.current_version})")

            # Try main URL first
            version_info = self._fetch_version_info(UPDATE_CHECK_URL)

            # Try fallback URLs if main fails
            if not version_info:
                for fallback_url in FALLBACK_URLS:
                    logger.info(f"Trying fallback URL: {fallback_url}")
                    version_info = self._fetch_version_info(fallback_url)
                    if version_info:
                        break

            if not version_info:
                logger.warning("Could not fetch version information")
                return None

            # Cache the version info
            self._cache_version_info(version_info)

            # Check if update is available
            if is_newer_version(self.current_version, version_info.version):
                logger.info(f"Update available: {version_info.version}")
                return version_info
            else:
                logger.info("Application is up to date")
                return None

        except Exception as e:
            if not silent:
                logger.error(f"Error checking for updates: {e}")
            return None

    def _fetch_version_info(self, url: str) -> Optional[VersionInfo]:
        """Fetch version information from URL."""
        try:
            req = request.Request(
                url,
                headers={'User-Agent': f'MintreuBgRemover/{self.current_version}'}
            )

            with request.urlopen(req, timeout=UPDATE_CHECK_TIMEOUT) as response:
                data = json.loads(response.read().decode('utf-8'))
                return VersionInfo.from_json(data)

        except error.URLError as e:
            logger.debug(f"URL error fetching {url}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from {url}: {e}")
            return None
        except Exception as e:
            logger.debug(f"Error fetching version info from {url}: {e}")
            return None

    def _cache_version_info(self, version_info: VersionInfo):
        """Cache version information locally."""
        try:
            cache_data = {
                'version': version_info.version,
                'release_date': version_info.release_date,
                'changelog': version_info.changelog,
                'checked_at': str(Path(__file__).stat().st_mtime)
            }
            self._cache_file.write_text(json.dumps(cache_data, indent=2))
        except Exception as e:
            logger.debug(f"Could not cache version info: {e}")

    def get_cached_version_info(self) -> Optional[Dict]:
        """Get cached version information."""
        try:
            if self._cache_file.exists():
                return json.loads(self._cache_file.read_text())
        except:
            pass
        return None

# ============================================================================
# AUTO-UPDATER FOR INSTALLED VERSION
# ============================================================================

class InstalledUpdater:
    """Handle silent auto-updates for installed version."""

    def __init__(self, current_version: str):
        self.current_version = current_version
        self.checker = UpdateChecker(current_version)

    def is_installed_version(self) -> bool:
        """Check if running as installed version."""
        # Check if running from Program Files or has uninstaller
        exe_path = Path(sys.executable)

        # Check common installation directories
        install_dirs = [
            Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')),
            Path(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')),
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs'
        ]

        for install_dir in install_dirs:
            try:
                if install_dir and exe_path.is_relative_to(install_dir):
                    return True
            except:
                pass

        # Check for uninstaller
        if getattr(sys, 'frozen', False):
            app_dir = Path(sys.executable).parent
            uninstall_file = app_dir / "unins000.exe"
            if uninstall_file.exists():
                return True

        return False

    def check_and_update(self, silent: bool = True) -> bool:
        """
        Check for updates and install silently if available.

        Args:
            silent: If True, update in background without user interaction

        Returns:
            True if update was installed, False otherwise
        """
        try:
            logger.info("Checking for updates (installed version)")

            version_info = self.checker.check_for_updates(silent=silent)

            if not version_info:
                return False

            logger.info(f"Update available: {version_info.version}")

            # Download installer
            installer_path = self._download_installer(version_info.download_url_installer)

            if not installer_path:
                logger.error("Failed to download installer")
                return False

            # Install update
            if silent:
                success = self._install_silently(installer_path)
            else:
                success = self._install_with_ui(installer_path)

            return success

        except Exception as e:
            logger.error(f"Error during auto-update: {e}")
            return False

    def _download_installer(self, url: str) -> Optional[Path]:
        """Download installer to temp directory."""
        try:
            logger.info(f"Downloading installer from {url}")

            # Create temp file
            temp_dir = Path(tempfile.gettempdir()) / "mintreu_updates"
            temp_dir.mkdir(exist_ok=True)

            installer_path = temp_dir / f"MintreuBgRemover_Update_{self.current_version}.exe"

            # Download with progress
            req = request.Request(
                url,
                headers={'User-Agent': f'MintreuBgRemover/{self.current_version}'}
            )

            with request.urlopen(req, timeout=DOWNLOAD_TIMEOUT) as response:
                total_size = int(response.headers.get('content-length', 0))

                with open(installer_path, 'wb') as f:
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
                            logger.debug(f"Download progress: {percent:.1f}%")

            logger.info(f"Installer downloaded: {installer_path}")
            return installer_path

        except Exception as e:
            logger.error(f"Error downloading installer: {e}")
            return None

    def _install_silently(self, installer_path: Path) -> bool:
        """Install update silently in background."""
        try:
            logger.info("Installing update silently")

            # Run installer with silent flags
            cmd = [
                str(installer_path),
                '/VERYSILENT',
                '/SUPPRESSMSGBOXES',
                '/NORESTART',
                '/CLOSEAPPLICATIONS',
                '/RESTARTAPPLICATIONS'
            ]

            # Start installer and exit current application
            subprocess.Popen(cmd, shell=False)

            logger.info("Silent update initiated. Application will restart.")
            return True

        except Exception as e:
            logger.error(f"Error installing update silently: {e}")
            return False

    def _install_with_ui(self, installer_path: Path) -> bool:
        """Install update with user interface."""
        try:
            logger.info("Launching installer with UI")

            # Run installer normally
            subprocess.Popen([str(installer_path)], shell=False)

            logger.info("Installer launched")
            return True

        except Exception as e:
            logger.error(f"Error launching installer: {e}")
            return False

# ============================================================================
# UPDATER FOR PORTABLE VERSION
# ============================================================================

class PortableUpdater:
    """Handle update notifications for portable version."""

    def __init__(self, current_version: str):
        self.current_version = current_version
        self.checker = UpdateChecker(current_version)

    def check_for_updates(self) -> Optional[VersionInfo]:
        """Check for updates and return version info if available."""
        return self.checker.check_for_updates(silent=True)

    def download_update(self, version_info: VersionInfo, dest_path: Optional[Path] = None) -> Optional[Path]:
        """
        Download portable update.

        Args:
            version_info: Version information from server
            dest_path: Destination path for download (default: Downloads folder)

        Returns:
            Path to downloaded file, or None if failed
        """
        try:
            if dest_path is None:
                downloads = Path.home() / "Downloads"
                downloads.mkdir(exist_ok=True)
                dest_path = downloads / f"MintreuBgRemover_v{version_info.version}_Portable.zip"

            logger.info(f"Downloading portable update to {dest_path}")

            # Download
            req = request.Request(
                version_info.download_url_portable,
                headers={'User-Agent': f'MintreuBgRemover/{self.current_version}'}
            )

            with request.urlopen(req, timeout=DOWNLOAD_TIMEOUT) as response:
                total_size = int(response.headers.get('content-length', 0))

                with open(dest_path, 'wb') as f:
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
                            logger.debug(f"Download progress: {percent:.1f}%")

            logger.info(f"Update downloaded successfully: {dest_path}")
            return dest_path

        except Exception as e:
            logger.error(f"Error downloading portable update: {e}")
            return None

    def get_download_url(self, version_info: VersionInfo) -> str:
        """Get direct download URL for manual download."""
        return version_info.download_url_portable

# ============================================================================
# BACKGROUND UPDATE CHECKER
# ============================================================================

class BackgroundUpdateChecker:
    """Check for updates in background thread."""

    def __init__(self, current_version: str, callback=None):
        self.current_version = current_version
        self.callback = callback
        self.checker = UpdateChecker(current_version)
        self._thread = None

    def start(self):
        """Start background update check."""
        if self._thread and self._thread.is_alive():
            return

        self._thread = threading.Thread(target=self._check_updates, daemon=True)
        self._thread.start()
        logger.info("Background update checker started")

    def _check_updates(self):
        """Background thread function."""
        try:
            version_info = self.checker.check_for_updates(silent=True)

            if version_info and self.callback:
                self.callback(version_info)

        except Exception as e:
            logger.debug(f"Background update check failed: {e}")

# ============================================================================
# MAIN UPDATE MANAGER
# ============================================================================

class UpdateManager:
    """Main update manager - decides between installed and portable updater."""

    def __init__(self, current_version: str):
        self.current_version = current_version
        self.installed_updater = InstalledUpdater(current_version)
        self.portable_updater = PortableUpdater(current_version)

    def is_installed(self) -> bool:
        """Check if running as installed version."""
        return self.installed_updater.is_installed_version()

    def check_and_apply_updates(self, silent: bool = True) -> Tuple[bool, Optional[VersionInfo]]:
        """
        Check for updates and apply if possible.

        Returns:
            (updated, version_info) tuple
            updated: True if update was applied
            version_info: VersionInfo if update available, None otherwise
        """
        if self.is_installed():
            # Installed version - auto-update silently
            logger.info("Running as installed version - attempting silent update")
            updated = self.installed_updater.check_and_update(silent=silent)
            return updated, None
        else:
            # Portable version - just check and notify
            logger.info("Running as portable version - checking for updates")
            version_info = self.portable_updater.check_for_updates()
            return False, version_info

    def get_updater(self):
        """Get appropriate updater based on installation type."""
        if self.is_installed():
            return self.installed_updater
        else:
            return self.portable_updater

# ============================================================================
# TESTING AND DEBUGGING
# ============================================================================

def test_update_system():
    """Test the update system."""
    print("Testing Mintreu BG Remover Update System")
    print("=" * 70)

    current_version = "1.0.0"

    # Test version comparison
    print("\n[1] Testing version comparison...")
    assert is_newer_version("1.0.0", "1.0.1") == True
    assert is_newer_version("1.0.0", "1.1.0") == True
    assert is_newer_version("1.0.0", "2.0.0") == True
    assert is_newer_version("1.1.0", "1.0.9") == False
    assert is_newer_version("1.0.0", "1.0.0") == False
    print("✓ Version comparison works")

    # Test update checker
    print("\n[2] Testing update checker...")
    checker = UpdateChecker(current_version)
    version_info = checker.check_for_updates(silent=True)

    if version_info:
        print(f"✓ Update found: {version_info.version}")
        print(f"  Release date: {version_info.release_date}")
        print(f"  Changelog: {version_info.changelog[:100]}...")
    else:
        print("✓ No updates available (or server unreachable)")

    # Test installation detection
    print("\n[3] Testing installation detection...")
    manager = UpdateManager(current_version)
    if manager.is_installed():
        print("✓ Running as installed version")
    else:
        print("✓ Running as portable version")

    print("\n" + "=" * 70)
    print("Update system test complete!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_update_system()
