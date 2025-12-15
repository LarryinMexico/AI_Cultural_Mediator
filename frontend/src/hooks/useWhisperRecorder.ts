import { useState, useRef } from 'react';

export const useWhisperRecorder = () => {
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const chunksRef = useRef<Blob[]>([]);

    const startRecording = async () => {
        try {
            console.log("Starting recording...");

            const stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true,
                }
            });

            console.log("Microphone access granted");

            // Check available MIME types
            const mimeType = MediaRecorder.isTypeSupported('audio/webm')
                ? 'audio/webm'
                : 'audio/mp4';

            console.log(`Using MIME type: ${mimeType}`);

            const mediaRecorder = new MediaRecorder(stream, { mimeType });
            mediaRecorderRef.current = mediaRecorder;
            chunksRef.current = [];

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    chunksRef.current.push(e.data);
                    console.log(`Audio chunk: ${e.data.size} bytes`);
                }
            };

            mediaRecorder.onstop = async () => {
                console.log("Recording stopped, processing...");
                setIsProcessing(true);

                const audioBlob = new Blob(chunksRef.current, { type: mimeType });
                console.log(`Total audio size: ${audioBlob.size} bytes`);

                await uploadAudio(audioBlob);
                setIsProcessing(false);

                // Stop all tracks
                stream.getTracks().forEach(track => {
                    track.stop();
                    console.log("Track stopped");
                });
            };

            mediaRecorder.start();
            setIsRecording(true);
            console.log("Recording started");

        } catch (error) {
            console.error('Recording error:', error);
            alert(`Cannot access microphone: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current?.state === 'recording') {
            console.log("Stopping recording...");
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
    };

    const uploadAudio = async (audioBlob: Blob) => {
        try {
            console.log("Uploading audio to backend...");

            const formData = new FormData();
            formData.append('file', audioBlob, 'recording.webm');

            const response = await fetch('http://localhost:8000/api/transcribe', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const result = await response.json();
            console.log('Transcription result:', result);

        } catch (error) {
            console.error('Upload error:', error);
            alert(`Failed to transcribe audio: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }
    };

    return {
        isRecording,
        isProcessing,
        startRecording,
        stopRecording
    };
};
