import logging
import asyncio
import uuid
from datetime import datetime
from src.audio.streaming_asr import asr_engine
from src.services.translator import translation_service
from src.services.insight import insight_generator
from src.models.core import TranscriptChunk, Translation

logger = logging.getLogger(__name__)


async def process_transcript(sid, text: str, is_final: bool):
    """
    Process transcription and generate translation/insights
    """
    try:
        logger.info(f"Processing transcript for {sid}: '{text}' (final={is_final})")

        # Generate transcript ID
        transcript_id = str(uuid.uuid4())

        # Import sio from main
        from src.main import sio

        # Emit partial transcript
        logger.info(f"Emitting transcript_partial to {sid}")
        await sio.emit(
            "transcript_partial",
            {
                "id": transcript_id,
                "text": text,
                "is_final": is_final,
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.9,
            },
            room=sid,
        )
        logger.info(f"transcript_partial emitted successfully")

        # Only process final transcripts for translation
        if is_final and text.strip():
            # 1. FIRST: Generate cultural insights (with LLM explanation)
            logger.info("Generating cultural insights...")
            insight = await insight_generator.process(text)
            
            # 2. SECOND: Translate with cultural context
            start_time = datetime.now()
            logger.info(f"Starting translation: {text}")
            
            if insight and insight.search_context:
                # Use raw search results for better translation
                logger.info(f"Translating with search context")
                translation = await translation_service.translate(
                    text, 
                    target_lang="zh-TW",
                    cultural_context=insight.search_context  # Use raw search results
                )
            else:
                translation = await translation_service.translate(text, target_lang="zh-TW")
            
            latency = (datetime.now() - start_time).total_seconds() * 1000
            logger.info(f"Translation result: {translation}")

            # Emit translation
            logger.info(f"Emitting translation_final to {sid}")
            await sio.emit(
                "translation_final",
                {
                    "chunk_id": transcript_id,
                    "target_lang": "zh-TW",
                    "translated_text": translation,
                    "latency_ms": int(latency),
                },
                room=sid,
            )
            logger.info(f"translation_final emitted")

            # 3. THIRD: Emit cultural insight if generated
            if insight:
                logger.info(f"Emitting cultural_insight to {sid}")
                await sio.emit(
                    "cultural_insight",
                    {
                        "phrase": insight.source_text,
                        "explanation": insight.explanation,
                        "type": insight.context_type,
                        "sources": insight.sources,
                    },
                    room=sid,
                )
                logger.info(f"cultural_insight emitted")
            else:
                logger.info("No cultural insights to emit")

    except Exception as e:
        logger.error(f"Error in process_transcript: {e}", exc_info=True)


def register_socket_events(sio):
    """Register Socket.IO event handlers"""

    @sio.event
    async def connect(sid, environ):
        logger.info(f"Client connected: {sid}")
        
        # Clear audio buffer from previous session
        asr_engine.clear_buffer()
        logger.info("Audio buffer cleared for new session")
        
        # Define callback function for ASR transcription
        def transcription_callback(text, is_final):
            """Called when ASR produces transcription"""
            logger.info(f"ASR Callback: '{text}' (final={is_final}) for client {sid}")
            
            # Schedule processing in event loop
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                # Create task to process and emit transcript
                loop.create_task(process_transcript(sid, text, is_final))
                logger.info(f"Scheduled transcript processing for {sid}")
            except Exception as e:
                logger.error(f"Error scheduling transcript: {e}", exc_info=True)
        
        # Set callback for this client
        asr_engine.set_callback(transcription_callback)
        logger.info(f"ASR callback configured for {sid}")

    @sio.event
    async def disconnect(sid):
        logger.info(f"Client disconnected: {sid}")
        # Stop audio processing
        asr_engine.reset()

    @sio.event
    async def audio_chunk(sid, data):
        """
        Handle incoming audio chunk from client
        Args:
            sid: socket ID
            data: audio data (ArrayBuffer from frontend, bytes of float32)
        """
        try:
            if not data:
                return
            
            # Log first chunk only
            if not hasattr(audio_chunk, 'first_logged'):
                logger.info(f"Receiving audio chunks from {sid}, size: {len(data)} bytes")
                audio_chunk.first_logged = True
            
            # Process audio through streaming ASR
            await asr_engine.process_audio(data)
            
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}", exc_info=True)