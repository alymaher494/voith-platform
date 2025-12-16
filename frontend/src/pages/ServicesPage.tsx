import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Mic, FileVideo, Download, ArrowRight, Sparkles } from "lucide-react";
import { ScepterButton } from "../components/pharaonic/ScepterButton";

const SERVICES = [
    {
        icon: "𓉐",
        lucideIcon: Download,
        title: "The Gatherer",
        subtitle: "Video Downloader",
        description: "Extract wisdom from any realm. Download high-fidelity streams from YouTube, Vimeo, Twitter, TikTok, and 800+ sources.",
        path: "/services/download",
        features: ["4K Support", "Audio Extract", "Batch Downloads"]
    },
    {
        icon: "𓆣",
        lucideIcon: FileVideo,
        title: "The Alchemist",
        subtitle: "File Converter",
        description: "Transmute media forms instantly. Convert and compress video & audio files without losing their essence.",
        path: "/services/convert",
        features: ["MP4, AVI, MKV", "Audio to MP3", "Compression"]
    },
    {
        icon: "𓏟",
        lucideIcon: Mic,
        title: "The Divine Scribe",
        subtitle: "Audio Transcriber",
        description: "Turn spoken words into eternal scrolls. AI-powered transcription with precise word-level timestamps.",
        path: "/services/transcribe",
        features: ["50+ Languages", "Timestamps", "Export Options"]
    },
];

export const ServicesPage = () => {
    return (
        <div className="relative min-h-screen">
            {/* Hero Section */}
            <section className="container mx-auto px-4 pt-12 pb-16 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="space-y-6"
                >
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-gold/10 border border-gold/30 rounded-full text-sm text-gold mb-4">
                        <Sparkles className="w-4 h-4" />
                        <span>Powered by Ancient Algorithms</span>
                    </div>

                    <h1 className="text-4xl md:text-6xl font-heading font-bold text-gold">
                        The Sacred Tools
                    </h1>
                    <p className="text-xl text-sand max-w-2xl mx-auto">
                        Powerful artifacts designed to handle your media with divine precision.
                        Choose your tool and begin your transformation.
                    </p>
                </motion.div>
            </section>

            {/* Services Grid */}
            <section className="container mx-auto px-4 pb-24">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
                    {SERVICES.map((service, index) => (
                        <motion.div
                            key={service.path}
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: index * 0.15 }}
                        >
                            <Link to={service.path} className="block h-full">
                                <div className="h-full bg-temple/50 backdrop-blur-sm border border-gold/10 rounded-2xl p-8 hover:border-gold/40 hover:shadow-[0_0_40px_rgba(209,174,118,0.1)] transition-all duration-300 group">
                                    {/* Icon */}
                                    <div className="mb-6 relative">
                                        <div className="w-20 h-20 rounded-2xl bg-obsidian border border-gold/20 flex items-center justify-center group-hover:border-gold/40 group-hover:shadow-[0_0_20px_rgba(209,174,118,0.2)] transition-all">
                                            <span
                                                className="text-5xl text-[#d1ae76]"
                                                style={{
                                                    textShadow: "1px 1px 0 #927952, 2px 2px 0 #927952, 3px 3px 5px rgba(0,0,0,0.3)",
                                                    filter: "drop-shadow(0 0 5px rgba(209, 174, 118, 0.3))"
                                                }}
                                            >
                                                {service.icon}
                                            </span>
                                        </div>
                                    </div>

                                    {/* Content */}
                                    <div className="space-y-4">
                                        <div>
                                            <p className="text-xs text-gold/70 uppercase tracking-widest mb-1">
                                                {service.subtitle}
                                            </p>
                                            <h3 className="text-2xl font-heading font-bold text-papyrus group-hover:text-gold transition-colors">
                                                {service.title}
                                            </h3>
                                        </div>

                                        <p className="text-sand text-sm leading-relaxed">
                                            {service.description}
                                        </p>

                                        {/* Features */}
                                        <div className="flex flex-wrap gap-2 pt-2">
                                            {service.features.map((feature) => (
                                                <span
                                                    key={feature}
                                                    className="px-3 py-1 text-xs bg-gold/10 border border-gold/20 rounded-full text-gold/80"
                                                >
                                                    {feature}
                                                </span>
                                            ))}
                                        </div>

                                        {/* CTA */}
                                        <div className="pt-4">
                                            <div className="flex items-center gap-2 text-gold font-medium group-hover:gap-3 transition-all">
                                                <span>Try Now</span>
                                                <ArrowRight className="w-4 h-4" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </Link>
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* Bottom CTA */}
            <section className="container mx-auto px-4 pb-24">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="bg-gradient-to-r from-temple to-obsidian border border-gold/20 rounded-3xl p-12 text-center max-w-4xl mx-auto"
                >
                    <h2 className="text-3xl font-heading font-bold text-gold mb-4">
                        Ready to Transform Your Media?
                    </h2>
                    <p className="text-sand mb-8 max-w-xl mx-auto">
                        Try any tool for free. No account required for your first transformation.
                    </p>
                    <Link to="/services/transcribe">
                        <ScepterButton className="px-8">
                            Start with Transcription
                            <ArrowRight className="w-4 h-4 ml-2" />
                        </ScepterButton>
                    </Link>
                </motion.div>
            </section>
        </div>
    );
};
