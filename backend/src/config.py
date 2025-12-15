import os
import logging
from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "Local AI Cultural Mediator"
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:5173"]
    exa_api_key: str | None = os.getenv("EXA_API_KEY")
    
    # Model settings
    # Upgraded to 3B for better translation quality
    asr_model: str = "distil-whisper/distil-large-v3"
    llm_model: str = "Qwen/Qwen2.5-3B-Instruct"  # Upgraded from 0.5B

settings = Settings()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("backend")

if settings.debug:
    logger.setLevel(logging.DEBUG)
