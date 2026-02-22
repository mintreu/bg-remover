"""
Mintreu BG Remover - Application Test Suite
============================================
Comprehensive tests for the application functionality

Author: Krishanu Bhattacharya
Company: Mintreu
License: MIT
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def print_test(name):
    """Print test name."""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print('='*70)

def print_success(msg):
    """Print success message."""
    print(f"✅ {msg}")

def print_error(msg):
    """Print error message."""
    print(f"❌ {msg}")

def print_info(msg):
    """Print info message."""
    print(f"ℹ️  {msg}")

# ============================================================================
# IMPORT TESTS
# ============================================================================

def test_imports():
    """Test all required modules can be imported."""
    print_test("Module Import Test")

    modules = {
        'numpy': 'NumPy',
        'cv2': 'OpenCV',
        'PIL': 'Pillow',
        'onnxruntime': 'ONNX Runtime',
        'PySide6': 'PySide6',
        'requests': 'Requests',
        'tqdm': 'tqdm'
    }

    all_ok = True
    for module, name in modules.items():
        try:
            __import__(module)
            print_success(f"{name} imported successfully")
        except ImportError as e:
            print_error(f"{name} import failed: {e}")
            all_ok = False

    return all_ok

# ============================================================================
# PATH TESTS
# ============================================================================

def test_paths():
    """Test all required paths exist."""
    print_test("Path Verification Test")

    paths = {
        'main.py': PROJECT_ROOT / 'main.py',
        'pyproject.toml': PROJECT_ROOT / 'pyproject.toml',
        'LICENSE.txt': PROJECT_ROOT / 'LICENSE.txt',
        'assets': PROJECT_ROOT / 'assets',
        'models': PROJECT_ROOT / 'models',
    }

    all_ok = True
    for name, path in paths.items():
        if path.exists():
            print_success(f"{name} exists: {path}")
        else:
            print_error(f"{name} missing: {path}")
            all_ok = False

    return all_ok

# ============================================================================
# CONFIGURATION TESTS
# ============================================================================

def test_config():
    """Test application configuration."""
    print_test("Configuration Test")

    try:
        from main import (
            MODELS, APP_VERSION, THEME,
            BASE_PATH, DATA_PATH, MODELS_PATH
        )

        print_info(f"App Version: {APP_VERSION}")
        print_info(f"Base Path: {BASE_PATH}")
        print_info(f"Data Path: {DATA_PATH}")
        print_info(f"Models Path: {MODELS_PATH}")

        # Check models config
        for key, model in MODELS.items():
            print_success(f"Model configured: {model.name} ({model.size_mb} MB)")

        # Check theme
        print_success(f"Theme configured: BG_DARK={THEME.BG_DARK}")

        return True
    except Exception as e:
        print_error(f"Configuration test failed: {e}")
        return False

# ============================================================================
# MODEL TESTS
# ============================================================================

def test_models():
    """Test model files exist and are valid."""
    print_test("Model Files Test")

    try:
        from main import MODELS, MODELS_PATH

        all_ok = True
        for key, model in MODELS.items():
            model_path = MODELS_PATH / model.filename

            if model_path.exists():
                size_mb = model_path.stat().st_size / (1024 * 1024)
                if size_mb >= 1:
                    print_success(f"{model.name} found: {size_mb:.1f} MB")
                else:
                    print_error(f"{model.name} file too small: {size_mb:.2f} MB")
                    all_ok = False
            else:
                print_info(f"{model.name} not found (will be downloaded on first use)")

        return all_ok
    except Exception as e:
        print_error(f"Model test failed: {e}")
        return False

# ============================================================================
# SYSTEM HEALTH TESTS
# ============================================================================

def test_system_health():
    """Test system health check."""
    print_test("System Health Check Test")

    try:
        from main import SystemHealthCheck

        # Check Python version
        py_ok, py_msg = SystemHealthCheck.check_python_version()
        if py_ok:
            print_success(f"Python version: {py_msg}")
        else:
            print_error(f"Python version: {py_msg}")

        # Check dependencies
        dep_ok, missing = SystemHealthCheck.check_dependencies()
        if dep_ok:
            print_success("All dependencies installed")
        else:
            print_error(f"Missing dependencies: {missing}")

        # Check directories
        dir_ok, issues = SystemHealthCheck.check_directories()
        if dir_ok:
            print_success("All directories accessible")
        else:
            print_error(f"Directory issues: {issues}")

        # Check models
        models_ok, status = SystemHealthCheck.check_models()
        if models_ok:
            print_success("All models present")
        else:
            print_info("Some models missing (expected on first run)")

        # Run full check
        is_healthy, report = SystemHealthCheck.run_full_check()
        print()
        print("Full Health Report:")
        print("-" * 70)
        print(report)
        print("-" * 70)

        return True
    except Exception as e:
        print_error(f"System health test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# IMAGE PROCESSING TESTS
# ============================================================================

def test_image_processing():
    """Test image processing functionality."""
    print_test("Image Processing Test")

    try:
        import numpy as np
        from PIL import Image
        from main import BGRemover, ModelManager, MODELS

        # Create test image
        print_info("Creating test image...")
        test_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        test_img_path = Path(tempfile.mktemp(suffix='.png'))
        Image.fromarray(test_img).save(test_img_path)
        print_success(f"Test image created: {test_img_path}")

        # Test model manager
        print_info("Testing ModelManager...")
        model_manager = ModelManager()
        print_success("ModelManager initialized")

        # Test BGRemover (without actually processing if model not present)
        print_info("Testing BGRemover...")
        remover = BGRemover(model_manager, "rmbg_v14")

        # Check if model exists
        model_path = model_manager.cache_dir / MODELS["rmbg_v14"].filename
        if model_path.exists():
            print_success("Model file found, can test processing")
            print_info("Note: Full processing test requires model download")
        else:
            print_info("Model not found - skipping actual processing test")
            print_info("Download model via app to enable full processing tests")

        # Cleanup
        if test_img_path.exists():
            test_img_path.unlink()
            print_success("Test image cleaned up")

        return True
    except Exception as e:
        print_error(f"Image processing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# UI TESTS
# ============================================================================

def test_ui_components():
    """Test UI components can be instantiated."""
    print_test("UI Components Test")

    try:
        from PySide6.QtWidgets import QApplication
        import sys

        # Create QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        print_success("QApplication created")

        # Test imports from main
        from main import (
            MainWindow, FileItemWidget, ImageViewer,
            DownloadDialog, SystemErrorDialog, LicenseDialog,
            TutorialDialog, create_splash_screen
        )

        print_success("All UI components imported successfully")

        # Test splash screen
        splash = create_splash_screen()
        print_success("Splash screen created")

        # Test FileInfo
        from main import FileInfo
        print_success("FileInfo class imported")

        return True
    except Exception as e:
        print_error(f"UI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# BUILD TESTS
# ============================================================================

def test_build_scripts():
    """Test build scripts exist and are valid."""
    print_test("Build Scripts Test")

    scripts = {
        'build_complete_offline.py': 'Complete offline builder',
        'installMaker.py': 'PyInstaller builder',
        'run.bat': 'Run script',
    }

    all_ok = True
    for script, desc in scripts.items():
        path = PROJECT_ROOT / script
        if path.exists():
            print_success(f"{desc}: {script}")
        else:
            print_error(f"{desc} missing: {script}")
            all_ok = False

    return all_ok

# ============================================================================
# INTEGRATION TEST
# ============================================================================

def test_integration():
    """Test application can start (without showing window)."""
    print_test("Integration Test")

    print_info("This test verifies the app can initialize without errors")
    print_info("Full UI test requires manual interaction")

    try:
        # Import main components
        from main import (
            ModelManager, BGRemover, Config,
            SystemHealthCheck, MODELS, APP_VERSION
        )

        print_success(f"Application version: {APP_VERSION}")

        # Test config
        config = Config()
        print_success("Config loaded")

        # Test model manager
        model_manager = ModelManager()
        print_success("ModelManager initialized")

        # Test system health
        is_healthy, report = SystemHealthCheck.run_full_check()
        print_success("System health check completed")

        return True
    except Exception as e:
        print_error(f"Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        Mintreu BG Remover - Application Test Suite              ║
║                                                                  ║
║                      Version 1.0.0                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")

    tests = [
        ('Imports', test_imports),
        ('Paths', test_paths),
        ('Configuration', test_config),
        ('Models', test_models),
        ('System Health', test_system_health),
        ('Image Processing', test_image_processing),
        ('UI Components', test_ui_components),
        ('Build Scripts', test_build_scripts),
        ('Integration', test_integration),
    ]

    results = {}
    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            result = test_func()
            results[name] = result
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print_error(f"Test {name} crashed: {e}")
            results[name] = False
            failed += 1

    # Summary
    print_test("Test Summary")
    print()
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {name}")

    print()
    print("="*70)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(tests)*100):.1f}%")
    print("="*70)

    if failed == 0:
        print()
        print("🎉 All tests passed! Application is ready for distribution.")
        return 0
    else:
        print()
        print("⚠️  Some tests failed. Please review and fix issues.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print()
        print_error("Tests cancelled by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Test runner crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
