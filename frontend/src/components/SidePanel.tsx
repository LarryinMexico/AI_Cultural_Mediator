import React, { useState, useEffect } from 'react';
import { useAppStore } from '@/store/useAppStore';
import { Lightbulb, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';

export const SidePanel: React.FC = () => {
    const { insights } = useAppStore();
    const [expandedId, setExpandedId] = useState<number | null>(null);

    // Auto-expand the latest (first) insight when new one arrives
    useEffect(() => {
        if (insights.length > 0) {
            setExpandedId(0); // Expand the newest (index 0)
        }
    }, [insights.length]);

    const toggleExpand = (index: number) => {
        setExpandedId(expandedId === index ? null : index);
    };

    return (
        <div className="w-[500px] border-l bg-card p-6 overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">Cultural Insights</h2>

            {insights.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                    No cultural insights yet.
                </p>
            ) : (
                <div className="space-y-3">
                    {insights.map((insight, idx) => {
                        const isExpanded = expandedId === idx;
                        return (
                            <div key={idx} className="border rounded-lg bg-background overflow-hidden">
                                {/* Header - Always visible, clickable */}
                                <div
                                    className="p-3 cursor-pointer hover:bg-muted/50 transition-colors flex items-center justify-between"
                                    onClick={() => toggleExpand(idx)}
                                >
                                    <div className="flex items-center gap-2 flex-1">
                                        <Lightbulb className="w-4 h-4 text-amber-500 flex-shrink-0" />
                                        <div>
                                            <h3 className="font-semibold text-sm">
                                                {insight.phrase || insight.source_text}
                                            </h3>
                                            <span className="text-xs text-muted-foreground">
                                                {insight.type || insight.context_type}
                                            </span>
                                        </div>
                                    </div>
                                    {isExpanded ? (
                                        <ChevronUp className="w-4 h-4 text-muted-foreground" />
                                    ) : (
                                        <ChevronDown className="w-4 h-4 text-muted-foreground" />
                                    )}
                                </div>

                                {/* Expandable content */}
                                {isExpanded && (
                                    <div className="px-3 pb-3 pt-0 border-t">
                                        <p className="text-sm text-foreground mt-2 mb-3 whitespace-pre-wrap">
                                            {insight.explanation}
                                        </p>

                                        {insight.sources && insight.sources.length > 0 && (
                                            <div className="mt-3 pt-3 border-t">
                                                <p className="text-xs font-semibold mb-2">Sources:</p>
                                                <div className="space-y-2">
                                                    {insight.sources.map((source: any, sidx: number) => (
                                                        <div key={sidx} className="text-xs">
                                                            {typeof source === 'string' ? (
                                                                <a
                                                                    href={source}
                                                                    target="_blank"
                                                                    rel="noopener noreferrer"
                                                                    className="text-primary hover:underline flex items-center gap-1"
                                                                >
                                                                    <ExternalLink className="w-3 h-3" />
                                                                    {source}
                                                                </a>
                                                            ) : (
                                                                <div className="border-l-2 border-primary/30 pl-2">
                                                                    <a
                                                                        href={source.url}
                                                                        target="_blank"
                                                                        rel="noopener noreferrer"
                                                                        className="text-primary hover:underline font-medium flex items-center gap-1 mb-1"
                                                                    >
                                                                        <ExternalLink className="w-3 h-3" />
                                                                        {source.title || 'Source'}
                                                                    </a>
                                                                    {source.snippet && (
                                                                        <p className="text-muted-foreground text-xs mt-1">
                                                                            {source.snippet}
                                                                        </p>
                                                                    )}
                                                                </div>
                                                            )}
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};
