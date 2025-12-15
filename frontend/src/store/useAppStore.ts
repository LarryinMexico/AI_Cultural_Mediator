import { create } from 'zustand'

export interface TranscriptChunk {
    id: string
    text: string
    is_final: boolean
    timestamp: number
    confidence: number
}

export interface Translation {
    chunk_id: string
    target_lang: string
    translated_text: string
    latency_ms: number
}

export interface CulturalInsight {
    id?: string
    source_text: string
    phrase: string  // alias for source_text
    explanation: string
    context_type: "idiom" | "historical" | "slang" | "etiquette"
    type: string  // alias for context_type
    sources: Array<{ url: string, title: string, snippet: string }>
    relevance_score?: number
}

interface AppState {
    status: 'idle' | 'listening' | 'processing' | 'error'
    transcript: TranscriptChunk[]
    translations: Map<string, Translation>
    insights: CulturalInsight[]

    setStatus: (status: AppState['status']) => void
    addTranscriptChunk: (chunk: TranscriptChunk) => void
    updateTranslation: (translation: Translation) => void
    addInsight: (insight: CulturalInsight) => void
    clearTranscript: () => void
    reset: () => void
}

export const useAppStore = create<AppState>((set) => ({
    status: 'idle',
    transcript: [],
    translations: new Map(),
    insights: [],

    setStatus: (status) => set({ status }),

    addTranscriptChunk: (chunk) => set((state) => {
        // If chunk exists (by ID), update it. Otherwise append.
        const existingIndex = state.transcript.findIndex(c => c.id === chunk.id);
        if (existingIndex !== -1) {
            const newTranscript = [...state.transcript];
            newTranscript[existingIndex] = chunk;
            return { transcript: newTranscript };
        }
        return { transcript: [...state.transcript, chunk] };
    }),

    updateTranslation: (translation) => set((state) => {
        const newTranslations = new Map(state.translations);
        newTranslations.set(translation.chunk_id, translation);
        return { translations: newTranslations };
    }),

    addInsight: (insight) => set((state) => {
        // Check if insight with same source_text already exists
        const existingIndex = state.insights.findIndex(
            i => (i.phrase || i.source_text).toLowerCase() === (insight.phrase || insight.source_text).toLowerCase()
        );

        if (existingIndex !== -1) {
            // Move existing to top (most recent)
            const updated = [...state.insights];
            const [existing] = updated.splice(existingIndex, 1);
            return { insights: [existing, ...updated] };
        }

        // Add new insight at the beginning
        return { insights: [insight, ...state.insights] };
    }),

    clearTranscript: () => set({ transcript: [], translations: new Map() }),

    reset: () => set({
        status: 'idle',
        transcript: [],
        translations: new Map(),
        insights: []
    })
}))
