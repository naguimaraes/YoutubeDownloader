# YouTube Downloader

A cross-platform YouTube video and audio downloader built with Python and yt-dlp.

## Features

- Download YouTube videos in various quality options (720p and above)
- Download audio-only in MP3 format
- Cross-platform support (Windows, Ubuntu/Linux, macOS)
- Animated loading indicators
- Clean, formatted output tables
- Automatic dependency checking
- Refactored, well-documented code

## Quick Start

### Automatic Installation (Recommended)

1. Download or clone this repository
2. Run the automatic dependency installer:

   ```bash
   python install_dependencies.py
   ```

   This will automatically install all required dependencies for your operating system.

3. Run the downloader:

   ```bash
   python youtube_downloader.py
   ```

If you prefer to install dependencies manually, see the [Manual Installation](#manual-installation) section below.

## Manual Installation

### Prerequisites

1. **Python 3.6 or higher**
2. **yt-dlp** (YouTube downloader library)
3. **ffmpeg** (for audio conversion)

### Windows

1. Install Python from [python.org](https://python.org)
2. Install dependencies:

   ```cmd
   pip install yt-dlp
   ```
  
3. Install ffmpeg:

   ```cmd
   winget install ffmpeg
   ```

   Or download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Ubuntu/Linux

1. Install Python and pip:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. Install yt-dlp:

   ```bash
   pip3 install yt-dlp
   # or
   sudo apt install yt-dlp
   ```

3. Install ffmpeg:

   ```bash
   sudo apt install ffmpeg
   ```

### macOS

1. Install Python (if not already installed):

   ```bash
   brew install python
   ```

2. Install dependencies:

   ```bash
   pip3 install yt-dlp
   brew install ffmpeg
   ```

## Usage

### Download Video

```bash
python youtube_downloader.py
```

This will:

1. Prompt for a YouTube URL
2. Show available video formats (720p and above)
3. Let you choose the desired quality
4. Download the video with audio merged

### Download Audio Only

```bash
python youtube_downloader.py --audio-only
# or
python youtube_downloader.py -a
```

This will:

1. Prompt for a YouTube URL
2. Show available audio formats
3. Let you choose the desired audio quality
4. Download and convert to MP3

## Examples

```bash
# Download video (interactive mode)
python youtube_downloader.py

# Download audio only (interactive mode)
python youtube_downloader.py --audio-only

# Show help
python youtube_downloader.py --help
```

## Output

Downloaded files are saved to:

- **Windows**: `C:\Users\{username}\Downloads\Youtube Downloads\`
- **Linux**: `~/Downloads/Youtube Downloads/` (or `~/Youtube Downloads/` if Downloads folder doesn't exist)
- **macOS**: `~/Downloads/Youtube Downloads/`

## Troubleshooting

### "yt-dlp not found"

Install yt-dlp using pip:

```bash
pip install yt-dlp  # Windows
pip3 install yt-dlp  # Linux/macOS
```

### "ffmpeg not found"

Install ffmpeg for your system:

- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **Fedora**: `sudo dnf install ffmpeg`
- **Arch**: `sudo pacman -S ffmpeg`
- **Windows**: `winget install ffmpeg`
- **macOS**: `brew install ffmpeg`

### Permission errors (Linux)

If you get permission errors, you might need to use `sudo` or install in user space:

```bash
pip3 install --user yt-dlp
```

## License

This project is open source and available under the MIT License.
