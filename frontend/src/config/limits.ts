// Guest Mode Limits Configuration

/**
 * Maximum file size allowed for guest users (in bytes)
 * 50MB = 50 * 1024 * 1024
 */
export const GUEST_MAX_SIZE = 50 * 1024 * 1024; // 50MB

/**
 * Maximum audio/video duration for transcription (in seconds)
 */
export const GUEST_MAX_DURATION = 120; // 2 minutes

/**
 * Maximum number of operations per day for guest users
 */
export const GUEST_DAILY_LIMIT = 2;

/**
 * LocalStorage key for tracking guest usage
 */
export const GUEST_USAGE_KEY = 'voith_guest_usage';

/**
 * Get today's date string for usage tracking
 */
export const getTodayKey = (): string => {
    return new Date().toISOString().split('T')[0]; // YYYY-MM-DD
};

/**
 * Get current guest usage count for today
 */
export const getGuestUsageCount = (): number => {
    try {
        const usage = localStorage.getItem(GUEST_USAGE_KEY);
        if (!usage) return 0;

        const parsed = JSON.parse(usage);
        const today = getTodayKey();

        // Reset if it's a new day
        if (parsed.date !== today) {
            return 0;
        }

        return parsed.count || 0;
    } catch {
        return 0;
    }
};

/**
 * Increment guest usage count
 */
export const incrementGuestUsage = (): void => {
    const today = getTodayKey();
    const currentCount = getGuestUsageCount();

    localStorage.setItem(GUEST_USAGE_KEY, JSON.stringify({
        date: today,
        count: currentCount + 1
    }));
};

/**
 * Check if guest has exceeded daily limit
 */
export const hasExceededDailyLimit = (): boolean => {
    return getGuestUsageCount() >= GUEST_DAILY_LIMIT;
};

/**
 * Format file size for display
 */
export const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};
