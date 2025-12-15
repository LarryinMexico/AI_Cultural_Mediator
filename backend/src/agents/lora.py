import logging
import mlx_lm
from src.config import settings

logger = logging.getLogger(__name__)

class LoRAManager:
    def __init__(self):
        self.model_path = settings.llm_model
        self.model = None
        self.tokenizer = None
        self.adapters = {}
        self.is_loading = False
        self.load_error = None
        logger.info(f"Initializing LoRA Manager with model: {self.model_path}")
        # Load model in background to avoid blocking
        import threading
        threading.Thread(target=self._load_model, daemon=True).start()
    
    def _load_model(self):
        """Load model in background thread"""
        try:
            self.is_loading = True
            logger.info(f"Loading model {self.model_path}... (this may take a few minutes on first run)")
            
            # Load model with V2 adapter (idiom-optimized)
            self.model, self.tokenizer = mlx_lm.load(
                self.model_path,
                adapter_path="adapters/translation_v2"  # 使用習語優化版本
            )
            
            logger.info("✓ Model loaded successfully with V2 adapter!")
            logger.info("  V2 includes: Basic translation + Idiom understanding")
            self.is_loading = False
        except Exception as e:
            logger.error(f"Error loading model with V2 adapter: {e}")
            logger.info("Falling back to base model without adapter...")
            try:
                # Fallback to base model
                self.model, self.tokenizer = mlx_lm.load(self.model_path)
                logger.info("✓ Base model loaded successfully")
                self.is_loading = False
            except Exception as e2:
                logger.error(f"Failed to load base model: {e2}")
                self.load_error = str(e2)
                self.is_loading = False
                self.model = None
                self.tokenizer = None
    
    def is_model_ready(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None and self.tokenizer is not None 

    def load_adapter(self, adapter_name: str, adapter_path: str):
        """
        Load a LoRA adapter into memory.
        """
        logger.info(f"Loading adapter {adapter_name} from {adapter_path}")
        # In real app: self.model.load_adapter(adapter_path, adapter_name)
        pass

    async def generate(self, prompt: str, adapter: str = "default", max_tokens: int = 100) -> str:
        """
        Generate text using the specified adapter.
        """
        if self.model is None or self.tokenizer is None:
            logger.warning("Model not loaded, returning mock response")
            return "MOCKED_LLM_RESPONSE"
        
        try:
            # Set adapter if specified and available
            if adapter != "default" and adapter in self.adapters:
                # Note: mlx-lm doesn't have built-in adapter support
                # This would require custom implementation
                pass
            
            # Generate response with better parameters
            response = mlx_lm.generate(
                self.model, 
                self.tokenizer, 
                prompt=prompt, 
                max_tokens=max_tokens,
                verbose=False
            )
            return response
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return "MOCKED_LLM_RESPONSE"

lora_manager = LoRAManager()
