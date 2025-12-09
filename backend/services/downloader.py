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

        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
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
