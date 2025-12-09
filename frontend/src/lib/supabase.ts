import { createClient } from '@supabase/supabase-js';

// Supabase configuration
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

// Validate environment variables
if (!supabaseUrl || !supabaseAnonKey) {
    console.warn(
        '⚠️ Supabase credentials not found. Please configure .env file with VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY'
    );
}

// Create Supabase client
export const supabase = createClient(supabaseUrl || '', supabaseAnonKey || '', {
    auth: {
        autoRefreshToken: true,
        persistSession: true,
        detectSessionInUrl: true
    }
});

// Database Types (will be auto-generated later with Supabase CLI)
export type Database = {
    public: {
        Tables: {
            user_profiles: {
                Row: {
                    id: string;
                    username: string | null;
                    full_name: string | null;
                    avatar_url: string | null;
                    plan_id: string | null;
                    storage_used: number;
                    created_at: string;
                    updated_at: string;
                };
                Insert: {
                    id: string;
                    username?: string | null;
                    full_name?: string | null;
                    avatar_url?: string | null;
                    plan_id?: string | null;
                    storage_used?: number;
                    created_at?: string;
                    updated_at?: string;
                };
                Update: {
                    id?: string;
                    username?: string | null;
                    full_name?: string | null;
                    avatar_url?: string | null;
                    plan_id?: string | null;
                    storage_used?: number;
                    created_at?: string;
                    updated_at?: string;
                };
            };
            files: {
                Row: {
                    id: string;
                    user_id: string;
                    filename: string;
                    original_filename: string | null;
                    file_type: string | null;
                    mime_type: string | null;
                    size_bytes: number | null;
                    storage_path: string | null;
                    public_url: string | null;
                    metadata: any;
                    created_at: string;
                };
            };
            jobs: {
                Row: {
                    id: string;
                    user_id: string;
                    job_type: string;
                    status: string;
                    progress: number;
                    input_data: any;
                    output_file_id: string | null;
                    error_message: string | null;
                    started_at: string | null;
                    completed_at: string | null;
                    created_at: string;
                };
            };
        };
    };
};
