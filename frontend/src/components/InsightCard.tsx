import React from 'react';
import { CulturalInsight } from '@/store/useAppStore';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ExternalLink } from 'lucide-react';

interface InsightCardProps {
    insight: CulturalInsight;
}

export const InsightCard: React.FC<InsightCardProps> = ({ insight }) => {
    return (
        <Card className="overflow-hidden animate-in slide-in-from-right duration-500">
            <CardHeader className="p-4 pb-2">
                <div className="flex justify-between items-start gap-2">
                    <CardTitle className="text-lg font-bold">
                        "{insight.source_text}"
                    </CardTitle>
                    <Badge variant="secondary" className="capitalize shrink-0">
                        {insight.context_type}
                    </Badge>
                </div>
            </CardHeader>
            <CardContent className="p-4 pt-2 space-y-3">
                <div className="text-sm text-foreground">
                    {insight.explanation}
                </div>
                
                {insight.sources && insight.sources.length > 0 && (
                    <div className="pt-2 border-t">
                        <p className="text-xs text-muted-foreground mb-1 font-semibold">Sources:</p>
                        <div className="flex flex-col gap-1">
                            {insight.sources.map((source, idx) => (
                                <a 
                                    key={idx} 
                                    href={source} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="text-xs text-blue-500 hover:underline flex items-center gap-1 truncate"
                                >
                                    <ExternalLink className="w-3 h-3 shrink-0" />
                                    {new URL(source).hostname}
                                </a>
                            ))}
                        </div>
                    </div>
                )}
            </CardContent>
        </Card>
    );
};
