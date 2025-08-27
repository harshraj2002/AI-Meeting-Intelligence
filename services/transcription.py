import whisper
import os
from pathlib import Path
import subprocess
import tempfile

class TranscriptionService:
    def __init__(self):
        # Use OpenAI's whisper instead of faster-whisper
        try:
            self.model = whisper.load_model("base")
            print("Whisper model loaded successfully")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            self.model = None
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio file using OpenAI Whisper"""
        if not self.model:
            raise Exception("Whisper model not loaded")
        
        try:
            result = self.model.transcribe(audio_file_path)
            transcript = result["text"].strip()
            return transcript
                
        except Exception as e:
            raise Exception(f"Transcription error: {str(e)}")
    
    def extract_audio_from_video(self, video_path: str, audio_path: str):
        """Extract audio from video file using ffmpeg"""
        try:
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vn", "-acodec", "pcm_s16le",
                "-ar", "16000", "-ac", "1",
                audio_path, "-y"
            ]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            # If ffmpeg is not available, copy the file and hope it works
            import shutil
            shutil.copy2(video_path, audio_path)
        except FileNotFoundError:
            # ffmpeg not found, copy the original file
            import shutil
            shutil.copy2(video_path, audio_path)