import { motion } from 'framer-motion';

export const LivingBackground = () => {
    return (
        <div className="fixed inset-0 z-[-1] overflow-hidden pointer-events-none bg-obsidian">
            {/* Abstract Sun Disk */}
            <motion.div
                animate={{
                    rotate: 360,
                    scale: [1, 1.1, 1]
                }}
                transition={{
                    rotate: { duration: 120, repeat: Infinity, ease: "linear" },
                    scale: { duration: 20, repeat: Infinity, ease: "easeInOut" }
                }}
                className="absolute -top-[10%] -right-[10%] w-[50vw] h-[50vw] rounded-full border border-gold/5 opacity-20 blur-3xl"
            />

            {/* Floating Hieroglyph-like shapes/Geometrics */}
            <motion.div
                animate={{ y: [0, -20, 0], opacity: [0.3, 0.5, 0.3] }}
                transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
                className="absolute top-1/4 left-10 w-24 h-24 border border-gold/10 rotate-45"
            />

            <motion.div
                animate={{ y: [0, 30, 0], rotate: [0, 10, 0] }}
                transition={{ duration: 12, repeat: Infinity, ease: "easeInOut", delay: 1 }}
                className="absolute bottom-1/3 right-20 w-32 h-32 border-2 border-gold/5 rounded-full"
            />

            {/* Grid Pattern Overlay */}
            <div className="absolute inset-0 opacity-[0.03]"
                style={{
                    backgroundImage: 'radial-gradient(#d1ae76 1px, transparent 1px)',
                    backgroundSize: '40px 40px'
                }}
            />

            {/* Vignette */}
            <div className="absolute inset-0 bg-radial-vignette pointer-events-none"
                style={{ background: 'radial-gradient(circle at center, transparent 0%, #192325 100%)' }}
            />
        </div>
    );
};
