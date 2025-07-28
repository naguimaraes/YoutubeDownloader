# YouTube Downloader

A DIY YouTube video and audio downloader for Windows built with Python made in one night. Basically works as a `yt-dlp` wrapper with friendly interface and easy use. This project was created to provide a simple solution for downloading YouTube content without relying on the currently available websites, that often require subscriptions or are filled with ads and scams.

## Features

- `yt-dlp` integration for downloading videos and audio;
- Windows support with automated dependency installation;
- Allow the user to choose video/audio quality (720p and above for videos);
- Shows estimated file size for downloads;
- Estimated file size and download progress.

## Automatic Installation (Recommended)

1. First, verify that Python and pip are installed on your system:

   ```bash
   python --version
   pip --version
   ```

   If either command fails, install Python from [python.org](https://python.org) (pip is included with Python).

2. Download or clone this repository and navigate to the project directory:

   ```bash
   git clone https://github.com/naguimaraes/YoutubeDownloader.git
   cd YoutubeDownloader
   ```

3. Run the automatic dependency installer:

   ```bash
   python install_dependencies.py
   ```

4. Run the main script:

   ```bash
   python youtube_downloader.py
   ```

If you prefer to install dependencies manually, see the [Manual Installation](#manual-installation) section below. If you have already downloaded the dependencies, you can skip to the [Usage](#usage) section.

## Manual Installation

### Prerequisites

1. **Python 3.6 or higher**
2. **yt-dlp** (YouTube downloader library)
3. **ffmpeg** (for audio conversion)

### Windows Installation

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

## Usage

### Help

```bash
python youtube_downloader.py -h
# or
python youtube_downloader.py --help
```

This will display the help message with usage instructions:

```bash
usage: youtube_downloader.py [-h] [--audio-only]

Download YouTube videos or audio

options:
  -h, --help        show this help message and exit
  --audio-only, -a  Download only audio (MP3 format)

Examples:
  python youtube_downloader.py                  # Download video
  python youtube_downloader.py --audio-only     # Download audio only
```

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
python youtube_downloader.py -a
# or
python youtube_downloader.py --audio-only
```

This will:

1. Prompt for a YouTube URL
2. Show available audio formats
3. Let you choose the desired audio quality
4. Download and convert to MP3

## Example Execution

```terminal
> python youtube_downloader.py
Enter the YouTube video URL: https://youtu.be/iv-5mZ_9CPY?si=c6vYYg4B9WVDO_vP        
                                                                          
Title: But how do AI videos actually work? | Guest video by @WelchLabsVideo
Channel: 3Blue1Brown
Duration: 39:48

+----+------------+--------+----------+-----------+----------------+
|                      AVAILABLE VIDEO FORMATS                     |
+----+------------+--------+----------+-----------+----------------+
| #  | Resolution |  FPS   |  Codec   | Container | Estimated Size |
+----+------------+--------+----------+-----------+----------------+
| 1  | 2160p      | 30     | av01     | mp4       | 1.13 GB        |
| 2  | 2160p      | 30     | vp9      | webm      | 1.8 GB         |
| 3  | 1440p      | 30     | av01     | mp4       | 557.8 MB       |
| 4  | 1440p      | 30     | vp9      | webm      | 709.36 MB      |
| 5  | 1080p      | 30     | av01     | mp4       | 189.64 MB      |
| 6  | 1080p      | 30     | vp9      | webm      | 234.76 MB      |
| 7  | 1080p      | 30     | avc1     | mp4       | 293.44 MB      |
| 8  | 720p       | 30     | avc1     | mp4       | 114.36 MB      |
| 9  | 720p       | 30     | av01     | mp4       | 124.41 MB      |
| 10 | 720p       | 30     | vp9      | webm      | 147.2 MB       |
+----+------------+--------+----------+-----------+----------------+

Select the format by number: 10

Downloading format 247 to: C:\Users\nathan\Downloads\Youtube Downloads
[download] 100% of  110.34MiB in 00:00:10 at 10.39MiB/s
[download] 100% of   33.24MiB in 00:00:04 at 6.78MiB/s

Download complete!
```

## Output

Downloaded files are saved to:

- **Windows**: `C:\Users\{username}\Downloads\Youtube Downloads\`

## Troubleshooting

### "yt-dlp not found"

Install yt-dlp using pip:

```cmd
pip install yt-dlp
```

### "ffmpeg not found"

Install ffmpeg for Windows:

- **Windows**: `winget install ffmpeg`
- Or download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Permission errors

If you get permission errors, try running the command prompt as administrator.

## License

This project is open source and available under the MIT License.
