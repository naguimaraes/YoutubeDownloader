#!/usr/bin/env python3
"""
YouTube Downloader - Dependency Installation Script

This script automatically installs the required dependencies for the YouTube Downloader
on Windows, Linux (Ubuntu/Debian), and macOS systems.

Dependencies installed:
- yt-dlp: YouTube downloader library
- ffmpeg: Video/audio processing tool

Usage:
    python install_dependencies.py
    python3 install_dependencies.py  (on Linux/macOS)
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


def print_header():
    """Print a welcome header."""
    print("=" * 60)
    print("YouTube Downloader - Dependency Installation")
    print("=" * 60)
    print()


def check_python_version():
    """Check if Python version is 3.6 or higher."""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python version: {sys.version.split()[0]}")


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
    Install a Python package using pip.
    
    Args:
        package_name (str): Name of the package to install
        description (str): Description for user feedback
    """
    # Try pip3 first, then pip
    pip_commands = ['pip3', 'pip']
    
    for pip_cmd in pip_commands:
        if shutil.which(pip_cmd):
            command = [pip_cmd, 'install', '--upgrade', package_name]
            if run_command(command, description, critical=False):
                return True
    
    # If both fail, try with python -m pip
    command = [sys.executable, '-m', 'pip', 'install', '--upgrade', package_name]
    return run_command(command, description, critical=True)


def install_windows_dependencies():
    """Install dependencies on Windows."""
    print("Detected Windows system")
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


def install_linux_dependencies():
    """Install dependencies on Linux."""
    print("Detected Linux system")
    print()
    
    # Install yt-dlp
    install_pip_package('yt-dlp', 'yt-dlp (YouTube downloader)')
    
    # Install ffmpeg using system package manager
    # Try different package managers
    package_managers = [
        (['sudo', 'apt', 'update'], ['sudo', 'apt', 'install', '-y', 'ffmpeg'], 'apt (Ubuntu/Debian)'),
        (['sudo', 'dnf', 'install', '-y', 'ffmpeg'], None, 'dnf (Fedora)'),
        (['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg'], None, 'pacman (Arch)'),
        (['sudo', 'zypper', 'install', '-y', 'ffmpeg'], None, 'zypper (openSUSE)'),
    ]
    
    for update_cmd, install_cmd, manager_name in package_managers:
        # Check if the package manager exists
        manager_cmd = update_cmd[1] if update_cmd else install_cmd[1]
        if shutil.which(manager_cmd):
            print(f"Found {manager_name} package manager")
            
            # Run update command if provided
            if update_cmd:
                run_command(update_cmd, f"package list update via {manager_name}", critical=False)
            
            # Install ffmpeg
            cmd = install_cmd if install_cmd else update_cmd
            if run_command(cmd, f'ffmpeg via {manager_name}', critical=False):
                return
    
    print("⚠ Could not install ffmpeg automatically.")
    print("Please install ffmpeg manually using your system's package manager:")
    print("Ubuntu/Debian: sudo apt install ffmpeg")
    print("Fedora: sudo dnf install ffmpeg")
    print("Arch: sudo pacman -S ffmpeg")


def install_macos_dependencies():
    """Install dependencies on macOS."""
    print("Detected macOS system")
    print()
    
    # Install yt-dlp
    install_pip_package('yt-dlp', 'yt-dlp (YouTube downloader)')
    
    # Install ffmpeg using Homebrew
    if shutil.which('brew'):
        run_command(['brew', 'install', 'ffmpeg'], 'ffmpeg via Homebrew')
    else:
        print("⚠ Homebrew not found.")
        print("Please install Homebrew first:")
        print('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
        print("Then run: brew install ffmpeg")


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
    """Main installation function."""
    print_header()
    
    # Check Python version
    check_python_version()
    print()
    
    # Detect operating system and install dependencies
    system = platform.system().lower()
    
    if system == "windows":
        install_windows_dependencies()
    elif system == "linux":
        install_linux_dependencies()
    elif system == "darwin":  # macOS
        install_macos_dependencies()
    else:
        print(f"Unsupported operating system: {system}")
        print("Please install dependencies manually:")
        print("- yt-dlp: pip install yt-dlp")
        print("- ffmpeg: See https://ffmpeg.org/download.html")
        sys.exit(1)
    
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
