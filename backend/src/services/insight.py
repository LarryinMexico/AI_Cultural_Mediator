import logging
from uuid import uuid4
from src.services.exa import exa_client
from src.models.culture import CulturalInsight
from src.agents.lora import lora_manager

logger = logging.getLogger(__name__)

class InsightGenerator:
    """Generate cultural insights using Exa search and LLM explanation"""
    
    async def _should_search(self, text: str) -> bool:
        """
        Use LLM to determine if text contains cultural content requiring web search
        """
        try:
            prompt = f"""Analyze if the following English text contains modern slang, idioms, cultural references, or internet terminology that would benefit from web search for cultural context.

Text: "{text}"

Consider:
1. Modern slang or internet language (e.g., "salty", "based", "sus", "ratio", "rage bait", "touch grass")
2. Cultural idioms or expressions (e.g., "break a leg", "spill the tea", "no cap")
3. Pop culture references or memes
4. Regional expressions or colloquialisms  
5. Newly emerged terminology from social media
6. Click-bait or provocative internet terminology (e.g., "rage bait", "trolling")

Examples that need search:
- "They're being salty" → YES (internet slang)
- "This is total rage bait" → YES (internet terminology)
- "Break a leg" → YES (cultural idiom)
- "I want a burger" → NO (standard language)

Answer ONLY with "YES" if web search would help provide cultural context, or "NO" if it's standard language.

Answer:"""
            
            response = await lora_manager.generate(prompt, adapter="default", max_tokens=5)
            decision = response.strip().upper()
            
            should_search = "YES" in decision
            logger.info(f"LLM detection for '{text}': {decision} -> search={should_search}")
            
            return should_search
            
        except Exception as e:
            logger.error(f"Error in LLM detection: {e}")
            return False  # Default to no search on error
    
    async def process(self, text: str) -> CulturalInsight | None:
        """
        Process text and generate cultural insights with LLM explanation
        """
        try:
            # Use LLM to decide if search is needed
            if not await self._should_search(text):
                logger.info(f"No cultural content detected in: '{text}'")
                return None
            
            logger.info(f"Cultural content detected, searching for '{text}'")
            search_query = f"{text} meaning slang idiom cultural explanation"
            logger.info(f"Searching Exa with query: {search_query}")
            
            # Use search_context which is the actual method in exa.py
            results = await exa_client.search_context(search_query)
            
            if not results or len(results) == 0:
                logger.warning(f"No Exa results found for: {text}")
                return None
            
            logger.info(f"Found {len(results)} Exa results")
            
            # results is already a list of dicts with url, title, snippet
            sources = results
            
            # Generate LLM explanation from search results
            # Use search results to generate Traditional Chinese explanation
            explanation = await self._generate_explanation(text, results)
            
            # Extract search context for translation (keep original English)
            search_context = "\n\n".join([
                f"Source: {r.get('title', 'Unknown')}\nContext: {r.get('snippet', r.get('text', ''))}"
                for r in results[:2]  # Use top 2 results
            ])
            
            return CulturalInsight(
                id=str(uuid4()),
                source_text=text,
                explanation=explanation,
                context_type="slang",
                sources=[
                    {
                        "url": r.get("url", ""),
                        "title": r.get("title", ""),
                        "snippet": r.get("snippet", r.get("text", ""))[:200]
                    }
                    for r in results[:3]
                ],
                search_context=search_context,  # Add raw search results
                relevance_score=0.9  # High relevance since LLM detected it
            )
            
        except Exception as e:
            logger.error(f"Error generating insight: {e}", exc_info=True)
            return None
    
    async def _generate_explanation(self, text: str, search_results: list) -> str:
        """
        Use LLM to generate a clear Traditional Chinese explanation from search results
        """
        try:
            # Build context from search results
            context = "\n\n".join([
                f"Source {i+1}: {r.get('title', 'Unknown')}\n{r.get('snippet', r.get('text', 'No content'))[:500]}"
                for i, r in enumerate(search_results[:3])
            ])
            
            # LLM prompt for explanation
            prompt = f"""根據以下網路搜尋結果，用 2-3 句繁體中文清楚解釋 "{text}" 的文化含義、起源和使用情境。

搜尋結果：
{context}

請用繁體中文解釋（2-3 句話）："""
            
            logger.debug(f"Explanation prompt: {prompt}")
            
            # Generate explanation using base model
            explanation = await lora_manager.generate(
                prompt, 
                adapter="default",
                max_tokens=150
            )
            
            explanation = explanation.strip()
            logger.info(f"LLM explanation generated: {explanation[:100]}...")
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating LLM explanation: {e}")
            # Fallback to simple concatenation
            fallback = " ".join([r.get('snippet', '')[:100] for r in search_results[:2]])
            return f"{text} 的文化背景：{fallback}"

insight_generator = InsightGenerator()
