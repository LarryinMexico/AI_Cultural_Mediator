import React from 'react';
import { useAppStore } from '@/store/useAppStore';
import { useModelStatus } from '@/hooks/useModelStatus';

export const StatusIndicator: React.FC = () => {
    const { status } = useAppStore();
    const { status: modelStatus } = useModelStatus();

    const getColor = () => {
        switch (status) {
            case 'listening':
                return 'bg-green-500 animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.5)]';
            case 'processing':
                return 'bg-blue-500 animate-bounce';
            case 'error':
                return 'bg-red-500';
            case 'idle':
            default:
                return 'bg-gray-400';
        }
    };

    const getLabel = () => {
        switch (status) {
            case 'listening':
                return 'Listening...';
            case 'processing':
                return 'Processing...';
            case 'error':
                return 'Connection Error';
            case 'idle':
            default:
                return 'Ready';
        }
    };

    const getModelStatus = () => {
        if (!modelStatus) return null;
        
        if (modelStatus.model_loading) {
            return <span className="text-yellow-500">(Loading model...)</span>;
        }
        if (modelStatus.model_loaded) {
            return <span className="text-green-500">(Model ready)</span>;
        }
        if (modelStatus.model_error) {
            return <span className="text-red-500">(Model error)</span>;
        }
        return <span className="text-gray-500">(Model not loaded)</span>;
    };

    return (
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-muted/50 border text-xs font-medium transition-all duration-300">
            <div className={`w-2.5 h-2.5 rounded-full ${getColor()} transition-all duration-300`} />
            <span className="text-muted-foreground">{getLabel()}</span>
            {getModelStatus()}
        </div>
    );
};
