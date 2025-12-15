# Research & Technology Decisions: Core Experience

**Status**: Complete
**Date**: 2025-12-12

## Decisions

### 1. Audio Processing & VAD
- **Decision**: Client-side VAD using `onnxruntime-web` (Silero VAD) + AudioWorklet.
- **Rationale**: Reduces bandwidth by only sending speech; AudioWorklet ensures non-blocking audio capture on the main thread.
- **Alternatives**: Server-side VAD (increased latency/bandwidth), Browser native VAD (inconsistent support).

### 2. ASR Engine
- **Decision**: `mlx-whisper` with `distil-whisper-large-v3`.
- **Rationale**: Optimized for Apple Silicon; distil model provides best speed/accuracy trade-off for real-time (<500ms).
- **Alternatives**: Vanilla Whisper (too slow), Faster-Whisper (no MLX support).

### 3. LLM & Cultural Insights
- **Decision**: `mlx-lm` with `Qwen2.5-3B-Instruct-4bit`.
- **Rationale**: Fits in memory constraints (<6GB total system load) while maintaining decent reasoning capability for cultural extraction.
- **Alternatives**: Llama-3-8B (too large for 8GB RAM constraints with ASR running).

### 4. Communication Protocol
- **Decision**: WebSocket via `socket.io`.
- **Rationale**: Full-duplex communication required for streaming audio up and partial transcripts down.
- **Alternatives**: HTTP/2 Server-Sent Events (unidirectional, harder to handle upstream audio stream).

### 5. Search Provider
- **Decision**: Exa AI SDK.
- **Rationale**: Constitutionally mandated; optimized for neural search.

## Open Items
- None.
