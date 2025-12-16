import { motion } from 'framer-motion';
import type { HTMLMotionProps } from 'framer-motion';

interface ScepterButtonProps extends Omit<HTMLMotionProps<"button">, 'onDrag' | 'onDragStart' | 'onDragEnd' | 'children'> {
    variant?: 'primary' | 'secondary' | 'ghost';
    isLoading?: boolean;
    children?: React.ReactNode;
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
