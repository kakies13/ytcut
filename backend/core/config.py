import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "YTcut"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DOWNLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "downloads")

settings = Settings()

# Ensure download directory exists
os.makedirs(settings.DOWNLOAD_DIR, exist_ok=True)
