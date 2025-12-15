import logging
import asyncio
from src.config import settings
from src.agents.lora import lora_manager

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.model_path = settings.llm_model
        logger.info(f"Initializing Translation Service with model: {self.model_path}")
        # Use the shared lora_manager instance
    
    async def translate(self, text: str, target_lang: str = "es", cultural_context: str = None) -> str:
        """
        Translate text to target language with optional cultural context.
        Args:
            text: Text to translate
            target_lang: Target language code
            cultural_context: Optional cultural explanation to improve translation
        """
        try:
            logger.info(f"Starting translation: '{text}' -> {target_lang}")
            if cultural_context:
                logger.info(f"Using cultural context for translation")
            
            # Check if model is ready
            if not lora_manager.is_model_ready():
                logger.warning(f"模型未就緒! is_loading={lora_manager.is_loading}, error={lora_manager.load_error}")
                return text  # Return original if model not ready
            
            # Build a clear instruction prompt
            # Use chat format for better instruction following
            lang_map = {
                "zh-TW": "Traditional Chinese (繁體中文)",
                "zh": "Chinese",
                "es": "Spanish",
                "fr": "French",
                "de": "German",
                "ja": "Japanese",
                "ko": "Korean"
            }
            target_language = lang_map.get(target_lang, target_lang)
            
            # Build prompt with cultural context if provided
            if cultural_context:
                # Use search results to inform translation
                prompt = f"""You are a professional translator specializing in English to Traditional Chinese translation with cultural awareness.

Source text: "{text}"

Cultural context from web search:
{cultural_context}

Based on the above context, translate the English text to Traditional Chinese. Consider:
1. The cultural meaning and nuances explained in the context
2. How this phrase is actually used in modern internet/cultural discourse
3. The appropriate Traditional Chinese equivalent that captures both literal and cultural meaning

Provide ONLY the Traditional Chinese translation, nothing else.

Translation:"""
            else:
                # Standard translation without cultural context
                prompt = f"""Translate the following English text to Traditional Chinese.

Source: "{text}"

Provide ONLY the Traditional Chinese translation.

Translation:"""
            
            logger.debug(f"Prompt: {prompt}")
            
            response = await lora_manager.generate(prompt, adapter="default", max_tokens=50)
            logger.info(f"模型響應: {response}")
            
            # Clean up the response
            translation = response.strip()
            
            # Extract the actual translation (sometimes model adds extra text)
            lines = translation.split('\n')
            translation = lines[0].strip()  # Take first line
            
            if translation == "MOCKED_LLM_RESPONSE" or not translation:
                logger.warning("收到 mock response 或空響應，返回原文")
                return text
            
            logger.info(f"翻譯完成: '{text}' → '{translation}'")
            return translation
            
        except Exception as e:
            logger.error(f"翻譯錯誤: {e}")
            return text # Fallback to original

translation_service = TranslationService()
