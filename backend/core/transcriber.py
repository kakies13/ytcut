from faster_whisper import WhisperModel
import os
import gc

class TranscriberService:
    def __init__(self, model_size="tiny"):
        self.model_size = model_size
        self.model = None
        self.device = "cpu"
        self.compute_type = "int8" # Extremely memory efficient

    def transcribe_video(self, video_path: str):
        """
        Transcribes the audio from a video file using faster-whisper.
        Returns a list of Segment objects.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Lazy load model just before use
        if self.model is None:
            # Preemptive GC to clear memory from download/other tasks
            gc.collect() 
            print(f"Loading Faster-Whisper model '{self.model_size}' on {self.device} ({self.compute_type})...")
            self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)

        try:
            print("Starting transcription (Greedy Search for Low RAM)...")
            # faster-whisper returns a generator
            # beam_size=1 reduces memory usage significantly
            segments, info = self.model.transcribe(video_path, beam_size=1)
            
            # Consume generator to get all segments
            result = list(segments)
            print(f"Transcription complete. Language: {info.language}")
            return result
        finally:
            # Aggressive cleanup
            print("Cleaning up Whisper model to free memory...")
            del self.model
            self.model = None
            gc.collect()

    def format_for_llm(self, transcription_result) -> str:
        """
        Formats the transcription into a readable string with timestamps for the LLM.
        Expects a list of Segment objects from faster-whisper.
        """
        formatted_text = ""
        for segment in transcription_result:
            start = int(segment.start)
            end = int(segment.end)
            text = segment.text.strip()
            formatted_text += f"[{start}s - {end}s]: {text}\n"
        return formatted_text
