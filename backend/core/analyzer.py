import google.generativeai as genai
from core.config import settings
import json
import typing

class ContentAnalyzer:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_transcript(self, transcript_text: str) -> list[dict]:
        """
        Analyzes the transcript and returns a list of interesting clips.
        """
        prompt = f"""
        You are a top-tier viral content editor for TikTok and YouTube Shorts.
        Analyze the following video transcript and identify the top 3 most engaging, funny, or interesting segments that will go viral.
        
        CRITICAL RULES:
        1. Each segment MUST be between 25 and 35 seconds long. Ideally exactly 30 seconds.
        2. The content must be self-contained (has a clear start and punchline/end).
        3. Do NOT select the intro/outro unless it's extremely funny.
        
        Transcript:
        {transcript_text}

        Return the Output STRICTLY as a JSON array of objects with the following keys, and NO other text:
        [
            {{
                "title": "Catchy Title for the Clip",
                "reason": "Why this is viral material",
                "start_time": <start_seconds_int>,
                "end_time": <end_seconds_int>
            }}
        ]
        """

        try:
            print(f"Sending transcript to Gemini (Length: {len(transcript_text)} chars)...")
            response = self.model.generate_content(prompt)
            # print("Gemini Raw Response:", response.text) # DEBUG PRINT
            
            # Cleanup markdown formatting if present
            text = response.text.replace('```json', '').replace('```', '').strip()
            data = json.loads(text)
            
            if not data:
                raise ValueError("AI returned empty list")
                
            return data
            
        except Exception as e:
            print(f"Error in Gemini Analysis: {e}")
            import traceback
            traceback.print_exc()
            
            # FALLBACK: If AI fails, return the first 30 seconds of the video (better than 60)
            print("FALLBACK: Generating default clip due to AI error.")
            return [
                {
                    "title": "Highlight (AI Fallback)",
                    "reason": "AI analysis failed, showing video start.",
                    "start_time": 0,
                    "end_time": 30
                }
            ]
