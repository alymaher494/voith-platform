import React from 'react';
import { motion } from 'framer-motion';

interface CartoucheCardProps {
    children: React.ReactNode;
    className?: string;
    title?: string;
}

export const CartoucheCard = ({ children, className = '', title }: CartoucheCardProps) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className={`relative bg-temple border border-gold/30 rounded-[2rem] p-8 shadow-xl overflow-hidden ${className}`}
        >
            {/* Decorative corners */}
            <div className="absolute top-0 left-0 w-16 h-16 border-t-2 border-l-2 border-gold/20 rounded-tl-[2rem] pointer-events-none" />
            <div className="absolute top-0 right-0 w-16 h-16 border-t-2 border-r-2 border-gold/20 rounded-tr-[2rem] pointer-events-none" />
            <div className="absolute bottom-0 left-0 w-16 h-16 border-b-2 border-l-2 border-gold/20 rounded-bl-[2rem] pointer-events-none" />
            <div className="absolute bottom-0 right-0 w-16 h-16 border-b-2 border-r-2 border-gold/20 rounded-br-[2rem] pointer-events-none" />

            {title && (
                <div className="mb-6 text-center">
                    <h3 className="text-2xl font-heading text-gold inline-block border-b-2 border-gold/30 pb-2 px-8">
                        {title}
                    </h3>
                </div>
            )}

            <div className="relative z-10">
                {children}
            </div>
        </motion.div>
    );
};
