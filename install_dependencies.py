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


def check_pip_availability():
    """Check if pip is available and install it if missing."""
    # Try different pip commands
    pip_commands = ['pip3', 'pip', f'{sys.executable} -m pip']
    
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
    print("Installing pip...")
    
    # Try to install pip using system package manager
    system = platform.system().lower()
    if system == "linux":
        # Try different package managers for pip installation
        pip_install_commands = [
            (['sudo', 'apt', 'update'], ['sudo', 'apt', 'install', '-y', 'python3-pip'], 'apt (Ubuntu/Debian)'),
            (['sudo', 'dnf', 'install', '-y', 'python3-pip'], None, 'dnf (Fedora)'),
            (['sudo', 'pacman', '-S', '--noconfirm', 'python-pip'], None, 'pacman (Arch)'),
            (['sudo', 'zypper', 'install', '-y', 'python3-pip'], None, 'zypper (openSUSE)'),
        ]
        
        for update_cmd, install_cmd, manager_name in pip_install_commands:
            manager_cmd = update_cmd[1] if update_cmd else install_cmd[1]
            if shutil.which(manager_cmd):
                print(f"Found {manager_name} package manager")
                
                if update_cmd:
                    run_command(update_cmd, f"package list update via {manager_name}", critical=False)
                
                cmd = install_cmd if install_cmd else update_cmd
                if run_command(cmd, f'python3-pip via {manager_name}', critical=False):
                    return True
        
        print("Could not install pip automatically.")
        print("Please install pip manually:")
        print("Ubuntu/Debian: sudo apt install python3-pip")
        print("Fedora: sudo dnf install python3-pip")
        print("Arch: sudo pacman -S python-pip")
        sys.exit(1)
    else:
        print("Please install pip manually for your system.")
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
    Install a Python package using pip, handling externally managed environments.
    
    Args:
        package_name (str): Name of the package to install
        description (str): Description for user feedback
    """
    # Check if we're on a system with externally managed environment
    system = platform.system().lower()
    
    if system == "linux":
        # First try system package (apt install python3-xyz)
        if package_name == 'yt-dlp' and shutil.which('apt'):
            print(f"Trying to install {description} via system package...")
            if run_command(['sudo', 'apt', 'update'], 'package list update', critical=False):
                if run_command(['sudo', 'apt', 'install', '-y', 'yt-dlp'], description + ' via apt', critical=False):
                    return True
        
        # Try pipx if available (recommended for externally managed environments)
        if shutil.which('pipx'):
            print(f"Using pipx to install {description}...")
            command = ['pipx', 'install', package_name]
            if run_command(command, description + ' via pipx', critical=False):
                return True
        else:
            # Try to install pipx first
            print("pipx not found. Attempting to install pipx...")
            if shutil.which('apt'):
                if run_command(['sudo', 'apt', 'install', '-y', 'pipx'], 'pipx package manager', critical=False):
                    # Ensure pipx is in PATH
                    pipx_path = Path.home() / '.local' / 'bin'
                    if pipx_path.exists():
                        os.environ['PATH'] = str(pipx_path) + ':' + os.environ.get('PATH', '')
                    
                    # Try pipx install again
                    command = ['pipx', 'install', package_name]
                    if run_command(command, description + ' via pipx', critical=False):
                        return True
    
    # Try standard pip installation methods
    pip_commands = ['pip3', 'pip']
    
    for pip_cmd in pip_commands:
        if shutil.which(pip_cmd):
            # First try normal install
            command = [pip_cmd, 'install', '--upgrade', package_name]
            result = run_command(command, description, critical=False)
            if result:
                return True
            
            # If that fails due to externally managed environment, try --user
            print(f"Trying user installation for {description}...")
            command = [pip_cmd, 'install', '--user', '--upgrade', package_name]
            result = run_command(command, description + ' (user install)', critical=False)
            if result:
                return True
    
    # Try with python -m pip
    print(f"Trying python -m pip for {description}...")
    command = [sys.executable, '-m', 'pip', 'install', '--upgrade', package_name]
    result = run_command(command, description, critical=False)
    if result:
        return True
    
    # Try --user with python -m pip
    print(f"Trying python -m pip --user for {description}...")
    command = [sys.executable, '-m', 'pip', 'install', '--user', '--upgrade', package_name]
    result = run_command(command, description + ' (user install)', critical=False)
    if result:
        return True
    
    # Last resort: suggest virtual environment or --break-system-packages
    print(f"✗ Failed to install {description}")
    print("\nThis system has an externally managed Python environment.")
    print("You have several options:")
    print("1. Create a virtual environment:")
    print("   python3 -m venv youtube_downloader_env")
    print("   source youtube_downloader_env/bin/activate")
    print("   pip install yt-dlp")
    print("2. Use pipx (if available):")
    print(f"   sudo apt install pipx && pipx install {package_name}")
    print("3. Use system package (Ubuntu/Debian):")
    if package_name == 'yt-dlp':
        print("   sudo apt install yt-dlp")
    print("4. Override protection (NOT RECOMMENDED):")
    print(f"   pip install --break-system-packages {package_name}")
    
    return False


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
    
    # Install python-is-python3 for Ubuntu/Debian systems to allow 'python' command
    if shutil.which('apt'):
        print("Installing python-is-python3 for 'python' command compatibility...")
        run_command(['sudo', 'apt', 'update'], 'package list update', critical=False)
        run_command(['sudo', 'apt', 'install', '-y', 'python-is-python3'], 
                   'python-is-python3 (allows python command)', critical=False)
    
    # Install yt-dlp - try multiple methods for externally managed environments
    print()
    print("Installing yt-dlp (YouTube downloader)...")
    
    # Method 1: Try system package first (most compatible with managed environments)
    if shutil.which('apt'):
        print("Attempting system package installation...")
        if run_command(['sudo', 'apt', 'install', '-y', 'yt-dlp'], 
                      'yt-dlp via apt (system package)', critical=False):
            print("✓ yt-dlp installed via system package")
        else:
            # Method 2: Try pipx installation
            print("System package failed, trying pipx...")
            if not shutil.which('pipx'):
                run_command(['sudo', 'apt', 'install', '-y', 'pipx'], 
                           'pipx package manager', critical=False)
            
            if shutil.which('pipx'):
                if run_command(['pipx', 'install', 'yt-dlp'], 
                              'yt-dlp via pipx', critical=False):
                    print("✓ yt-dlp installed via pipx")
                else:
                    # Method 3: Fall back to pip with various options
                    install_pip_package('yt-dlp', 'yt-dlp (YouTube downloader)')
            else:
                # Method 3: Fall back to pip with various options
                install_pip_package('yt-dlp', 'yt-dlp (YouTube downloader)')
    else:
        # For non-apt systems, use pip package function
        install_pip_package('yt-dlp', 'yt-dlp (YouTube downloader)')
    
    print()
    
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
    
    # Check pip availability
    check_pip_availability()
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
