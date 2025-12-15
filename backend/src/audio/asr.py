import numpy as np
import logging
from RealtimeSTT import AudioToTextRecorder
from src.config import settings

logger = logging.getLogger(__name__)

class ASREngine:
    def __init__(self, on_text_callback=None):
        self.model_path = "tiny" # Use tiny for speed on CPU/M1 default
        logger.info(f"Initializing RealtimeSTT with model: {self.model_path}")
        
        self.recorder = AudioToTextRecorder(
            model=self.model_path,
            language="en", # Force English for now as source
            use_microphone=False,
            spinner=False,
            enable_realtime_transcription=True,
            on_realtime_transcription_update=self._on_partial,
            debug_mode=False
        )
        
        self.on_text_callback = on_text_callback
        
        # Start the text processing loop in a non-blocking way if possible, 
        # but RealtimeSTT.text() is blocking.
        # However, for feed_audio usage, we typically don't call .text() in a loop explicitly 
        # if we want async behavior.
        # Actually, RealtimeSTT's architecture is a bit complex. 
        # If we use .text(callback), it starts a loop.
        # We need to start this loop in a background thread so it doesn't block FastAPI.
        
        import threading
        self.processing_thread = threading.Thread(target=self._start_processing, daemon=True)
        self.processing_thread.start()

    def _start_processing(self):
        logger.info("Starting STT processing loop...")
        try:
            # This will call self._on_final whenever a sentence is completed
            self.recorder.text(self._on_final)
        except EOFError:
            # Connection closed, this is normal when recorder is shut down
            logger.info("STT processing loop ended (connection closed)")
        except Exception as e:
            logger.error(f"Error in STT processing loop: {e}")

    def set_callback(self, callback):
        self.on_text_callback = callback

    def _on_partial(self, text):
        if self.on_text_callback:
            self.on_text_callback(text, is_final=False)

    def _on_final(self, text):
        if self.on_text_callback:
            self.on_text_callback(text, is_final=True)

    async def process_audio(self, audio_chunk: bytes):
        """
        Process incoming audio chunk (float32 bytes) -> int16 -> feed to recorder.
        """
        try:
            # Convert bytes (float32) to numpy array
            audio_float32 = np.frombuffer(audio_chunk, dtype=np.float32)
            
            # Convert to int16 (PCM) for RealtimeSTT
            # Scale -1.0..1.0 to -32768..32767
            audio_int16 = (audio_float32 * 32767).astype(np.int16)
            
            # Feed raw bytes of int16
            self.recorder.feed_audio(audio_int16.tobytes())
            
            # We don't return text here anymore; callbacks handle it
            return None

        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return None
            
    def reset(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'recorder') and self.recorder:
                self.recorder.shutdown()
            if hasattr(self, 'processing_thread') and self.processing_thread.is_alive():
                # Thread is daemon, will be cleaned up automatically
                pass
            logger.info("ASR Engine reset complete")
        except Exception as e:
            logger.error(f"Error resetting ASR engine: {e}")