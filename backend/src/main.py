import socketio
import warnings
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings, logger
from pydantic import BaseModel
import os
import tempfile
from contextlib import asynccontextmanager

# Suppress resource tracker warnings (they're harmless)
warnings.filterwarnings('ignore', category=UserWarning, module='multiprocessing.resource_tracker')

# Create FastAPI app
app = FastAPI(title=settings.app_name)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=settings.allowed_origins
)

# Mount Socket.IO app
socket_app = socketio.ASGIApp(sio, app)

# Register event handlers
from src.api import events

# Register Socket.IO events
events.register_socket_events(sio)

# Add text input endpoint for testing
from fastapi import HTTPException
from pydantic import BaseModel

class TextInput(BaseModel):
    text: str

@app.post("/api/test-text")
async def test_text(input: TextInput):
    """Test endpoint for sending text directly to translation"""
    try:
        logger.info(f"Received test text: {input.text}")
        # Note: sio_server is not defined here, assuming it should be 'sio'
        logger.info(f"Connected clients: {[None if sid is None else sid for sid in sio.manager.get_participants('/', '/')]}")
        
        # Import necessary modules
        from src.services.translator import translation_service
        from src.services.insight import insight_generator
        
        # STEP 1: Check for cultural content and search if needed
        logger.info("Checking cultural insights...")
        insight = await insight_generator.process(input.text)
        
        # STEP 2: Translate with or without cultural context
        if insight and insight.search_context:
            logger.info("Translating with search context...")
            translation = await translation_service.translate(
                input.text,
                target_lang="zh-TW",
                cultural_context=insight.search_context
            )
        else:
            logger.info("Translating without cultural context...")
            translation = await translation_service.translate(
                input.text,
                target_lang="zh-TW"
            )
        
        logger.info(f"Translation: {translation}")
        
        # Build response
        response = {
            "source_text": input.text,
            "target_lang": "zh-TW",
            "translated_text": translation
        }
        
        # Add cultural insight if detected
        if insight:
            logger.info("Cultural insight detected")
            response["cultural_insight"] = {
                "phrase": insight.source_text,
                "explanation": insight.explanation,
                "type": insight.context_type,
                "sources": insight.sources
            }
        else:
            logger.info("No cultural insight")
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing test text: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Upload audio file and transcribe with local OpenAI Whisper"""
    try:
        logger.info(f"Received audio file: {file.filename}, type: {file.content_type}, size: {file.size if hasattr(file, 'size') else 'unknown'}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
            logger.info(f"Saved to temp file: {tmp_path}")
        
        try:
            # Transcribe with local Whisper
            from src.services.whisper_local import whisper_local_service
            from src.api.events import process_transcript
            
            logger.info("Starting Whisper transcription...")
            transcript = whisper_local_service.transcribe(tmp_path, language="en")
            logger.info(f"Whisper transcript: {transcript}")
            
            # Find connected clients
            connected_clients = list(sio.manager.rooms.get("/", {}).keys())
            logger.info(f"Connected clients: {connected_clients}")
            
            # Process transcript (translate + insights)
            for sid in connected_clients:
                if sid:  # Skip None
                    await process_transcript(sid, transcript, is_final=True)
            
            return {
                "status": "ok",
                "transcript": transcript
            }
            
        finally:
            # Cleanup temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                logger.info(f"Cleaned up temp file")
        
    except Exception as e:
        logger.error(f"Transcription error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    from src.agents.lora import lora_manager
    return {
        "status": "ok",
        "model_loaded": lora_manager.is_model_ready(),
        "model_loading": lora_manager.is_loading,
        "model_path": lora_manager.model_path,
        "model_error": lora_manager.load_error
    }

# Socket.IO events are registered in events.py via register_socket_events()
# Don't duplicate them here!

if __name__ == "__main__":
    import multiprocessing
    import signal
    import sys
    import atexit
    
    multiprocessing.freeze_support()
    
    def cleanup_resources():
        """Clean up resources on exit"""
        logger.info("Cleaning up resources...")
        try:
            # Clean up ASR engine if it exists
            from src.api.events import asr_engine
            if asr_engine:
                asr_engine.reset()
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")
    
    def signal_handler(sig, frame):
        """Handle shutdown signals gracefully"""
        logger.info("Received shutdown signal, cleaning up...")
        cleanup_resources()
        sys.exit(0)
    
    # Register cleanup handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(cleanup_resources)
    
    import uvicorn
    uvicorn.run("src.main:socket_app", host="0.0.0.0", port=8000, reload=True)
