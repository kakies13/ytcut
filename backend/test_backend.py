
import sys
try:
    print("Testing imports...")
    import fastapi
    import uvicorn
    from moviepy.editor import VideoFileClip
    import yt_dlp
    import cv2 
    import main
    print("SUCCESS: All imports working!")
except Exception as e:
    print(f"ERROR: {e}")
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
