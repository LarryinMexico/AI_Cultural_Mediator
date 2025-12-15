"""
Simplified streaming ASR engine using faster-whisper
Replaces RealtimeSTT with a simpler, more reliable approach
"""
import logging
import asyncio
import numpy as np
from faster_whisper import WhisperModel
from collections import deque
from threading import Lock

logger = logging.getLogger(__name__)

class StreamingASREngine:
    """Simple streaming ASR using faster-whisper with buffering"""
    
    def __init__(self):
        # Use base whisper model for faster-whisper compatibility
        self.model_path = "large-v3"  # faster-whisper uses simplified names
        self.model = None  # Initialize before loading
        self.on_text_callback = None
        
        # Audio buffering - increased for longer recordings
        self.audio_buffer = deque(maxlen=300)  # Increased from 150 to 300 (longer buffer)
        self.buffer_lock = Lock()
        self.sample_rate = 16000
        
        # Processing state
        self.is_processing = False
        self.last_process_time = 0
        self.process_interval = 1.0  # Reduced from 1.5s to 1.0s for faster response
        
        logger.info(f"Streaming ASR initializing...")
        
        # Eagerly load model on startup (like Qwen)
        try:
            self._load_model()
        except Exception as e:
            logger.error(f"Failed to load Whisper model on startup: {e}")
            self.model = None
    
    def _load_model(self):
        """Load faster-whisper model"""
        if self.model is not None:
            return
            
        try:
            logger.info("Loading Faster Whisper model...")
            # Use CPU with int8 for Apple Silicon efficiency
            self.model = WhisperModel(
                self.model_path,
                device="cpu",
                compute_type="int8"
            )
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def set_callback(self, callback):
        """Set callback for transcription results"""
        self.on_text_callback = callback
        logger.info(f"Callback SET: {callback is not None}")
    
    def clear_buffer(self):
        """Clear audio buffer - call this on new connection"""
        with self.buffer_lock:
            self.audio_buffer.clear()
        logger.info("Audio buffer cleared")
    
    async def process_audio(self, audio_chunk: bytes):
        """
        Process incoming audio chunk
        Args:
            audio_chunk: bytes of float32 audio data
        """
        try:
            # Model already loaded on startup
            if self.model is None:
                logger.warning("Whisper model not loaded, skipping audio")
                return
            
            # Convert bytes to numpy array
            audio_float32 = np.frombuffer(audio_chunk, dtype=np.float32)
            
            # Add to buffer
            with self.buffer_lock:
                self.audio_buffer.append(audio_float32)
            
            # Check if we should process
            import time
            current_time = time.time()
            
            if current_time - self.last_process_time >= self.process_interval:
                self.last_process_time = current_time
                asyncio.create_task(self._process_buffer())
                
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}")
    
    async def _process_buffer(self):
        """Process accumulated audio buffer"""
        if self.is_processing or self.model is None:
            return
            
        self.is_processing = True
        
        try:
            # Get audio from buffer
            with self.buffer_lock:
                if not self.audio_buffer:
                    self.is_processing = False
                    return
                
                # Concatenate all chunks
                audio_data = np.concatenate(list(self.audio_buffer))
            
            # Skip if too short
            duration = len(audio_data) / self.sample_rate
            if duration < 0.5:  # Less than 0.5 seconds
                logger.debug(f"Audio too short ({duration:.2f}s), skipping")
                self.is_processing = False
                return
            
            logger.info(f"Transcribing {duration:.2f}s of audio...")
            
            # Transcribe with minimal VAD filtering for maximum capture
            segments, info = self.model.transcribe(
                audio_data,
                language="en",
                beam_size=5,
                vad_filter=True,
                vad_parameters={
                    "threshold": 0.2,                    # Very low threshold - maximum sensitivity
                    "min_speech_duration_ms": 50,        # Minimum possible duration
                    "max_speech_duration_s": float('inf'),
                    "min_silence_duration_ms": 2000,     # Very long silence tolerance
                    "speech_pad_ms": 600                 # Maximum padding
                }
            )
            
            # Process segments and invoke callback
            segment_count = 0
            for segment in segments:
                text = segment.text.strip()
                segment_count += 1
                logger.info(f"Segment {segment_count}: '{text}'")
                
                # ⭐ CRITICAL: Invoke callback for each segment
                if text and self.on_text_callback:
                    logger.info(f"Calling callback with: '{text}'")
                    try:
                        self.on_text_callback(text, is_final=True)
                        logger.info(f"Callback invoked")
                    except Exception as e:
                        logger.error(f"Callback error: {e}", exc_info=True)
                elif not text:
                    logger.debug(f"Empty segment {segment_count}, skipping")
                elif not self.on_text_callback:
                    logger.warning(f"No callback set! Text lost: '{text}'")
            
            if segment_count == 0:
                logger.info("No segments detected in audio")
            
        except Exception as e:
            logger.error(f"Error processing buffer: {e}", exc_info=True)
        finally:
            self.is_processing = False
    
    def reset(self):
        """Reset the engine but keep callback"""
        with self.buffer_lock:
            self.audio_buffer.clear()
        self.is_processing = False
        # DON'T reset callback - it should persist across sessions
        logger.info(f"ASR Engine reset (callback preserved: {self.on_text_callback is not None})")

# Global instance (model loaded lazily on first use)
asr_engine = StreamingASREngine()
