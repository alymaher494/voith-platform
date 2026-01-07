import React from 'react';
import { API_BASE_URL } from '../lib/api';

/**
 * Temporary Debug Component to visualize environment variables in production.
 * This should be removed after the issue is resolved.
 */
export const DebugEnv: React.FC = () => {
    // Only show if explicitly requested via query param or in development, 
    // or just always show for this debugging session as requested by user.
    return (
        <div style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            backgroundColor: 'rgba(0, 0, 0, 0.85)',
            color: '#00ff00',
            padding: '15px',
            borderRadius: '8px',
            zIndex: 9999,
            fontSize: '12px',
            fontFamily: 'monospace',
            border: '1px solid #d1ae76',
            boxShadow: '0 0 10px rgba(209, 174, 118, 0.5)',
            maxWidth: '300px',
            wordBreak: 'break-all'
        }}>
            <div style={{ color: '#d1ae76', fontWeight: 'bold', marginBottom: '8px', borderBottom: '1px solid #333', paddingBottom: '4px' }}>
                🔍 RUNTIME DEBUGGER
            </div>
            <div><strong>NODE_ENV:</strong> {import.meta.env.MODE}</div>
            <div><strong>VITE_API_URL (Raw):</strong> {import.meta.env.VITE_API_URL || 'undefined'}</div>
            <div style={{ marginTop: '8px', color: '#ffcc00' }}>
                <strong>Final API_BASE_URL:</strong><br />
                {API_BASE_URL}
            </div>
            <div style={{ fontSize: '10px', marginTop: '10px', color: '#888', fontStyle: 'italic' }}>
                Check console for: 🚨 CURRENT API URL
            </div>
        </div>
    );
};
