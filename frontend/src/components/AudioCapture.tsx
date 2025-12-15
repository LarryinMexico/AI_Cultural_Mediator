import React from 'react';
import { Mic, MicOff, Activity } from 'lucide-react';
import { Button } from "@/components/ui/button"
import { useAudio } from "@/hooks/useAudio"

export const AudioCapture: React.FC = () => {
    const { isListening, isSpeechDetected, toggleListening } = useAudio();

    return (
        <div className="flex items-center gap-4 p-4 border rounded-lg bg-card">
            <Button 
                variant={isListening ? "destructive" : "default"}
                size="icon"
                onClick={toggleListening}
                className="w-12 h-12 rounded-full"
            >
                {isListening ? <MicOff className="w-6 h-6" /> : <Mic className="w-6 h-6" />}
            </Button>
            
            <div className="flex flex-col">
                <span className="font-semibold">
                    {isListening ? "Listening..." : "Microphone off"}
                </span>
                {isListening && (
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Activity className={`w-4 h-4 ${isSpeechDetected ? "text-green-500 animate-pulse" : "text-gray-400"}`} />
                        <span>{isSpeechDetected ? "Speech detected" : "Silence"}</span>
                    </div>
                )}
            </div>
        </div>
    );
};
