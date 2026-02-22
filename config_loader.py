"""
Mintreu BG Remover - Configuration Loader
==========================================
Loads configuration from config.ini file

Author: Krishanu Bhattacharya
Company: Mintreu
License: MIT
"""

import os
import sys
import logging
from pathlib import Path
from configparser import ConfigParser
from typing import Optional, List

logger = logging.getLogger("ConfigLoader")

# ============================================================================
# DEFAULT CONFIGURATION
# ============================================================================

DEFAULT_CONFIG = {
    'UPDATE': {
        'update_check_url': 'https://mintreu.com/api/bg-remover/version.json',
        'fallback_urls': 'https://updates.mintreu.com/bg-remover/version.json,https://cdn.mintreu.com/bg-remover/version.json',
        'update_check_timeout': '10',
        'download_timeout': '300',
        'auto_check_updates': 'true',
        'background_update_check': 'true',
    },
    'DOWNLOAD': {
        'download_base_url': 'https://mintreu.com/downloads/bg-remover',
        'download_folder': '',
    },
    'APPLICATION': {
        'app_name': 'Mintreu BG Remover',
        'company_name': 'Mintreu',
        'company_website': 'https://mintreu.com',
        'support_email': 'contact@mintreu.com',
        'support_url': 'https://mintreu.com/support',
    },
    'MODELS': {
        'model_base_url': 'https://huggingface.co',
        'auto_download_models': 'true',
    },
    'LOGGING': {
        'log_level': 'INFO',
        'enable_file_logging': 'true',
        'log_file': '',
    },
    'ADVANCED': {
        'default_workers': '0',
        'enable_gpu': 'false',
        'cache_directory': '',
        'output_directory': '',
    }
}

# ============================================================================
# CONFIGURATION LOADER
# ============================================================================

