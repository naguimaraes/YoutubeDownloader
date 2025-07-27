#!/usr/bin/env python3
"""
YouTube Downloader - Windows Dependency Installation Script

This script automatically installs the required dependencies for the YouTube Downloader
on Windows systems.

Dependencies installed:
- yt-dlp: YouTube downloader library
- ffmpeg: Video/audio processing tool

Usage:
    python install_dependencies.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_header():
    """Print a welcome header."""
    print("=" * 60)
    print("YouTube Downloader - Windows Dependency Installation")
    print("=" * 60)
    print()


def check_python_version():
    """Check if Python version is 3.6 or higher."""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python version: {sys.version.split()[0]}")


def check_pip_availability():
    """Check if pip is available and install it if missing."""
    # Try different pip commands
    pip_commands = ['pip', f'{sys.executable} -m pip']
    
    for pip_cmd in pip_commands:
        try:
            if ' -m ' in pip_cmd:
                # For python -m pip, split the command
                result = subprocess.run(pip_cmd.split(), 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL, 
                                      check=True)
            else:
                result = subprocess.run([pip_cmd, '--version'], 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL, 
                                      check=True)
            print(f"✓ pip is available via: {pip_cmd}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("✗ pip is not available")
    print("Please install pip manually. It should be included with Python 3.4+")
    print("If you're using an older version of Python, please update to Python 3.6+")
    sys.exit(1)


def run_command(command, description, critical=True):
    """
    Run a system command and handle errors.
    
    Args:
        command (list): Command to run as list of strings
        description (str): Description of what the command does
        critical (bool): Whether failure should exit the program
        
    Returns:
        bool: True if command succeeded, False otherwise
    """
    print(f"Installing {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✓ {description} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {description}")
        print(f"Error: {e.stderr.strip()}")
        if critical:
            sys.exit(1)
        return False
    except FileNotFoundError:
        print(f"✗ Command not found: {' '.join(command)}")
        if critical:
            print("Please install the required package manager first.")
            sys.exit(1)
        return False


def install_pip_package(package_name, description):
    """
    Install a Python package using pip on Windows.
    
    Args:
        package_name (str): Name of the package to install
        description (str): Description for user feedback
    """
    # Try pip first, then python -m pip
    pip_commands = ['pip']
    
    for pip_cmd in pip_commands:
        if shutil.which(pip_cmd):
            command = [pip_cmd, 'install', '--upgrade', package_name]
            if run_command(command, description, critical=False):
                return True
    
    # Try with python -m pip
    print(f"Trying python -m pip for {description}...")
    command = [sys.executable, '-m', 'pip', 'install', '--upgrade', package_name]
    return run_command(command, description, critical=True)


def install_windows_dependencies():
    """Install dependencies on Windows."""
    print("Installing dependencies for Windows")
    print()
    
    # Install yt-dlp
    install_pip_package('yt-dlp', 'yt-dlp (YouTube downloader)')
    
    # Check for ffmpeg
    if shutil.which('ffmpeg'):
        print("✓ ffmpeg is already installed")
    else:
        print("Installing ffmpeg...")
        # Try winget first
        if shutil.which('winget'):
            if run_command(['winget', 'install', 'ffmpeg'], 'ffmpeg via winget', critical=False):
                return
        
        # Try chocolatey
        if shutil.which('choco'):
            if run_command(['choco', 'install', 'ffmpeg', '-y'], 'ffmpeg via chocolatey', critical=False):
                return
        
        print("⚠ Could not install ffmpeg automatically.")
        print("Please install ffmpeg manually:")
        print("1. Download from: https://ffmpeg.org/download.html")
        print("2. Extract to a folder (e.g., C:\\ffmpeg)")
        print("3. Add the bin folder to your PATH environment variable")
        print("4. Or use: winget install ffmpeg")


def verify_installation():
    """Verify that all dependencies are properly installed."""
    print()
    print("Verifying installation...")
    print()
    
    # Check yt-dlp
    try:
        import yt_dlp
        print("✓ yt-dlp is available")
    except ImportError:
        print("✗ yt-dlp is not available")
        return False
    
    # Check ffmpeg
    if shutil.which('ffmpeg'):
        print("✓ ffmpeg is available")
    else:
        print("✗ ffmpeg is not available")
        return False
    
    return True


def main():
    """Main installation function for Windows."""
    print_header()
    
    # Check Python version
    check_python_version()
    
    # Check pip availability
    check_pip_availability()
    print()
    
    # Install Windows dependencies
    install_windows_dependencies()
    
    # Verify installation
    print()
    if verify_installation():
        print()
        print("=" * 60)
        print("✓ All dependencies installed successfully!")
        print("You can now run: python youtube_downloader.py")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("⚠ Some dependencies failed to install.")
        print("Please check the error messages above and install manually.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
