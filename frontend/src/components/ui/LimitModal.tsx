import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { X, UserPlus, LogIn, AlertTriangle } from "lucide-react";
import { ScepterButton } from "../pharaonic/ScepterButton";

interface LimitModalProps {
    isOpen: boolean;
    onClose: () => void;
    limitType: "size" | "duration" | "daily";
    currentValue?: string;
    maxValue?: string;
}

const LIMIT_MESSAGES = {
    size: {
        title: "File Too Large",
        description: "Guest users can only process files up to",
        icon: "📁"
    },
    duration: {
        title: "Duration Exceeded",
        description: "Guest users can only transcribe audio up to",
        icon: "⏱️"
    },
    daily: {
        title: "Daily Limit Reached",
        description: "You've used all your free operations for today.",
        icon: "🔒"
    }
};

export const LimitModal = ({ isOpen, onClose, limitType, currentValue, maxValue }: LimitModalProps) => {
    const message = LIMIT_MESSAGES[limitType];

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="fixed inset-0 bg-obsidian/80 backdrop-blur-sm z-50"
                    />

                    {/* Modal */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: 20 }}
                        transition={{ type: "spring", damping: 25, stiffness: 300 }}
                        className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md"
                    >
                        <div className="bg-temple border border-gold/30 rounded-2xl shadow-[0_0_60px_rgba(209,174,118,0.15)] overflow-hidden">
                            {/* Header */}
                            <div className="relative bg-gradient-to-r from-gold/10 to-transparent p-6 border-b border-gold/20">
                                <button
                                    onClick={onClose}
                                    className="absolute top-4 right-4 p-2 text-sand hover:text-gold transition-colors rounded-lg hover:bg-gold/10"
                                >
                                    <X className="w-5 h-5" />
                                </button>

                                <div className="flex items-center gap-4">
                                    <div className="w-14 h-14 rounded-xl bg-gold/10 border border-gold/30 flex items-center justify-center text-2xl">
                                        {message.icon}
                                    </div>
                                    <div>
                                        <h2 className="text-xl font-heading font-bold text-gold">
                                            {message.title}
                                        </h2>
                                        <p className="text-sand text-sm mt-1">
                                            Upgrade for unlimited access
                                        </p>
                                    </div>
                                </div>
                            </div>

                            {/* Content */}
                            <div className="p-6 space-y-6">
                                <div className="flex items-start gap-3 p-4 bg-obsidian/50 rounded-xl border border-gold/10">
                                    <AlertTriangle className="w-5 h-5 text-gold shrink-0 mt-0.5" />
                                    <div className="space-y-1">
                                        <p className="text-papyrus text-sm">
                                            {message.description}
                                            {maxValue && (
                                                <span className="text-gold font-bold ml-1">{maxValue}</span>
                                            )}
                                        </p>
                                        {currentValue && (
                                            <p className="text-sand text-xs">
                                                Your file: <span className="text-red-400">{currentValue}</span>
                                            </p>
                                        )}
                                    </div>
                                </div>

                                <div className="text-center">
                                    <p className="text-sand text-sm mb-4">
                                        Sign up for <span className="text-gold font-bold">FREE</span> to unlock:
                                    </p>
                                    <ul className="text-left text-sm text-papyrus space-y-2 mb-6">
                                        <li className="flex items-center gap-2">
                                            <span className="text-gold">✓</span> Unlimited file size
                                        </li>
                                        <li className="flex items-center gap-2">
                                            <span className="text-gold">✓</span> Longer duration transcriptions
                                        </li>
                                        <li className="flex items-center gap-2">
                                            <span className="text-gold">✓</span> More daily operations
                                        </li>
                                        <li className="flex items-center gap-2">
                                            <span className="text-gold">✓</span> Access to The Archives (File Storage)
                                        </li>
                                    </ul>
                                </div>

                                {/* Action Buttons */}
                                <div className="flex flex-col gap-3">
                                    <Link to="/register" className="w-full">
                                        <ScepterButton className="w-full h-12">
                                            <UserPlus className="w-4 h-4 mr-2" />
                                            Sign Up Free
                                        </ScepterButton>
                                    </Link>
                                    <Link to="/login" className="w-full">
                                        <ScepterButton variant="ghost" className="w-full h-12">
                                            <LogIn className="w-4 h-4 mr-2" />
                                            I have an account
                                        </ScepterButton>
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
};
