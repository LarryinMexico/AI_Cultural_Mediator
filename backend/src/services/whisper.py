import logging
import openai
from src.config import settings

logger = logging.getLogger(__name__)

class WhisperService:
    """OpenAI Whisper API service for speech-to-text"""
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        if not self.api_key:
            logger.warning("OpenAI API key not configured")
        else:
            openai.api_key = self.api_key
            logger.info("OpenAI Whisper service initialized")
    
    async def transcribe(self, audio_file, language: str = "en") -> str:
        """
        Transcribe audio file using OpenAI Whisper API
        
        Args:
            audio_file: File-like object containing audio data
            language: Language code (default: "en")
            
        Returns:
            Transcribed text
        """
        try:
            logger.info(f"Transcribing audio with Whisper API (language: {language})")
            
            # Call OpenAI Whisper API
            response = await openai.Audio.atranscribe(
                model="whisper-1",
                file=audio_file,
                language=language
            )
            
            transcript = response.get('text', '').strip()
            logger.info(f"Whisper transcript: {transcript}")
            
            return transcript
            
        except Exception as e:
            logger.error(f"Whisper transcription error: {e}")
            raise

whisper_service = WhisperService()
