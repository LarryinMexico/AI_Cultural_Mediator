# Implementation Plan: Core Experience

**Branch**: `001-core-experience` | **Date**: 2025-12-12 | **Spec**: [specs/001-core-experience/spec.md](../001-core-experience/spec.md)
**Input**: Feature specification from `/specs/001-core-experience/spec.md`

## Summary

Implement the core real-time translation loop with dual-stream architecture. The system captures audio, performs local ASR and translation (<500ms latency), and asynchronously generates cultural insights using a lightweight LLM and external search, all running on Apple Silicon via MLX.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript 5.0+ (Frontend)
**Primary Dependencies**: 
- Backend: FastAPI, mlx-whisper, mlx-lm, python-socketio, exa-py
- Frontend: React, Vite, Zustand, socket.io-client, shadcn/ui, onnxruntime-web (VAD)
**Storage**: N/A (Transient state only)
**Testing**: pytest (Backend), Vitest (Frontend)
**Target Platform**: macOS (Apple Silicon M1+), Localhost
**Project Type**: Web application (FastAPI + React)
**Performance Goals**: Translation latency < 500ms (P95), UI 60fps
**Constraints**: <6GB Memory, 4-bit quantization mandatory, Offline-first (except search)
**Scale/Scope**: Single user, local session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Local-First**: ✅ Uses MLX for on-device inference.
- **Architecture**: ✅ FastAPI + React + WebSocket architecture selected.
- **Latency**: ✅ Dual-stream design ensures cultural insights don't block translation.
- **Hardware**: ✅ 4-bit quantization and M1 support verified.
- **Models**: ✅ Uses specified distil-whisper and Qwen2.5-3B models.
- **UI/UX**: ✅ Optimistic updates and no spinners planned.
- **Type Safety**: ✅ TypeScript/Zod and Python/Pydantic enforced.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-experience/
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Running instructions
├── contracts/           # API/WebSocket schemas
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── agents/          # RouterAgent, LoRAManager
│   ├── audio/           # ASREngine
│   ├── api/             # WebSocket routes
│   ├── models/          # Pydantic schemas
│   └── main.py          # App entrypoint
└── tests/

frontend/
├── src/
│   ├── components/      # UI Components (Chat, SidePanel)
│   ├── hooks/           # WebSocket hooks
│   ├── store/           # Zustand state
│   └── lib/             # Audio processing
└── tests/
```

**Structure Decision**: Web application with separate frontend/backend directories as per Constitution Principle II.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (None)    | -          | -                                   |