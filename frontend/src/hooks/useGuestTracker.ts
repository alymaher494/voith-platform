import { useState, useCallback } from 'react';

const STORAGE_KEY = 'voith_guest_usage';

interface GuestUsageData {
    date: string;
    count: number;
}

/**
 * Get today's date in YYYY-MM-DD format
 */
const getTodayDate = (): string => {
    return new Date().toISOString().split('T')[0];
};

/**
 * Get current guest usage from localStorage
 */
const getStoredUsage = (): GuestUsageData => {
    try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (!stored) {
            return { date: getTodayDate(), count: 0 };
        }

        const parsed: GuestUsageData = JSON.parse(stored);

        // Reset if it's a new day
        if (parsed.date !== getTodayDate()) {
            return { date: getTodayDate(), count: 0 };
        }

        return parsed;
    } catch {
        return { date: getTodayDate(), count: 0 };
    }
};

/**
 * Hook for tracking guest usage limits
 * 
 * Guests get 1 free trial per day. After that, they are blocked.
 */
export const useGuestTracker = () => {
    const [usage, setUsage] = useState<GuestUsageData>(getStoredUsage);

    /**
     * Check if guest has reached their daily limit
     * @returns true if limit reached (count >= 1)
     */
    const checkGuestLimit = useCallback((): boolean => {
        const currentUsage = getStoredUsage();
        return currentUsage.count >= 1;
    }, []);

    /**
     * Increment the guest usage count
     * Should be called after a successful operation
     */
    const incrementGuestUsage = useCallback((): void => {
        const today = getTodayDate();
        const currentUsage = getStoredUsage();

        const newUsage: GuestUsageData = {
            date: today,
            count: currentUsage.date === today ? currentUsage.count + 1 : 1
        };

        localStorage.setItem(STORAGE_KEY, JSON.stringify(newUsage));
        setUsage(newUsage);
    }, []);

    /**
     * Get remaining free trials for today
     */
    const getRemainingTrials = useCallback((): number => {
        const currentUsage = getStoredUsage();
        return Math.max(0, 1 - currentUsage.count);
    }, []);

    /**
     * Reset usage (mainly for testing)
     */
    const resetUsage = useCallback((): void => {
        localStorage.removeItem(STORAGE_KEY);
        setUsage({ date: getTodayDate(), count: 0 });
    }, []);

    return {
        usage,
        checkGuestLimit,
        incrementGuestUsage,
        getRemainingTrials,
        resetUsage
    };
};
