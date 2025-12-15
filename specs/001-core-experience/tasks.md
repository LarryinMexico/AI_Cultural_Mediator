---
description: "Task list for Core Experience feature"
---

# Tasks: Core Experience

**Input**: Design documents from `/specs/001-core-experience/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/async-api.md, research.md
**Tests**: Tests are OPTIONAL (not explicitly requested), but manual verification steps are included.
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: [US1] = Real-time Translation, [US2] = Cultural Context

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directories (backend/src, frontend/src) per plan.md
- [x] T002 Initialize Python backend with `uv` and dependencies (FastAPI, python-socketio) in backend/pyproject.toml
- [x] T003 Install MLX dependencies (mlx-whisper, mlx-lm) in backend/requirements.txt
- [x] T004 Initialize React frontend with Vite + TypeScript in frontend/
- [x] T005 [P] Install frontend dependencies (socket.io-client, zustand, shadcn/ui) in frontend/package.json
- [x] T006 [P] Configure backend environment variables and logging in backend/src/config.py

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure MUST be complete before user stories

- [x] T007 Create basic FastAPI app with Socket.IO server in backend/src/main.py
- [x] T008 Implement shared Pydantic models (TranscriptChunk, Translation) in backend/src/models/core.py
- [x] T009 [P] Setup frontend Zustand store for app state in frontend/src/store/useAppStore.ts
- [x] T010 [P] Create basic WebSocket hook for connection management in frontend/src/hooks/useSocket.ts
- [x] T011 [P] Implement AudioWorklet processor for 16kHz PCM capture in frontend/public/audio-processor.js
- [x] T012 Verify basic client-server WebSocket connection with a "ping-pong" test

**Checkpoint**: Foundation ready - Client connects, audio pipeline skeleton exists.

---

## Phase 3: User Story 1 - Real-time Translation (Priority: P1)

**Goal**: User speaks -> Rolling transcript + Translation appears < 500ms

**Independent Test**: Speak into mic, verify transcript and translation appear in UI.

### Implementation

- [x] T013 [US1] Implement VAD (Silero) integration with `onnxruntime-web` in frontend/src/lib/vad.ts
- [x] T014 [US1] Create AudioCapture component using AudioWorklet + VAD in frontend/src/components/AudioCapture.tsx
- [x] T015 [US1] Implement `audio_chunk` emission logic (only when speech detected) in frontend/src/hooks/useAudio.ts
- [x] T016 [US1] Create `ASREngine` class wrapping `mlx-whisper` in backend/src/audio/asr.py
- [x] T017 [US1] Implement WebSocket event handler for `audio_chunk` to feed ASREngine in backend/src/api/events.py
- [x] T018 [US1] Implement `transcript_partial` emission from ASREngine to client in backend/src/api/events.py
- [x] T019 [US1] Create `TranslationService` (placeholder or simple MLX model call) in backend/src/services/translator.py
- [x] T020 [US1] Wire up TranslationService to transcript events and emit `translation_final` in backend/src/api/events.py
- [x] T021 [US1] Create `TranscriptView` component to render rolling text/translation in frontend/src/components/TranscriptView.tsx
- [x] T022 [US1] Integrate TranscriptView and AudioCapture into main App page in frontend/src/App.tsx

**Checkpoint**: Functional real-time translation loop.

---

## Phase 4: User Story 2 - Cultural Context & Idioms (Priority: P2)

**Goal**: Idioms detected -> Side panel shows cultural note + sources

**Independent Test**: Simulate "break a leg" input, verify side panel card appears.

### Implementation

- [x] T023 [US2] Implement `CulturalInsight` Pydantic model in backend/src/models/culture.py
- [x] T024 [US2] Create `LoRAManager` to load Qwen2.5-3B-4bit model in backend/src/agents/lora.py
- [x] T025 [US2] Implement `RouterAgent` logic with Chain-of-Thought (CoT) prompt for idiom detection in backend/src/agents/router.py
- [x] T026 [US2] Create `ExaClient` wrapper for search operations in backend/src/services/exa.py
- [x] T027 [US2] Implement `InsightGenerator` (Stream B) that uses Router + Exa asynchronously in backend/src/services/insight.py
- [x] T028 [US2] Update WebSocket handler to trigger InsightGenerator on final transcripts in backend/src/api/events.py
- [x] T029 [US2] Create `SidePanel` component to display cultural insights in frontend/src/components/SidePanel.tsx
- [x] T030 [US2] Create `InsightCard` component with source links in frontend/src/components/InsightCard.tsx
- [x] T031 [US2] Update main App layout to include responsive SidePanel in frontend/src/App.tsx
- [x] T032 [US2] Implement graceful fallback for Network Failure (offline Exa) in backend/src/services/insight.py

**Checkpoint**: Full dual-stream experience (Translation + Cultural Insights).

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Optimization and cleanup

- [x] T033 [P] Optimize UI with optimistic updates (local echo of transcript) in frontend/src/store/useAppStore.ts
- [x] T034 Implement gracefull error handling (e.g. model load failure) in backend/src/api/events.py
- [x] T035 Add connection status indicator in frontend/src/components/StatusIndicator.tsx
- [x] T036 Verify memory usage < 6GB under load (manual check)
- [x] T037 Measure and verify Translation Latency < 500ms (P95) using instrumentation
- [x] T038 Measure and verify UI Frame Rate (60fps) during rapid speech/updates
- [x] T039 Evaluate Cultural Relevance > 90% on a test set of 10 idioms
- [x] T040 Verify system stability under "Rapid Speech" (buffer clearing/backpressure) conditions
- [x] T041 Update quickstart.md with any new env var requirements

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Starts immediately.
- **Foundational (Phase 2)**: Depends on Setup. Blocks US1.
- **User Story 1 (Phase 3)**: Depends on Foundational.
- **User Story 2 (Phase 4)**: Depends on Foundational (can run parallel to US1 backend work, but best sequential for single dev).

### Parallel Opportunities

- Frontend components (T021, T022, T029, T030) can be built while Backend services (T016, T019, T024, T027) are implemented.
- Setup tasks (T005, T006) are independent.

## Implementation Strategy

### MVP First (User Story 1)

1. **Skeleton**: Get audio flowing from Browser -> Python -> Browser (Echo).
2. **ASR**: Replace Echo with MLX Whisper.
3. **Translation**: Add translation step.
4. **Validation**: Test latency and accuracy.

### Incremental Delivery (User Story 2)

1. **Mock Insight**: Trigger a fake insight on specific keyword.
2. **LLM Integration**: Connect Qwen model for detection.
3. **Search Integration**: Connect Exa for context.
4. **UI**: Polish the side panel.
