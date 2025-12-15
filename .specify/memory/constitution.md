<!-- Sync Impact Report
Version: 0.0.0 -> 1.0.0
Modified Principles: All (Initial Definition)
Added Sections: Principles VI, VII, VIII
Templates Status:
- .specify/templates/plan-template.md: ✅ (Generic gates compatible)
- .specify/templates/spec-template.md: ✅ (Generic requirements compatible)
- .specify/templates/tasks-template.md: ✅ (Generic tasks compatible)
-->
# Local AI Cultural Mediator Constitution

## Core Principles

### I. Local-First
All inference MUST run on Apple Silicon via MLX. Zero data shall leave the device, with the sole exception of necessary external search queries (e.g., Exa AI).

### II. Architecture
The system MUST be architected as a Python FastAPI backend (using MLX) paired with a React frontend, communicating via WebSockets on localhost. WebGPU-only implementations are STRICTLY FORBIDDEN.

### III. Latency & Performance
Translation latency MUST be less than 500ms. Cultural insights generation MUST NEVER block the translation stream; a dual-stream architecture is mandatory.

### IV. Hardware Standards
The system MUST support a minimum configuration of Apple M1 with 8GB RAM. 4-bit quantization for models is MANDATORY to ensure performance within these constraints.

### V. Model Standards
Allowed models are restricted to:
- `distil-whisper-large-v3` (ASR)
- `Qwen2.5-3B-Instruct-4bit` (LLM)
- `Exa AI Fast mode` (Search)

### VI. LoRA Strategy
LoRA usage is restricted to inference-time switching ONLY. No training shall occur on the user device. The architecture MUST support multi-adapter memory-resident configurations.

### VII. UI/UX Philosophy
The UI MUST utilize optimistic updates. Loading spinners are forbidden; the interface should feel instant and fluid.

### VIII. Type Safety
Strict typing is MANDATORY:
- Frontend: TypeScript + Zod
- Backend: Python 3.11+ + Pydantic

## Governance

### Amendment Process
This Constitution supersedes all other project practices. Amendments require a version bump, documentation of the change rationale, and a migration plan for existing code.

### Compliance
All Pull Requests and code reviews MUST verify compliance with these principles. Deviations are not permitted without a constitutional amendment.

**Version**: 1.0.0 | **Ratified**: 2025-12-12 | **Last Amended**: 2025-12-12