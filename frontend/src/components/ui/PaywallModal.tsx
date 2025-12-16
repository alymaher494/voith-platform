import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { X, Lock, Sparkles, Zap, Shield, Clock } from "lucide-react";
import { ScepterButton } from "../pharaonic/ScepterButton";

interface PaywallModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const PaywallModal = ({ isOpen, onClose }: PaywallModalProps) => {
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
                        className="fixed inset-0 bg-obsidian/90 backdrop-blur-md z-50"
                    />

                    {/* Modal */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9, y: 30 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: 30 }}
                        transition={{ type: "spring", damping: 25, stiffness: 300 }}
                        className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-lg"
                    >
                        <div className="bg-gradient-to-b from-temple to-obsidian border border-gold/40 rounded-3xl shadow-[0_0_80px_rgba(209,174,118,0.2)] overflow-hidden">
                            {/* Decorative Top Bar */}
                            <div className="h-1 bg-gradient-to-r from-transparent via-gold to-transparent" />

                            {/* Close Button */}
                            <button
                                onClick={onClose}
                                className="absolute top-4 right-4 p-2 text-sand hover:text-gold transition-colors rounded-full hover:bg-gold/10 z-10"
                            >
                                <X className="w-5 h-5" />
                            </button>

                            {/* Header */}
                            <div className="relative px-8 pt-10 pb-6 text-center">
                                {/* Lock Icon with Glow */}
                                <motion.div
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    transition={{ delay: 0.2, type: "spring" }}
                                    className="relative inline-block mb-6"
                                >
                                    <div className="absolute inset-0 bg-gold/30 blur-2xl rounded-full" />
                                    <div className="relative w-20 h-20 rounded-2xl bg-gradient-to-br from-gold/20 to-gold/5 border border-gold/40 flex items-center justify-center">
                                        <Lock className="w-10 h-10 text-gold" />
                                    </div>
                                </motion.div>

                                <motion.h2
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.3 }}
                                    className="text-2xl md:text-3xl font-heading font-bold text-gold mb-3"
                                >
                                    Free Trial Limit Reached
                                </motion.h2>

                                <motion.p
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.4 }}
                                    className="text-sand text-base leading-relaxed max-w-sm mx-auto"
                                >
                                    You've used your free daily action. Unlock unlimited access, faster processing, and priority support by upgrading to Pro.
                                </motion.p>
                            </div>

                            {/* Benefits */}
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.5 }}
                                className="px-8 pb-6"
                            >
                                <div className="grid grid-cols-2 gap-3">
                                    <BenefitItem icon={Sparkles} text="Unlimited Operations" />
                                    <BenefitItem icon={Zap} text="Faster Processing" />
                                    <BenefitItem icon={Shield} text="Priority Support" />
                                    <BenefitItem icon={Clock} text="Longer Duration" />
                                </div>
                            </motion.div>

                            {/* Actions */}
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.6 }}
                                className="px-8 pb-8 space-y-4"
                            >
                                <Link to="/pricing" className="block">
                                    <ScepterButton className="w-full h-14 text-lg">
                                        <Sparkles className="w-5 h-5 mr-2" />
                                        Upgrade to Pro
                                    </ScepterButton>
                                </Link>

                                <div className="text-center">
                                    <Link
                                        to="/login"
                                        className="text-sm text-sand hover:text-gold transition-colors"
                                    >
                                        Already have an account? <span className="text-gold underline underline-offset-4">Login</span>
                                    </Link>
                                </div>
                            </motion.div>

                            {/* Bottom Glow */}
                            <div className="h-px bg-gradient-to-r from-transparent via-gold/30 to-transparent" />
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
};

const BenefitItem = ({ icon: Icon, text }: { icon: React.ComponentType<{ className?: string }>, text: string }) => (
    <div className="flex items-center gap-2 p-3 bg-obsidian/50 rounded-lg border border-gold/10">
        <Icon className="w-4 h-4 text-gold shrink-0" />
        <span className="text-xs text-papyrus">{text}</span>
    </div>
);
