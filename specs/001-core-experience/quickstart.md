# Quickstart: Core Experience

## Prerequisites

- Apple Silicon Mac (M1 or later)
- 8GB RAM minimum
- Python 3.11+
- Node.js 18+
- `uv` (recommended) or `pip`
- Exa AI API Key (set as `EXA_API_KEY`)

## Setup

1. **Clone & Install Backend**
   ```bash
   cd backend
   uv venv
   source .venv/bin/activate
   # Install dependencies
   uv pip install -e .
   # OR with pip directly
   pip install -r requirements.txt
   ```

2. **Install Frontend**
   ```bash
   cd frontend
   npm install
   ```

## Running the App

1. **Start Backend**
   ```bash
   # In backend/ directory
   export EXA_API_KEY=b1f5c1f3-b661-4c3f-97c6-524c03d818cf
   
   # Run with reloading enabled
   python -m src.main
   # Server starts at http://localhost:8000
   ```

2. **Start Frontend**
   ```bash
   # In frontend/ directory
   npm run dev
   # App runs at http://localhost:5173
   ```

## Verification

1. **Open App**: Go to http://localhost:5173
2. **Permissions**: Allow microphone access when prompted.
3. **Connect**: Verify the status indicator turns green/ready.
4. **Speak**: Say a phrase like "break a leg".
5. **Observe**:
   - Rolling transcript appears immediately.
   - Translation appears in blue text alongside transcript.
   - "break a leg" card appears in the side panel with cultural context.