# WebSocket API Contract

**Protocol**: Socket.IO v4
**Namespace**: `/`

## Client -> Server

### `audio_chunk`
- **Type**: Binary
- **Format**: 16kHz PCM mono, Float32
- **Description**: Stream of raw audio data from client microphone (via AudioWorklet).

### `config`
- **Type**: JSON
- **Description**: Session configuration sent on connection.
```json
{
  "target_lang": "es",
  "source_lang": "en" (optional, auto-detect if null)
}
```

## Server -> Client

### `transcript_partial`
- **Type**: JSON
- **Description**: Real-time updates of the transcription.
```json
{
  "id": "uuid-v4",
  "text": "Hello world",
  "is_final": false,
  "timestamp": 1678900000.123,
  "confidence": 0.95
}
```

### `translation_final`
- **Type**: JSON
- **Description**: Completed translation for a finalized segment.
```json
{
  "chunk_id": "uuid-v4-of-source",
  "target_lang": "es",
  "translated_text": "Hola mundo",
  "latency_ms": 120.5
}
```

### `cultural_insight`
- **Type**: JSON
- **Description**: Asynchronous insight pushed when detection occurs.
```json
{
  "id": "uuid-v4",
  "source_text": "break a leg",
  "explanation": "A theatrical idiom wishing good luck.",
  "context_type": "idiom",
  "sources": ["https://example.com/etymology"],
  "relevance_score": 0.98
}
```

### `error`
- **Type**: JSON
```json
{
  "code": "MODEL_LOAD_ERROR",
  "message": "Failed to load Qwen model"
}
```
