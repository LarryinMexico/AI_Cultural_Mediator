import { useEffect, useRef } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAppStore } from '../store/useAppStore';

const SOCKET_URL = 'http://localhost:8000';

export const useSocket = () => {
    const socketRef = useRef<Socket | null>(null);
    const {
        addTranscriptChunk,
        updateTranslation,
        addInsight,
        setStatus
    } = useAppStore();

    useEffect(() => {
        if (!socketRef.current) {
            socketRef.current = io(SOCKET_URL, {
                transports: ['websocket'],
                autoConnect: true
            });

            const socket = socketRef.current;

            socket.on('connect', () => {
                console.log('Socket connected');
                setStatus('idle');
            });

            socket.on('disconnect', () => {
                console.log('Socket disconnected');
                setStatus('error');
            });

            socket.on('connect_error', (err) => {
                console.error('Socket connect error:', err);
                setStatus('error');
            });

            socket.on('transcript_partial', (data: any) => {
                console.log('Received transcript_partial:', data);
                // Immediately display English text
                useAppStore.getState().addTranscriptChunk({
                    id: data.id || data.chunk_id || `transcript-${Date.now()}`,
                    text: data.text,
                    is_final: data.is_final || false,
                    timestamp: data.timestamp || Date.now(),
                    confidence: data.confidence || 1.0
                });
                setStatus('listening');
            });

            socket.on('translation_final', (translation) => {
                updateTranslation(translation);
            });

            socket.on('cultural_insight', (insight) => {
                addInsight(insight);
            });
        }

        return () => {
            if (socketRef.current) {
                socketRef.current.disconnect();
                socketRef.current = null;
            }
        };
    }, [addTranscriptChunk, updateTranslation, addInsight, setStatus]);

    return socketRef.current;
};
