"""
YouTube Downloader - Windows YouTube video and audio downloader
Built with Python and yt-dlp

Features:
- Download YouTube videos in various quality options (720p and above)
- Download audio-only in MP3 format
- Windows support
- Animated loading indicators
- Clean, formatted output tables
- Automatic dependency checking
"""

import os
import sys
import time
import threading
import argparse
import subprocess
from pathlib import Path
import yt_dlp

class LoadingAnimation:
    """
    A thread-based loading animation that displays animated dots
    while background operations are running.
    """
    
    def __init__(self, message="Fetching options"):
        """
        Initialize the loading animation.
        
        Args:
            message (str): The base message to display during loading
        """
        self.message = message
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the loading animation in a separate thread."""
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True  # Dies when main thread dies
        self.thread.start()
    
    def stop(self):
        """Stop the loading animation and clear the line."""
        self.running = False
        if self.thread:
            self.thread.join()
        # Clear the loading line by overwriting with spaces
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()
    
    def _animate(self):
        """
        Internal method that handles the animation loop.
        Cycles through 0-3 dots every 0.5 seconds.
        """
        dots = 0
        while self.running:
            dots = (dots + 1) % 4
            loading_text = self.message + '.' * dots + ' ' * (3 - dots)
            sys.stdout.write(f'\r{loading_text}')
            sys.stdout.flush()
            time.sleep(0.5)

def check_dependencies():
    """
    Check if required dependencies (yt-dlp and ffmpeg) are available.
    Provides installation instructions for missing dependencies on Windows.
    """
    # Check for yt-dlp library
    try:
        import yt_dlp
    except ImportError:
        print("Error: yt-dlp is not installed.")
        print("Please install it using:")
        print("  pip install yt-dlp")
        sys.exit(1)
    
    # Check for ffmpeg (required for audio conversion and video merging)
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: ffmpeg is not installed or not in PATH.")
        print("Audio conversion may not work properly.")
        print("To install ffmpeg:")
        print("  Download from: https://ffmpeg.org/download.html")
        print("  Or use: winget install ffmpeg")
        print()

def get_downloads_folder():
    """
    Get the Windows downloads folder path.
    
    Returns:
        str: Path to the downloads folder where files will be saved
    """
    # Windows: Use Downloads/Youtube Downloads
    return str(Path.home() / "Downloads" / "Youtube Downloads")


# Utility Functions
def format_filesize(bytesize):
    """
    Convert bytes to MB with 2 decimal places.
    
    Args:
        bytesize (int): Size in bytes
        
    Returns:
        str: Formatted size string (e.g., "125.50 MB")
    """
    return f"{round(bytesize / (1024 * 1024), 2)} MB" if bytesize else "Unknown"


def format_duration(seconds):
    """
    Convert seconds to HH:MM:SS or MM:SS format.
    
    Args:
        seconds (int): Duration in seconds
        
    Returns:
        str: Formatted duration string
    """
    if not seconds:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def get_best_audio_size(formats):
    """
    Get the file size of the best available audio format for size estimation.
    
    Args:
        formats (list): List of all available formats
        
    Returns:
        int: File size of the best audio format in bytes
    """
    # Filter for audio-only formats with known file sizes
    audio_formats = [
        f for f in formats
        if f.get('acodec') != 'none' and f.get('vcodec') == 'none'
        and f.get('filesize')
    ]
    
    if audio_formats:
        # Find the best quality audio (highest bitrate)
        best_audio = max(audio_formats, key=lambda x: x.get('abr', 0) or 0)
        return best_audio.get('filesize', 0)
    return 0


# Table Display Functions
def _print_video_formats_table(formats, best_audio_size):
    """
    Print a formatted table of video formats.
    
    Args:
        formats (list): List of video formats to display
        best_audio_size (int): Size of best audio format for total size calculation
    """
    print("+----+------------+--------+----------+-----------+----------------+")
    print("|                      AVAILABLE VIDEO FORMATS                     |")
    print("+----+------------+--------+----------+-----------+----------------+")
    print("| #  | Resolution |  FPS   |  Codec   | Container | Estimated Size |")
    print("+----+------------+--------+----------+-----------+----------------+")

    for i, format_info in enumerate(formats):
        # Extract and format resolution
        res = format_info.get('format_note') or format_info.get('height') or "?"
        if isinstance(res, int):
            res = f"{res}p"
            
        # Extract format details
        fps = str(format_info.get('fps', '?'))
        codec = format_info.get('vcodec', '?').split('.')[0]  # Get main codec name
        container = format_info.get('ext', '?')
        
        # Calculate total estimated size (video + audio)
        video_size = format_info.get('filesize', 0)
        total_size = video_size + best_audio_size
        size_str = format_filesize(total_size)
        
        # Print formatted row
        print(f"| {str(i+1).ljust(2)} | {res.ljust(10)} | {fps.ljust(6)} | {codec.ljust(8)} | {container.ljust(9)} | {size_str.ljust(14)} |")

    print("+----+------------+--------+----------+-----------+----------------+")


def _print_audio_formats_table(formats):
    """
    Print a formatted table of audio formats.
    
    Args:
        formats (list): List of audio formats to display
    """
    print("+----+-------------+----------+-----------+----------------+")
    print("|                 AVAILABLE AUDIO FORMATS                  |")
    print("+----+-------------+----------+-----------+----------------+")
    print("| #  |   Quality   |  Codec   | Container |      Size      |")
    print("+----+-------------+----------+-----------+----------------+")

    for i, format_info in enumerate(formats):
        # Extract format details
        quality = f"{format_info.get('abr', '?')}kbps" if format_info.get('abr') else "Unknown"
        codec = format_info.get('acodec', '?').split('.')[0]  # Get main codec name
        container = format_info.get('ext', '?')
        size = format_filesize(format_info.get('filesize'))
        
        # Print formatted row
        print(f"| {str(i+1).ljust(2)} | {quality.ljust(11)} | {codec.ljust(8)} | {container.ljust(9)} | {size.ljust(14)} |")

    print("+----+-------------+----------+-----------+----------------+")


# Format Listing Functions
def list_formats(url, loading_animation=None):
    """
    Extract and display available video formats from a YouTube URL.
    
    Args:
        url (str): YouTube video URL
        loading_animation (LoadingAnimation, optional): Animation to stop when done
        
    Returns:
        list: List of filtered video formats, or empty list on error
    """
    # Configure yt-dlp options for format extraction
    ydl_opts = {
        'quiet': True,  # Suppress verbose output
        'no_warnings': True,  # Suppress warnings during format extraction
        'skip_download': True,  # Only extract metadata, don't download
        'forcejson': True,  # Force JSON output format
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract video information and available formats
            info = ydl.extract_info(url, download=False)
            formats = info['formats']

            # Stop loading animation before showing results
            if loading_animation:
                loading_animation.stop()

            # Get estimated audio size for total size calculation
            best_audio_size = get_best_audio_size(formats)

            # Filter formats based on quality and compatibility criteria
            filtered = [
                f for f in formats
                if f.get('vcodec') != 'none'  # Must have video codec
                and f.get('height')  # Must have height information
                and f.get('ext') in ['mp4', 'webm']  # Compatible containers
                and f.get('height', 0) >= 720  # Only 720p or higher
                and f.get('filesize')  # Only formats with known file size
            ]

            # Sort by quality (height) descending, then by file size ascending
            # This ensures best quality appears first, with smallest file size for same quality
            filtered.sort(key=lambda x: (-x.get('height', 0), x.get('filesize', 0)))

            # Display video information
            print(f"\nTitle: {info.get('title')}")
            duration = info.get('duration')
            if duration:
                print(f"Duration: {format_duration(duration)}")
            print()
            
            # Display formatted table of available formats
            _print_video_formats_table(filtered, best_audio_size)

            return filtered
            
        except Exception as e:
            if loading_animation:
                loading_animation.stop()
            print(f"\nError retrieving formats: {e}")
            return []


def list_audio_formats(url, loading_animation=None):
    """
    Extract and display available audio formats from a YouTube URL.
    
    Args:
        url (str): YouTube video URL
        loading_animation (LoadingAnimation, optional): Animation to stop when done
        
    Returns:
        list: List of filtered audio formats, or empty list on error
    """
    # Configure yt-dlp options for format extraction
    ydl_opts = {
        'quiet': True,  # Suppress verbose output
        'no_warnings': True,  # Suppress warnings during format extraction
        'skip_download': True,  # Only extract metadata, don't download
        'forcejson': True,  # Force JSON output format
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract video information and available formats
            info = ydl.extract_info(url, download=False)
            formats = info['formats']

            # Stop loading animation before showing results
            if loading_animation:
                loading_animation.stop()

            # Filter for audio-only formats with quality information
            filtered = [
                f for f in formats
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none'  # Audio only
                and f.get('filesize')  # Only formats with known file size
                and f.get('abr')  # Only formats with bitrate info
            ]

            # Sort by bitrate descending (best quality first), then by file size ascending
            filtered.sort(key=lambda x: (-x.get('abr', 0), x.get('filesize', 0)))

            # Display video information
            print(f"\nTitle: {info.get('title')}")
            duration = info.get('duration')
            if duration:
                print(f"Duration: {format_duration(duration)}")
            print()
            
            # Display formatted table of available audio formats
            _print_audio_formats_table(filtered)

            return filtered
            
        except Exception as e:
            if loading_animation:
                loading_animation.stop()
            print(f"\nError retrieving audio formats: {e}")
            return []


# Download Functions
def download_selected_format(url, format_id):
    """
    Download a specific video format with audio merged.
    
    Args:
        url (str): YouTube video URL
        format_id (str): Format ID of the selected video quality
    """
    downloads_path = get_downloads_folder()
    
    # Configure yt-dlp options for video download
    ydl_opts = {
        'quiet': True,  # Suppress intermediate output
        'no_warnings': True,  # Suppress warnings
        'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),  # Output filename template
        'format': f"{format_id}+bestaudio/best",  # Download video + best audio
        'merge_output_format': 'mp4',  # Merge to MP4 container
        'postprocessor_args': [
            '-c:v', 'copy',  # Keep video without re-encoding (faster)
            '-c:a', 'aac'    # Convert audio to AAC (compatible)
        ]
    }

    # Create download directory if it doesn't exist
    os.makedirs(downloads_path, exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"\nDownloading format {format_id} to: {downloads_path}")
            ydl.download([url])
            print("\nDownload complete!")
        except Exception as e:
            print(f"\nDownload failed: {e}")


def download_selected_audio(url, format_id):
    """
    Download a specific audio format and convert to MP3.
    
    Args:
        url (str): YouTube video URL
        format_id (str): Format ID of the selected audio quality
    """
    downloads_path = get_downloads_folder()
    
    # Configure yt-dlp options for audio download
    ydl_opts = {
        'quiet': True,  # Suppress intermediate output
        'no_warnings': True,  # Suppress warnings
        'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),  # Output filename template
        'format': format_id,  # Download specific audio format
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract/convert audio
            'preferredcodec': 'mp3',  # Convert to MP3
            'preferredquality': '192',  # Set MP3 quality to 192 kbps
        }],
    }

    # Create download directory if it doesn't exist
    os.makedirs(downloads_path, exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"\nDownloading audio format {format_id} to: {downloads_path}")
            ydl.download([url])
            print("\nAudio download complete!")
        except Exception as e:
            print(f"\nAudio download failed: {e}")


def download_audio_only(url):
    downloads_path = get_downloads_folder()
    ydl_opts = {
        'quiet': True,  # Suppress intermediate output
        'no_warnings': True,  # Suppress warnings
        'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"\nDownloading audio to: {downloads_path}")
            ydl.download([url])
            print("\nAudio download complete!")
        except Exception as e:
            print(f"\nAudio download failed: {e}")

def main():
    """
    Main application entry point.
    Handles command line arguments, user input validation, and orchestrates
    the download process based on user preferences.
    """
    # Check that all required dependencies are available
    check_dependencies()
    
    # Parse and handle command line arguments
    parser = argparse.ArgumentParser(
        description='Download YouTube videos or audio',
        epilog='Examples:\n'
               '  python youtube_downloader.py                  # Download video\n'
               '  python youtube_downloader.py --audio-only     # Download audio only',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--audio-only', '-a', action='store_true', 
                       help='Download only audio (MP3 format)')
    args = parser.parse_args()

    # Get and validate YouTube URL from user
    url = input("Enter the YouTube video URL: ").strip()
    if not url:
        print("URL cannot be empty.")
        return

    # Handle audio-only download mode
    if args.audio_only:
        _handle_audio_download(url)
    else:
        # Handle standard video download mode
        _handle_video_download(url)


def _handle_audio_download(url):
    """
    Handle the audio-only download workflow.
    
    Args:
        url (str): YouTube video URL
    """
    print()  # Add visual spacing
    loading = LoadingAnimation("Fetching audio options")
    loading.start()
    
    # Get available audio formats
    audio_formats = list_audio_formats(url, loading)
    if not audio_formats:
        return

    # Get user's format selection
    selected_format = _get_user_format_choice(audio_formats, "audio")
    if selected_format:
        download_selected_audio(url, selected_format)


def _handle_video_download(url):
    """
    Handle the video download workflow.
    
    Args:
        url (str): YouTube video URL
    """
    print()  # Add visual spacing
    loading = LoadingAnimation("Fetching options")
    loading.start()
    
    # Get available video formats
    formats = list_formats(url, loading)
    if not formats:
        return

    # Get user's format selection
    selected_format = _get_user_format_choice(formats, "format")
    if selected_format:
        download_selected_format(url, selected_format)


def _get_user_format_choice(formats, format_type):
    """
    Get user's selection from available formats with input validation.
    
    Args:
        formats (list): List of available formats
        format_type (str): Type description for user prompts ("format" or "audio")
        
    Returns:
        str: Selected format ID, or None if user cancels
    """
    while True:
        try:
            choice = int(input(f"\nSelect the {format_type} by number: "))
            if 1 <= choice <= len(formats):
                return formats[choice - 1]['format_id']
            else:
                print(f"Invalid number. Please choose between 1 and {len(formats)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return None


# Entry Point
if __name__ == "__main__":
    """
    Entry point when script is run directly.
    This ensures main() only runs when the script is executed directly,
    not when imported as a module.
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        sys.exit(1)
