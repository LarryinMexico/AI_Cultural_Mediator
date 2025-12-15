import React, { useState } from 'react';
import { Button } from "@/components/ui/button"
import { Send } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';

export const TextInputTest: React.FC = () => {
    const [text, setText] = useState('');
    const [loading, setLoading] = useState(false);
    const addTranscriptChunk = useAppStore((state) => state.addTranscriptChunk);
    const updateTranslation = useAppStore((state) => state.updateTranslation);
    const addInsight = useAppStore((state) => state.addInsight);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!text.trim() || loading) return;

        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/test-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text.trim() }),
            });

            if (!response.ok) {
                throw new Error('Failed to send text');
            }

            const data = await response.json();
            console.log('Received response:', data);

            // Generate ID for this transcript
            const chunkId = `test-${Date.now()}`;

            // Display transcript
            addTranscriptChunk({
                id: chunkId,
                text: data.source_text,
                is_final: true,
                timestamp: Date.now(),
                confidence: 1.0
            });

            // Display translation
            if (data.translated_text) {
                updateTranslation({
                    chunk_id: chunkId,
                    target_lang: data.target_lang,
                    translated_text: data.translated_text,
                    latency_ms: 0
                });
            }

            // Display cultural insight
            if (data.cultural_insight) {
                addInsight({
                    source_text: data.cultural_insight.phrase,
                    phrase: data.cultural_insight.phrase,
                    explanation: data.cultural_insight.explanation,
                    context_type: data.cultural_insight.type as "idiom" | "historical" | "slang" | "etiquette",
                    type: data.cultural_insight.type,
                    sources: data.cultural_insight.sources
                });
            }

            setText('');
        } catch (error) {
            console.error('Error sending text:', error);
            alert('Failed to send text. Make sure backend is running.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-4 border rounded-lg bg-card">
            <h3 className="text-sm font-semibold mb-2">Type text</h3>
            <form onSubmit={handleSubmit} className="flex gap-2">
                <input
                    type="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Type English text to translate..."
                    className="flex-1 px-3 py-2 border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                    disabled={loading}
                />
                <Button
                    type="submit"
                    disabled={loading || !text.trim()}
                    size="icon"
                >
                    <Send className="w-4 h-4" />
                </Button>
            </form>

        </div>
    );
};
