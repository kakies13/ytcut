import yt_dlp
import os
import uuid
from core.config import settings

class DownloadService:
    def __init__(self):
        self.download_dir = settings.DOWNLOAD_DIR

    def download_video(self, url: str) -> dict:
        """
        Downloads a YouTube video and returns the file path and metadata.
        """
        video_id = str(uuid.uuid4())
        output_template = os.path.join(self.download_dir, f"{video_id}.%(ext)s")

        # Anti-bot measures
        cookies_content = os.environ.get("YOUTUBE_COOKIES")
        cookie_file = "cookies.txt"
        if cookies_content:
             # Create cookies.txt from env var if it doesn't exist or is empty
            with open(cookie_file, "w") as f:
                f.write(cookies_content)
        
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            # Spoof User-Agent to look like a real browser
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'http_headers': {
                'Referer': 'https://www.google.com/',
                'Accept-Language': 'en-US,en;q=0.9',
            },
            # Use cookies if available
            'cookiefile': cookie_file if os.path.exists(cookie_file) else None,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # define the final filename manually because merge_output_format is mp4
            # yt-dlp might return .mkv or .webm if not merged yet, but with merge_output_format it should be mp4
            final_filename = os.path.splitext(filename)[0] + ".mp4"
            
            return {
                "id": video_id,
                "title": info.get('title', 'Unknown Title'),
                "duration": info.get('duration', 0),
                "path": final_filename,
                "thumbnail": info.get('thumbnail', '')
            }
