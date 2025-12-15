# Local AI Cultural Mediator

> Real-time Speech Translation with Cultural Insights

A local-first AI system providing real-time English to Traditional Chinese translation with automatic detection and explanation of idioms, slang, and cultural references. Runs entirely on Apple Silicon for privacy and performance.

Built using the [Spec Kit](https://github.com/google/spec-kit) framework.

---

## Features

- **Real-time Translation**: Continuous speech-to-text with instant translation
- **Cultural Intelligence**: Automatic detection of idioms, slang, and cultural references
- **Web-Enhanced Insights**: Searches the web for context when cultural content is detected
- **Local-First**: Complete privacy - runs on your machine
- **Fine-Tuned Models**: Custom LoRA adapters for improved translation quality

---

## System Requirements

### Hardware
- **Apple Silicon**: M1 or newer
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 20GB available

### Software
- **macOS**: 12.0+ (Monterey or newer)
- **Python**: 3.11+
- **Node.js**: 18.0+
- **ffmpeg**: Required for audio processing

---

## Quick Start

### 1. Install Dependencies

#### Backend
```bash
cd backend

# Using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e .

# Or using pip
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
npm install
```

#### System Dependencies
```bash
# Install ffmpeg for audio processing
brew install ffmpeg
```

### 2. Environment Setup

Create a `.env` file or export environment variables:

```bash
export EXA_API_KEY=your_exa_api_key
```

Get your Exa API key from: https://exa.ai/

### 3. Start the Application

**Terminal 1 - Backend**:
```bash
cd backend
python -m src.main
```

On first run, the system will automatically download:
- Qwen2.5-3B-Instruct model (~6GB)
- Faster Whisper large-v3 model (~3GB)

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

### 4. Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```
please wait until "Model Ready", not just "Ready" on the upper right corner
---

## Usage

### Text Input
1. Type English text into the input box
2. Press Enter or click "Translate"
3. View the Traditional Chinese translation
4. If cultural content is detected, insights appear in the side panel

### Voice Input
1. Click the microphone button
2. Speak in English
3. Click again to stop
4. Translation and insights appear automatically

---

## Models

### Translation Model
- **Base**: Qwen/Qwen2.5-3B-Instruct
- **Adapters**: Custom LoRA fine-tuned for:
  - English → Traditional Chinese translation
  - Idiom understanding and cultural context

### Speech Recognition
- **Model**: faster-whisper (large-v3)
- **Processing**: Real-time streaming with VAD filtering

### Cultural Detection
- **Method**: LLM-based prompt analysis
- **Search**: Exa API for contextual information

---

## Fine-Tuning

The project includes pre-trained LoRA adapters. To train your own:

### Training Data

Located in `backend/training_data/`:
- `training.jsonl`: Basic English → Traditional Chinese pairs
- `idiom_training_data/`: Specialized idiom translations

Each entry follows the format:
```json
{
  "english": "break a leg",
  "traditional_chinese": "祝好運",
  "context": "A theatrical idiom wishing someone good luck"
}
```

### Running Training

```bash
cd backend
python train_translation.py  # Basic translation
python train_idioms.py       # Idiom specialization
```

Models are saved to `backend/adapters/`.

---

## Testing

### please be paitent after turn on backend, it will take a few minutes to download models

### Sample Inputs & Expected Results

#### Standard Language
```
Input: "I want a cheeseburger and a cup of tea please"
Expected: "我想要一個起司漢堡和一杯茶，謝謝"
Insights: None (standard language)
```

#### Modern Slang
```
Input: "They're being salty about losing the game"
Expected: "他們對輸掉比賽感到不滿"
Insights: Shows cultural explanation of "salty" with web sources
```

#### Cultural Idioms
```
Input: "break a leg with your presentation"
Expected: "祝你的簡報順利"
Insights: Explains theatrical origin and meaning
```

---

## Architecture

### Backend (Python/FastAPI)
```
src/
├── agents/           # LoRA fine-tuning & model management
├── audio/            # Speech-to-text with faster-whisper
├── services/         # Translation, insights, web search
├── api/              # WebSocket & REST endpoints
└── models/           # Data models & types
```

### Frontend (React/TypeScript)
```
src/
├── components/       # UI components
├── hooks/            # Audio capture, WebSocket
├── store/            # State management (Zustand)
└── lib/              # Utilities
```

### Communication Flow
1. Audio captured via WebAudioAPI
2. Streamed to backend via WebSocket
3. faster-whisper transcribes in real-time
4. LLM detects cultural content
5. If detected: Exa search → LLM explanation
6. Translation with cultural context
7. Results emitted to frontend

---

## Configuration

### Backend Settings

Edit `backend/src/config.py`:
- Model paths
- Server ports
- API endpoints
- VAD parameters

### Frontend Settings

Edit `frontend/src/lib/config.ts`:
- WebSocket URL
- API base URL
- UI preferences

---

## Development

### Project Structure
This project was developed using [Spec Kit](https://github.com/google/spec-kit), Google's specification-driven development framework.

See `specs/` directory for detailed feature specifications.

### Adding Features
1. Create specification in `specs/`
2. Implement backend service in `src/services/`
3. Add frontend hook/component
4. Update WebSocket events in `src/api/events.py`

### Testing Changes
```bash
# Backend
cd backend
pytest

# Frontend  
cd frontend
npm test
```

---

## Acknowledgments

- **Spec Kit**: Google's specification-driven development framework
- **MLX**: Apple's machine learning framework
- **Qwen**: Alibaba's language model
- **faster-whisper**: Efficient Whisper implementation
- **Exa**: Web search API
