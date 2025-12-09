import axios from 'axios';
import { supabase } from './supabase';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to attach the Supabase token
// Add a request interceptor to attach the Supabase token
api.interceptors.request.use(async (config) => {
    try {
        const { data: { session } } = await supabase.auth.getSession();
        if (session?.access_token) {
            config.headers.Authorization = `Bearer ${session.access_token}`;
        }
    } catch (error) {
        console.warn("⚠️ Failed to attach auth token:", error);
    }
    return config;
});

export const downloaderService = {
    download: async (url: string, format?: string, quality?: string, audioOnly?: boolean) => {
        return api.post('/downloader/download', {
            url,
            format_id: format,
            quality,
            audio_only: audioOnly
        });
    },
    getJobStatus: async (jobId: string) => {
        return api.get(`/downloader/status/${jobId}`);
    }
};

export const converterService = {
    convert: async (file: File, outputFormat: string) => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('output_format', outputFormat);

        return api.post('/converter/convert/video', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    }
};

export const asrService = {
    transcribe: async (file: File, language: string = 'auto', model: string = 'base') => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('language', language);
        formData.append('model_size', model);

        // Determine endpoint based on file type
        const endpoint = file.type.startsWith('video/')
            ? '/asr/transcribe/video/upload'
            : '/asr/transcribe/audio/upload';

        return api.post(endpoint, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    }
};

export const ocrService = {
    extract: async (file: File, languages: string[] = ['eng']) => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('languages', JSON.stringify(languages));

        return api.post('/ocr/extract', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    }
};

// --- New Integration Function ---
export const processMedia = async (file: File, language?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    if (language && language !== 'auto') {
        formData.append('language', language);
    }

    console.log("📤 Sending file to backend:", file.name);

    // Using the simplified endpoint created in backend/main.py
    const response = await api.post('/transcribe', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    });

    console.log("✅ Backend Response:", response.data);
    return response.data;
};
