from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from core.config import settings

app = FastAPI(title="YTcut API", version="1.0.0")

# FFmpeg is handled by the environment (imageio-ffmpeg or system install)
# ------------------------------------------------


from fastapi.staticfiles import StaticFiles

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False, # Disable credentials to allow wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (generated clips)
app.mount("/downloads", StaticFiles(directory=settings.DOWNLOAD_DIR), name="downloads")

from pydantic import BaseModel
from services.downloader import DownloadService
from core.transcriber import TranscriberService
from core.analyzer import ContentAnalyzer
from core.cropper import VideoCropper

# Initialize Services
downloader = DownloadService()
transcriber = TranscriberService(model_size="tiny") # Use 'tiny' for Render Free Tier (Low RAM)
analyzer = ContentAnalyzer()
cropper = VideoCropper()

class VideoRequest(BaseModel):
    url: str

@app.post("/api/process")
def process_video(request: VideoRequest):
    try:
        # 1. Download
        print(f"Downloading: {request.url}")
        video_data = downloader.download_video(request.url)
        video_path = video_data["path"]
        # 2. Transcribe
        print("Transcribing...")
        transcription_result = transcriber.transcribe_video(video_path)
        transcript_text = transcriber.format_for_llm(transcription_result)
        
        # 3. Analyze (Get interesting clips)
        print("Analyzing with Gemini...")
        clips_metadata = analyzer.analyze_transcript(transcript_text)
        
        if not clips_metadata:
            return {"status": "error", "message": "No interesting clips found by AI.", "raw_transcript": transcript_text[:500]}

        # 4. Process Clips (Crop & Cut)
        print(f"Processing {len(clips_metadata)} clips...")
        processed_clips = []
        for clip in clips_metadata:
            start = clip.get("start_time")
            end = clip.get("end_time")
            
            # Simple validation
            if start is None or end is None: 
                continue
                
            output_filename = f"{video_data['id']}_{start}_{end}.mp4"
            output_path = os.path.join(settings.DOWNLOAD_DIR, output_filename)
            
            try:
                cropper.create_vertical_clip(video_path, start, end, output_path)
                processed_clips.append({
                    "title": clip.get("title", "Untitled Clip"),
                    "reason": clip.get("reason", ""),
                    "file_path": output_filename, # Return relative path or filename
                    "duration": end - start
                })
            except Exception as e:
                print(f"Error processing clip {start}-{end}: {e}")

        # Cleanup original video if needed (optional)
        # os.remove(video_path) 

        return {
            "status": "success",
            "original_video": video_data,
            "clips": processed_clips
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "YTcut Backend is Running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
