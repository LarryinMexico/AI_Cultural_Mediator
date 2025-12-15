# Feature Specification: Core Experience (Instant Translation & Cultural Context)

**Feature Branch**: `001-core-experience`  
**Created**: 2025-12-12  
**Status**: Draft  
**Input**: User description: "As a non-native speaker, I want instant translation WITH cultural context so I understand idioms and references, not just words. Flow: 1. User speaks → rolling transcript appears 2. Translation shows in main chat (< 500ms) 3. If idiom detected → side panel shows cultural note + web sources (async) Success Metrics: - Translation latency < 500ms (P95) - Cultural relevance > 90% - Memory < 6GB on M1 8GB - Zero UI freezing (60fps) Out of scope: Training, multi-speaker, video input"

## User Scenarios & Testing

### User Story 1 - Real-time Translation (Priority: P1)

As a user listening to foreign speech, I want to see a real-time transcript and translation so that I can follow the literal meaning of the conversation instantly.

**Why this priority**: Core functionality. Without low-latency translation, the tool is unusable for live interaction.

**Independent Test**: Can be tested by playing audio clips and verifying transcript/translation appear on screen within 500ms.

**Acceptance Scenarios**:

1. **Given** the app is listening, **When** speech occurs, **Then** a rolling transcript of the original audio appears immediately.
2. **Given** the transcript is updating, **When** a sentence or phrase is formed, **Then** the translation appears in the main chat view within 500ms.
3. **Given** continuous speech, **When** new chunks arrive, **Then** the UI updates without freezing (maintaining 60fps).

---

### User Story 2 - Cultural Context & Idioms (Priority: P2)

As a non-native speaker, I want cultural notes and idiom explanations to appear in a side panel so that I understand the nuance behind the literal words.

**Why this priority**: The key differentiator ("Cultural Mediator"). Adds depth to the translation.

**Independent Test**: Can be tested by simulating input text containing known idioms and verifying the side panel populates with correct explanations and sources.

**Acceptance Scenarios**:

1. **Given** speech containing an idiom (e.g., "break a leg"), **When** it is processed, **Then** the main translation continues uninterrupted.
2. **Given** an idiom is detected, **When** background processing completes, **Then** a card appears in the side panel with the definition and cultural context.
3. **Given** a cultural note is generated, **When** displayed, **Then** it includes links to external web sources (via search) for further reading.
4. **Given** multiple idioms in quick succession, **When** detected, **Then** the side panel updates or stacks cards without blocking the main translation stream.

### Edge Cases

- **Silence/Noise**: If no speech is detected or audio is unintelligible, the transcript should not halluncinate text; the UI should remain in a "listening" state.
- **Network Failure**: If fetching cultural sources fails (e.g., offline or API error), the side panel should show the detected idiom and local definition (if available) or a graceful error, without crashing the main translation.
- **No Idioms**: If the conversation is purely literal, the side panel should remain collapsed or empty to avoid clutter.
- **Rapid Speech**: If the speaker talks faster than the model can process (causing latency spike), the system should prioritize keeping the audio buffer clear and may drop cultural insight generation to maintain translation sync.

## Requirements

### Functional Requirements

- **FR-001**: System MUST capture audio input and generate a rolling text transcript (ASR).
- **FR-002**: System MUST translate transcribed text into the user's target language with a P95 latency of < 500ms.
- **FR-003**: System MUST identify idioms and cultural references within the input text parallel to the translation process.
- **FR-004**: System MUST retrieve cultural context and web sources (using Exa AI Fast mode per Constitution) for identified items.
- **FR-005**: System MUST display cultural insights in a dedicated side panel.
- **FR-006**: The cultural insight generation MUST be asynchronous and NEVER block the main translation/transcript flow.
- **FR-007**: System MUST use 4-bit quantized models for inference to respect hardware constraints.

### Key Entities

- **TranscriptChunk**: Raw text from ASR with timestamp.
- **Translation**: Translated text corresponding to a TranscriptChunk.
- **CulturalInsight**: Structure containing the detected term, explanation, context, and list of URL sources.

### Assumptions

- Input audio is clear enough for ASR (distil-whisper-large-v3).
- User is on a device meeting the M1/8GB minimum requirement.
- "Web sources" implies using the configured search provider (Exa AI) as per project constitution.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Translation P95 latency is strictly < 500ms from speech end to text display.
- **SC-002**: Cultural relevance score is > 90% (measured by manual evaluation of test set).
- **SC-003**: System memory usage remains < 6GB at all times during operation.
- **SC-004**: UI rendering maintains 60fps, with zero frames dropped during simultaneous translation and insight generation.
