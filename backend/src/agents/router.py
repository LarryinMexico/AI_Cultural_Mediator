import json
import logging
from src.agents.lora import lora_manager

logger = logging.getLogger(__name__)

ROUTER_PROMPT = """
Analyze the following text for idioms, cultural references, or slang that might be confusing to a non-native speaker.
If found, extract the phrase and provide a brief explanation.

Text: "{text}"

Response Format (JSON):
{{
    "detected": true/false,
    "phrase": "extracted phrase",
    "type": "idiom" | "slang" | "cultural",
    "reasoning": "step-by-step reasoning"
}}
"""

# Common English idioms to detect
IDIOM_PHRASES = [
    "break a leg", "knock them dead", "knock 'em dead",
    "raining cats and dogs", "it's raining cats and dogs",
    "under the weather", "feeling under the weather",
    "on the fence", "on cloud nine", "feeling blue",
    "let the cat out of the bag", "spill the beans",
    "piece of cake", "when life gives you lemons",
    "burning the midnight oil", "hit the nail on the head",
    "bite the bullet", "cost an arm and a leg",
    "the early bird catches the worm", "better late than never",
    "back to square one", "beat around the bush",
    "once in a blue moon", "the ball is in your court",
    "barking up the wrong tree", "cutting corners",
    "cold feet", "chip on", "last straw", "cry over spilled milk",
    # Modern internet slang
    "rage bait", "no cap", "bussin", "salty", "vibe check",
    "gaslighting", "lowkey", "capping", "mid", "touch grass",
]

class RouterAgent:
    async def analyze(self, text: str) -> dict | None:
        """
        Analyze text for cultural nuances.
        """
        text_lower = text.lower()
        
        # Check for known idioms
        for idiom in IDIOM_PHRASES:
            if idiom in text_lower:
                return {
                    "detected": True,
                    "phrase": idiom,
                    "type": "idiom",
                    "reasoning": f"The phrase '{idiom}' is a common English idiom with cultural meaning."
                }
        
        # If no idiom detected
        return None

router_agent = RouterAgent()