class AppConfig:
    """Application configuration loader."""

    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize configuration loader.

        Args:
            config_file: Path to config.ini file. If None, searches in:
                1. Same directory as script/exe
                2. User's home directory (.mintreu_bg_remover/)
        """
        self.config = ConfigParser()

        # Load defaults
        self.config.read_dict(DEFAULT_CONFIG)

        # Find and load config file
        if config_file is None:
            config_file = self._find_config_file()

        if config_file and config_file.exists():
            logger.info(f"Loading configuration from: {config_file}")
            try:
                self.config.read(config_file, encoding='utf-8')
                logger.info("Configuration loaded successfully")
            except Exception as e:
                logger.warning(f"Could not load config file: {e}. Using defaults.")
        else:
            logger.info("No config file found. Using default configuration.")

        self.config_file = config_file

    def _find_config_file(self) -> Optional[Path]:
        """Find config.ini file in standard locations."""

        # Get base path (works for script and frozen exe)
        if getattr(sys, 'frozen', False):
            if hasattr(sys, '_MEIPASS'):
                base_path = Path(sys._MEIPASS)
            else:
                base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent

        # Search locations
        search_paths = [
            base_path / "config.ini",
            Path.home() / ".mintreu_bg_remover" / "config.ini",
            Path(os.getcwd()) / "config.ini",
        ]

        for path in search_paths:
            if path.exists():
                return path

        # If not found, use the base path location
        return base_path / "config.ini"

    def get(self, section: str, key: str, fallback: Optional[str] = None) -> str:
        """Get configuration value."""
        try:
            return self.config.get(section, key, fallback=fallback)
        except:
            return fallback or ""

    def get_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get boolean configuration value."""
        try:
            return self.config.getboolean(section, key, fallback=fallback)
        except:
            return fallback

    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        """Get integer configuration value."""
        try:
            return self.config.getint(section, key, fallback=fallback)
        except:
            return fallback

    def get_list(self, section: str, key: str, fallback: Optional[List[str]] = None) -> List[str]:
        """Get list configuration value (comma-separated)."""
        try:
            value = self.config.get(section, key)
            if value:
                return [item.strip() for item in value.split(',') if item.strip()]
            return fallback or []
        except:
            return fallback or []

    # ========================================================================
    # UPDATE CONFIGURATION
    # ========================================================================

    @property
    def update_check_url(self) -> str:
        """Get update check URL."""
        return self.get('UPDATE', 'update_check_url')

    @property
    def fallback_urls(self) -> List[str]:
        """Get fallback URLs for update checks."""
        return self.get_list('UPDATE', 'fallback_urls')

    @property
    def update_check_timeout(self) -> int:
        """Get update check timeout in seconds."""
        return self.get_int('UPDATE', 'update_check_timeout', 10)

    @property
    def download_timeout(self) -> int:
        """Get download timeout in seconds."""
        return self.get_int('UPDATE', 'download_timeout', 300)

    @property
    def auto_check_updates(self) -> bool:
        """Check if auto-update checking is enabled."""
        return self.get_bool('UPDATE', 'auto_check_updates', True)

    @property
    def background_update_check(self) -> bool:
        """Check if background update checking is enabled."""
        return self.get_bool('UPDATE', 'background_update_check', True)

    # ========================================================================
    # DOWNLOAD CONFIGURATION
    # ========================================================================

    @property
    def download_base_url(self) -> str:
        """Get base URL for downloads."""
        return self.get('DOWNLOAD', 'download_base_url')

    @property
    def download_folder(self) -> Optional[Path]:
        """Get custom download folder (or None for default)."""
        folder = self.get('DOWNLOAD', 'download_folder')
        if folder:
            return Path(folder)
        return None

    # ========================================================================
    # APPLICATION CONFIGURATION
    # ========================================================================

    @property
    def app_name(self) -> str:
        """Get application name."""
        return self.get('APPLICATION', 'app_name')

    @property
    def company_name(self) -> str:
        """Get company name."""
        return self.get('APPLICATION', 'company_name')

    @property
    def company_website(self) -> str:
        """Get company website."""
        return self.get('APPLICATION', 'company_website')

    @property
    def support_email(self) -> str:
        """Get support email."""
        return self.get('APPLICATION', 'support_email')

    @property
    def support_url(self) -> str:
        """Get support URL."""
        return self.get('APPLICATION', 'support_url')

    # ========================================================================
    # MODELS CONFIGURATION
    # ========================================================================

    @property
    def model_base_url(self) -> str:
        """Get model download base URL."""
        return self.get('MODELS', 'model_base_url')

    @property
    def auto_download_models(self) -> bool:
        """Check if auto-download of models is enabled."""
        return self.get_bool('MODELS', 'auto_download_models', True)

    # ========================================================================
    # LOGGING CONFIGURATION
    # ========================================================================

    @property
    def log_level(self) -> str:
        """Get log level."""
        return self.get('LOGGING', 'log_level', 'INFO')

    @property
    def enable_file_logging(self) -> bool:
        """Check if file logging is enabled."""
        return self.get_bool('LOGGING', 'enable_file_logging', True)

    @property
    def log_file(self) -> Optional[Path]:
        """Get custom log file path (or None for default)."""
        log_file = self.get('LOGGING', 'log_file')
        if log_file:
            return Path(log_file)
        return None

    # ========================================================================
    # ADVANCED CONFIGURATION
    # ========================================================================

    @property
    def default_workers(self) -> int:
        """Get default number of worker threads (0 = auto)."""
        return self.get_int('ADVANCED', 'default_workers', 0)

    @property
    def enable_gpu(self) -> bool:
        """Check if GPU acceleration is enabled."""
        return self.get_bool('ADVANCED', 'enable_gpu', False)

    @property
    def cache_directory(self) -> Optional[Path]:
        """Get custom cache directory (or None for default)."""
        cache_dir = self.get('ADVANCED', 'cache_directory')
        if cache_dir:
            return Path(cache_dir)
        return None

    @property
    def output_directory(self) -> Optional[Path]:
        """Get custom output directory (or None for default)."""
        output_dir = self.get('ADVANCED', 'output_directory')
        if output_dir:
            return Path(output_dir)
        return None

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def save(self, config_file: Optional[Path] = None):
        """Save current configuration to file."""
        if config_file is None:
            config_file = self.config_file or (Path(__file__).parent / "config.ini")

        try:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            logger.info(f"Configuration saved to: {config_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    def create_default_config(self, output_path: Optional[Path] = None):
        """Create default configuration file."""
        if output_path is None:
            output_path = Path(__file__).parent / "config.ini"

        # Reset to defaults
        self.config = ConfigParser()
        self.config.read_dict(DEFAULT_CONFIG)

        return self.save(output_path)

    def print_config(self):
        """Print current configuration (for debugging)."""
        print("\n" + "="*70)
        print("CURRENT CONFIGURATION")
        print("="*70)

        for section in self.config.sections():
            print(f"\n[{section}]")
            for key, value in self.config.items(section):
                print(f"  {key} = {value}")

        print("\n" + "="*70)

# ============================================================================
# GLOBAL CONFIG INSTANCE
# ============================================================================

# Create global config instance
app_config = AppConfig()

# ============================================================================
# TESTING
# ============================================================================

def test_config():
    """Test configuration loading."""
    print("Testing Configuration Loader")
    print("="*70)

    config = AppConfig()

    print(f"\nUpdate Check URL: {config.update_check_url}")
    print(f"Fallback URLs: {config.fallback_urls}")
    print(f"Update Timeout: {config.update_check_timeout}s")
    print(f"Auto-check Updates: {config.auto_check_updates}")

    print(f"\nApp Name: {config.app_name}")
    print(f"Company: {config.company_name}")
    print(f"Website: {config.company_website}")

    print(f"\nLog Level: {config.log_level}")
    print(f"Enable File Logging: {config.enable_file_logging}")

    print(f"\nConfig File: {config.config_file}")

    print("\n" + "="*70)
    print("✓ Configuration test complete!")

if __name__ == "__main__":
    test_config()
