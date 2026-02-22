"""
Mintreu BG Remover - Professional Installer Builder
Ensures a truly standalone, self-contained executable.
Can build a portable directory or a single executable file.
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_NAME = "MintreuBgRemover"
SCRIPT_NAME = "main.py"

PROJECT_ROOT = Path(__file__).parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
MODELS_DIR = PROJECT_ROOT / "models"
ASSETS_DIR = PROJECT_ROOT / "assets"
HOOKS_DIR = PROJECT_ROOT / "hooks"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def run_command(command, description):
    """Runs a command and exits if it fails."""
    print(f"▶️  {description}...")
    try:
        # Using sys.executable ensures we use the python from the current venv
        subprocess.run([sys.executable, "-m"] + command, check=True, capture_output=True, text=True)
        print(f"✅ {description} complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {description} failed.")
        print(f"   - Return Code: {e.returncode}")
        print(f"   - STDOUT: {e.stdout}")
        print(f"   - STDERR: {e.stderr}")
        print("\n💡 Common fixes:")
        print("   1. Make sure you are in the correct virtual environment.")
        print("   2. Run 'pip install -r requirements.txt' or 'pip install pyinstaller'.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find '{sys.executable}'. Is Python installed and in your PATH?")
        sys.exit(1)

def clean_build_folders():
    """Removes old build artifacts."""
    print("\n🧹 Cleaning old build artifacts...")
    spec_file = PROJECT_ROOT / f"{APP_NAME}.spec"
    if spec_file.exists():
        spec_file.unlink()
        print(f"   - Removed {spec_file}")
        
    for folder in [BUILD_DIR, DIST_DIR]:
        if folder.exists():
            shutil.rmtree(folder)
            print(f"   - Removed {folder}/")
            
    print("✅ Cleaning complete.")

# ============================================================================
# MAIN BUILD LOGIC
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Mintreu BG Remover - Professional Builder")
    parser.add_argument(
        "--build-type", 
        choices=["dir", "file"], 
        default="dir",
        help="Type of build to produce: 'dir' for a portable directory (default), 'file' for a single executable."
    )
    args = parser.parse_args()

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║         Mintreu BG Remover - Professional Builder         ║
║          Creates a 100% standalone executable.            ║
║                  Build Type: {args.build_type.upper()}                     ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # 1. Clean previous builds
    clean_build_folders()
    
    # 2. Check for PyInstaller
    print("\n📦 Checking for PyInstaller...")
    try:
        import PyInstaller
        print(f"✓ PyInstaller found (version {PyInstaller.__version__})")
    except ImportError:
        run_command(["pip", "install", "pyinstaller"], "Installing PyInstaller")

    # 3. Define the PyInstaller command
    print(f"\n🔨 Preparing build command for '{args.build_type}' type...")
    
    icon = ASSETS_DIR / "favicon.ico"
    build_mode = "--onedir" if args.build_type == "dir" else "--onefile"
    
    pyinstaller_command = [
        "PyInstaller",
        SCRIPT_NAME,
        "--name", APP_NAME,
        build_mode,
        "--windowed",
        "--noconfirm",
        f"--icon={icon}" if icon.exists() else "",
        f"--additional-hooks-dir={HOOKS_DIR}",
        f"--add-data={MODELS_DIR}{os.pathsep}models",
        f"--add-data={ASSETS_DIR}{os.pathsep}assets",
        "--collect-all", "PySide6",
        "--collect-all", "onnxruntime",
        "--collect-all", "cv2",
        "--collect-all", "PIL",
        "--collect-all", "numpy",
        "--collect-all", "requests",
        "--collect-all", "tqdm",
        "--hidden-import", "PySide6.QtOpenGL",
        "--hidden-import", "PySide6.QtSvg",
        "--hidden-import", "onnxruntime.capi._pybind_state",
        "--hidden-import", "PIL._tkinter_finder",
        "--copy-metadata", "certifi",
        "--collect-data", "certifi",
    ]
    
    pyinstaller_command = [arg for arg in pyinstaller_command if arg]
    
    # 4. Run the build
    print("⏳ Build process starting. This can take 5-10 minutes...")
    run_command(pyinstaller_command, "Building executable")
    
    # 5. Post-build summary
    print("\n🎉 BUILD SUCCEEDED! 🎉")
    
    if args.build_type == "dir":
        output_path = DIST_DIR / APP_NAME
        final_exe = output_path / f"{APP_NAME}.exe"
        if final_exe.exists():
            total_size_bytes = sum(f.stat().st_size for f in output_path.rglob('*') if f.is_file())
            total_size_mb = total_size_bytes / (1024 * 1024)
            
            print(f"\n📁 Standalone application directory created in: {output_path}")
            print(f"   - Main executable: {final_exe.name}")
            print(f"   - Total size: {total_size_mb:.1f} MB")
            print("\n🚀 To run your application:")
            print(f"   1. Open the folder: {output_path}")
            print(f"   2. Double-click on '{APP_NAME}.exe'")
        else:
            print(f"⚠️  Could not find final executable at {final_exe}")
    else: # 'file'
        final_exe = DIST_DIR / f"{APP_NAME}.exe"
        if final_exe.exists():
            size_mb = final_exe.stat().st_size / (1024 * 1024)
            print(f"\n📦 Single-file executable created in: {DIST_DIR}")
            print(f"   - Executable: {final_exe.name}")
            print(f"   - Size: {size_mb:.1f} MB")
            print("\n🚀 To run your application, double-click the .exe file.")
        else:
            print(f"⚠️  Could not find final executable at {final_exe}")

if __name__ == "__main__":
    main()
