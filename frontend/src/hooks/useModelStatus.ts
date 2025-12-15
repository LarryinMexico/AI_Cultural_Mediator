import { useEffect, useState } from 'react';

interface ModelStatus {
    model_loaded: boolean;
    model_loading: boolean;
    model_path: string;
    model_error: string | null;
}

export const useModelStatus = () => {
    const [status, setStatus] = useState<ModelStatus | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkStatus = async () => {
            try {
                const response = await fetch('http://localhost:8000/health');
                const data = await response.json();
                setStatus(data);
            } catch (error) {
                console.error('Error checking model status:', error);
            } finally {
                setLoading(false);
            }
        };

        checkStatus();
        const interval = setInterval(checkStatus, 3000); // Check every 3 seconds

        return () => clearInterval(interval);
    }, []);

    return { status, loading };
};

