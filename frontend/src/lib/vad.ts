// VAD is currently disabled due to Vite compatibility issues with .mjs files
// System works fine without VAD - all audio will be sent to backend
// TODO: Re-enable VAD once we fix the .mjs file loading issue

// import * as ort from 'onnxruntime-web';

export class VAD {
    // VAD is currently disabled - always return 1.0 to send all audio
    // This allows the system to work without VAD filtering
    
    async init() {
        // VAD initialization disabled - no-op
        // System works fine without VAD
    }

    async process(audioFrame: Float32Array): Promise<number> {
        // Always return 1.0 to send all audio (no VAD filtering)
        // This is fine for testing - backend can handle all audio
        return 1.0;
    }
}

export const vad = new VAD();
