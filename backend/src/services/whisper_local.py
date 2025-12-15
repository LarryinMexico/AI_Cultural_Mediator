import whisper
import logging

logger = logging.getLogger(__name__)

class WhisperLocalService:
    """Local OpenAI Whisper for speech-to-text (no API key needed)"""
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize Whisper model
        Args:
            model_name: tiny, base, small, medium, large
                       base (74MB) recommended for balance
        """
        logger.info(f"Loading Whisper model: {model_name}")
        self.model = whisper.load_model(model_name)
        logger.info(f"Whisper {model_name} model loaded successfully")
    
    def transcribe(self, audio_file_path: str, language: str = "en") -> str:
        """
        Transcribe audio file using Whisper
        Args:
            audio_file_path: Path to audio file (supports webm, mp3, wav, etc.)
            language: Language code (default: "en")
        Returns:
            Transcribed text
        """
        try:
            logger.info(f"Transcribing audio file: {audio_file_path}")
            
            result = self.model.transcribe(
                audio_file_path,
                language=language,
                fp16=False  # Use FP32 for CPU compatibility
            )
            
            transcript = result['text'].strip()
            logger.info(f"Whisper transcript: {transcript}")
            
            return transcript
            
        except Exception as e:
            logger.error(f"Whisper transcription error: {e}", exc_info=True)
            raise

# Initialize with base model (good balance of speed and accuracy)
whisper_local_service = WhisperLocalService(model_name="base")
