import logging
from exa_py import Exa
from src.config import settings

logger = logging.getLogger(__name__)

class ExaClient:
    def __init__(self):
        self.api_key = settings.exa_api_key
        self.client = Exa(self.api_key) if self.api_key else None
        
    async def search_context(self, query: str) -> list[dict]:
        """
        Search for cultural context and returns a list of sources.
        """
        if not self.api_key or not self.client:
            logger.warning("Exa API key not set. Returning mock results.")
            return [
                {
                    "url": "https://en.wikipedia.org/wiki/Idiom",
                    "title": "Idiom - Wikipedia",
                    "snippet": "An idiom is a phrase or expression..."
                },
                {
                    "url": "https://dictionary.cambridge.org/",
                    "title": "Cambridge Dictionary",
                    "snippet": "Dictionary and grammar resources..."
                }
            ]

        try:
            result = self.client.search(
                query,
                num_results=3
            )
            return [
                {
                    "url": r.url,
                    "title": r.title if hasattr(r, 'title') else "Source",
                    "snippet": r.text[:200] if hasattr(r, 'text') else ""
                }
                for r in result.results
            ]
            
        except Exception as e:
            logger.error(f"Exa search failed: {e}")
            return []

exa_client = ExaClient()
