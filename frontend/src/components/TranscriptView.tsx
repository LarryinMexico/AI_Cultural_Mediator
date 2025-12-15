import React, { useEffect, useRef } from 'react';
import { useAppStore } from '@/store/useAppStore';
import { ScrollArea } from "@/components/ui/scroll-area"

export const TranscriptView: React.FC = () => {
    const { transcript, translations } = useAppStore();
    const scrollRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [transcript, translations]);

    return (
        <ScrollArea className="h-[400px] w-full rounded-md border p-4 bg-card">
            <div className="flex flex-col gap-4">
                {transcript.length === 0 && (
                    <div className="text-center text-muted-foreground italic py-8">
                        Waiting for speech...
                    </div>
                )}
                
                {transcript.map((chunk) => {
                    const translation = translations.get(chunk.id);
                    
                    return (
                        <div key={chunk.id} className="flex flex-col gap-1 animate-in fade-in duration-300">
                            {/* Original Text */}
                            <div className="text-lg font-medium text-foreground">
                                {chunk.text}
                            </div>
                            
                            {/* Translation */}
                            {translation && (
                                <div className="text-base text-blue-500 font-normal ml-4 border-l-2 border-blue-500 pl-2">
                                    {translation.translated_text}
                                    <span className="text-xs text-muted-foreground ml-2">
                                        ({translation.latency_ms.toFixed(0)}ms)
                                    </span>
                                </div>
                            )}
                        </div>
                    );
                })}
                <div ref={scrollRef} />
            </div>
        </ScrollArea>
    );
};
