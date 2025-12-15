# Data Model: Core Experience

## Core Entities

### TranscriptChunk
Represents a segment of transcribed text.
```python
class TranscriptChunk(BaseModel):
    id: UUID
    text: str
    is_final: bool
    timestamp: float
    confidence: float
```

### Translation
Represents the translated text for a corresponding transcript chunk.
```python
class Translation(BaseModel):
    chunk_id: UUID
    target_lang: str
    translated_text: str
    latency_ms: float
```

### CulturalInsight
Represents an extracted cultural note.
```python
class CulturalInsight(BaseModel):
    id: UUID
    source_text: str  # The idiom/phrase detected
    explanation: str
    context_type: Literal["idiom", "historical", "slang", "etiquette"]
    sources: List[str]  # URLs from Exa
    relevance_score: float
```

## Frontend State (Zustand)

```typescript
interface AppState {
    status: 'idle' | 'listening' | 'processing' | 'error';
    transcript: TranscriptChunk[];
    translations: Map<UUID, Translation>;
    insights: CulturalInsight[];
    addTranscriptChunk: (chunk: TranscriptChunk) => void;
    updateTranslation: (translation: Translation) => void;
    addInsight: (insight: CulturalInsight) => void;
}
```

## Backend Events (Socket.IO)

- `client -> server`: `audio_chunk` (binary)
- `server -> client`: `transcript_partial` (JSON: TranscriptChunk)
- `server -> client`: `translation_final` (JSON: Translation)
- `server -> client`: `cultural_insight` (JSON: CulturalInsight)
