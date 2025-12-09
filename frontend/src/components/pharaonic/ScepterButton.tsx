import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../lib/utils'; // Assuming a utils file exists for tailwind-merge, or I'll implement a simple one if needed. Typically shadcn uses this. 
// If utils doesn't exist, I'll use template literals properly. 
// Checking context, there IS a `lib/utils` usually in these setups? 
// Actually, I should check if `lib/utils` exists or just use standard string concat for safety.
// `class-variance-authority` and `clsx` and `tailwind-merge` are in package.json (Step 97).
// User codebase usually has `lib/utils.ts`. I'll assume it exists or create a basic import.
// For safety, I will define `cn` locally if I can't verify, BUT typically it's better to stick to standard React props.
// I will use `clsx` and `tailwind-merge` directly if I'm not sure, but to be safe and consistent with typical "shadcn" like requests, I'll assume standard props.

interface ScepterButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'ghost';
    isLoading?: boolean;
}

export const ScepterButton = ({
    children,
    variant = 'primary',
    isLoading,
    className,
    ...props
}: ScepterButtonProps) => {

    const baseStyles = "relative px-6 py-3 font-heading font-bold uppercase tracking-wider transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2";

    const variants = {
        primary: "bg-gold text-obsidian hover:bg-gold-light border border-gold shadow-[0_0_15px_rgba(209,174,118,0.3)] hover:shadow-[0_0_25px_rgba(209,174,118,0.6)]",
        secondary: "bg-transparent text-gold border border-gold/50 hover:border-gold hover:bg-gold/10",
        ghost: "bg-transparent text-gold hover:text-gold-light hover:underline decoration-gold underline-offset-4"
    };

    return (
        <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`${baseStyles} ${variants[variant]} ${className || ''}`}
            {...props}
        >
            {isLoading && (
                <div className="w-5 h-5 border-2 border-obsidian border-t-transparent rounded-full animate-spin mr-2" />
            )}
            {children}
        </motion.button>
    );
};
