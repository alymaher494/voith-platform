-- ==============================================================================
-- VOITH SAAS PLATFORM SCHEMA MIGRATION
-- ==============================================================================
-- This script upgrades the database to support multi-tenancy, subscriptions, and usage tracking.

-- ------------------------------------------------------------------------------
-- 1. SETUP & ENUMS
-- ------------------------------------------------------------------------------

-- Create custom types if they don't exist
DO $$ BEGIN
    CREATE TYPE subscription_status AS ENUM ('active', 'canceled', 'past_due', 'trialing');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ------------------------------------------------------------------------------
-- 2. USER PROFILES (The Identity)
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Trigger to create a profile automatically when a new user signs up in auth.users
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, avatar_url)
    VALUES (
        new.id,
        new.email,
        new.raw_user_meta_data->>'full_name',
        new.raw_user_meta_data->>'avatar_url'
    );
    
    -- Also initialize usage metrics for the new user
    INSERT INTO public.usage_metrics (user_id)
    VALUES (new.id);
    
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Drop trigger if exists to avoid duplication errors on re-runs
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- ------------------------------------------------------------------------------
-- 3. SUBSCRIPTIONS (The Treasury)
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.subscriptions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL UNIQUE,
    status subscription_status NOT NULL DEFAULT 'trialing',
    plan_id TEXT NOT NULL DEFAULT 'price_free',
    current_period_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ------------------------------------------------------------------------------
-- 4. USAGE METRICS (The Scales)
-- ------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.usage_metrics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL UNIQUE,
    storage_used_bytes BIGINT DEFAULT 0,
    minutes_processed FLOAT DEFAULT 0,
    max_storage_limit BIGINT DEFAULT 1073741824, -- Default 1GB
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ------------------------------------------------------------------------------
-- 5. FILES TABLE ENHANCEMENT (The Archives)
-- ------------------------------------------------------------------------------

-- Ensure the existing files table has the necessary structure
CREATE TABLE IF NOT EXISTS public.files (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    filename TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    size_bytes BIGINT DEFAULT 0,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE
);

-- Note: If the 'files' table already existed without user_id from the previous non-SaaS version,
-- you would need to run:
-- ALTER TABLE public.files ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE;
-- However, we are assuming a fresh or compatible state here.

-- ------------------------------------------------------------------------------
-- 6. SECURITY: ROW LEVEL SECURITY (RLS) POLICIES
-- ------------------------------------------------------------------------------

-- ENABLE RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.usage_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.files ENABLE ROW LEVEL SECURITY;

-- POLICIES FOR profiles
CREATE POLICY "Users can view their own profile" 
ON public.profiles FOR SELECT 
USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" 
ON public.profiles FOR UPDATE 
USING (auth.uid() = id);

-- POLICIES FOR subscriptions
-- Only specific roles (service_role) should insert/update/delete subscriptions usually,
-- but users need to read their status.
CREATE POLICY "Users can view their own subscription" 
ON public.subscriptions FOR SELECT 
USING (auth.uid() = user_id);

-- POLICIES FOR usage_metrics
CREATE POLICY "Users can view their own usage" 
ON public.usage_metrics FOR SELECT 
USING (auth.uid() = user_id);

-- POLICIES FOR files
CREATE POLICY "Users can view their own files" 
ON public.files FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can upload their own files" 
ON public.files FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own files" 
ON public.files FOR UPDATE 
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own files" 
ON public.files FOR DELETE 
USING (auth.uid() = user_id);

-- STORAGE BUCKET POLICIES (Assuming bucket is 'processed_files')
-- These commands usually need to be run in the Storage section, but adding SQL representation here.
-- insert into storage.buckets (id, name) values ('processed_files', 'processed_files');
-- create policy "Authenticated users can upload to processed_files"
-- on storage.objects for insert with check ( bucket_id = 'processed_files' and auth.role() = 'authenticated' );

