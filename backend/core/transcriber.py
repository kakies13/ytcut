import whisper
import os
import torch

class TranscriberService:
    def __init__(self, model_size="base"):
        # Check for CUDA (GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading Whisper model '{model_size}' on {self.device}...")
        self.model = whisper.load_model(model_size, device=self.device)

    def transcribe_video(self, video_path: str) -> str:
        """
        Transcribes the audio from a video file.
        Returns the full text with timestamps handled internally if needed later.
        For LLM analysis, we mostly need the text with coarse timestamps.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        result = self.model.transcribe(video_path)
        
        # We return the segments to allow precise timestamp mapping later
        return result

    def format_for_llm(self, transcription_result) -> str:
        """
        Formats the transcription into a readable string with timestamps for the LLM.
        """
        formatted_text = ""
        for segment in transcription_result['segments']:
            start = int(segment['start'])
            end = int(segment['end'])
            text = segment['text'].strip()
            formatted_text += f"[{start}s - {end}s]: {text}\n"
        return formatted_text
