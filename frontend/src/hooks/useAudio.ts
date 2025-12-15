import { useState, useRef, useEffect, useCallback } from 'react';
import { useSocket } from './useSocket';
import { vad } from '../lib/vad';

export const useAudio = () => {
    const [isListening, setIsListening] = useState(false);
    const [isSpeechDetected, setIsSpeechDetected] = useState(false);
    const audioContextRef = useRef<AudioContext | null>(null);
    const workletNodeRef = useRef<AudioWorkletNode | null>(null);
    const sourceNodeRef = useRef<MediaStreamAudioSourceNode | null>(null);
    const streamRef = useRef<MediaStream | null>(null);
    const workletLoadedRef = useRef<boolean>(false); // Track if worklet is loaded
    const socket = useSocket();

    useEffect(() => {
        // VAD initialization is disabled for now due to Vite compatibility issues
        // System works fine without VAD - all audio will be sent to backend
        // TODO: Re-enable VAD once we fix the .mjs file loading issue
        // vad.init().catch((e) => {
        //     console.warn('VAD initialization failed, continuing without VAD:', e);
        // });

        return () => {
            stopCapture();
        };
    }, []);

    const startCapture = useCallback(async () => {
        try {
            if (!audioContextRef.current) {
                audioContextRef.current = new AudioContext({ sampleRate: 16000 });
            }

            if (audioContextRef.current.state === 'suspended') {
                await audioContextRef.current.resume();
            }

            // Load AudioWorklet module only once
            if (!workletLoadedRef.current) {
                try {
                    await audioContextRef.current.audioWorklet.addModule('/audio-processor.js');
                    workletLoadedRef.current = true;
                    console.log('AudioWorklet loaded successfully');
                } catch (error) {
                    // Module might already be loaded, this is okay
                    console.log('AudioWorklet module already loaded or error:', error);
                    workletLoadedRef.current = true; // Mark as loaded anyway
                }
            }

            // Get microphone access
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    channelCount: 1,
                    sampleRate: 16000,
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true, // Added autoGainControl
                }
            });
            console.log("Mic permission granted");
            console.log("Audio tracks:", stream.getAudioTracks());
            streamRef.current = stream;

            const source = audioContextRef.current.createMediaStreamSource(stream);
            sourceNodeRef.current = source;

            const workletNode = new AudioWorkletNode(audioContextRef.current, 'audio-processor');
            workletNodeRef.current = workletNode;

            let chunkCount = 0; // For debug logging
            workletNode.port.onmessage = async (event) => {
                const audioData = event.data; // Float32Array from AudioWorklet

                // DEBUG: Log audio levels periodically
                if (chunkCount % 50 === 0) {
                    const rms = Math.sqrt(audioData.reduce((sum, val) => sum + val * val, 0) / audioData.length);
                    console.log(`Audio RMS: ${rms.toFixed(4)} ${rms > 0.01 ? '(DETECTED)' : '(silent)'}`);
                }
                chunkCount++;

                // Process VAD (returns 1.0 if VAD not available, so all audio is sent)
                const probability = await vad.process(audioData);
                const isSpeech = probability > 0.5;
                setIsSpeechDetected(isSpeech);

                // Send to backend (VAD will return 1.0 if not available, so all audio is sent)
                if (socket && socket.connected) {
                    socket.emit('audio_chunk', audioData.buffer);
                    if (chunkCount === 1) {
                        console.log("First audio chunk sent, size:", audioData.buffer.byteLength);
                    }
                } else if (chunkCount % 100 === 0) {
                    // Only log occasionally to avoid spam
                    console.warn("Socket not connected, buffering audio...");
                }
            };

            source.connect(workletNode);
            workletNode.connect(audioContextRef.current.destination);

            setIsListening(true);
            console.log('Audio capture started');
        } catch (error) {
            console.error('Failed to start audio capture:', error);
            setIsListening(false);
        }
    }, [socket]);

    const stopCapture = useCallback(() => {
        console.log('Stopping audio capture...');

        // Disconnect audio nodes first
        if (workletNodeRef.current) {
            try {
                workletNodeRef.current.port.onmessage = null; // Remove event listener
                workletNodeRef.current.disconnect();
                workletNodeRef.current = null;
                console.log('WorkletNode disconnected');
            } catch (e) {
                console.error('Error disconnecting worklet:', e);
            }
        }

        if (sourceNodeRef.current) {
            try {
                sourceNodeRef.current.disconnect();
                sourceNodeRef.current = null;
                console.log('SourceNode disconnected');
            } catch (e) {
                console.error('Error disconnecting source:', e);
            }
        }

        // Stop the media stream tracks
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => {
                track.stop();
                console.log('Track stopped:', track.kind);
            });
            streamRef.current = null;
        }

        // Do not suspend the AudioContext here, as it might be reused.
        // It will be garbage collected when the component unmounts if not reused.

        setIsListening(false);
        setIsSpeechDetected(false);
        console.log('Audio capture stopped completely');
    }, []);

    const toggleListening = useCallback(() => {
        if (isListening) {
            stopCapture();
        } else {
            startCapture();
        }
    }, [isListening, startCapture, stopCapture]);

    return {
        isListening,
        isSpeechDetected,
        toggleListening,
        startCapture,
        stopCapture
    };
};
