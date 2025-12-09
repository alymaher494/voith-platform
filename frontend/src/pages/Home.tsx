import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/Button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../components/ui/Card";
import { ArrowRight } from "lucide-react";
import heroImage from "../assets/hero-thoth.png";

export const Home = () => {
    return (
        <div className="relative min-h-screen flex flex-col">
            {/* Hero Section */}
            <section className="container mx-auto px-4 pt-20 pb-32 flex flex-col lg:flex-row items-center justify-between gap-12">
                <motion.div
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.8 }}
                    className="flex-1 space-y-8"
                >
                    <h1 className="text-5xl md:text-7xl font-heading font-bold leading-tight text-transparent bg-clip-text bg-gradient-to-r from-papyrus via-gold to-papyrus animate-pulse-gold">
                        Unlock the <br />
                        <span className="text-gold">Wisdom of Media</span>
                    </h1>
                    <p className="text-xl text-sand max-w-xl">
                        Transmute video, audio, and text with the power of Thoth.
                        A unified platform for downloading, converting, and analyzing content.
                    </p>
                    <div className="flex gap-4">
                        <Link to="/login">
                            <Button size="lg" className="text-lg px-8">
                                Enter the Temple <ArrowRight className="ml-2 w-5 h-5" />
                            </Button>
                        </Link>
                        <Link to="/register">
                            <Button variant="secondary" size="lg" className="text-lg px-8">
                                Get Started Free
                            </Button>
                        </Link>
                    </div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 1, delay: 0.2 }}
                    className="flex-1 relative"
                >
                    {/* Glowing backdrop */}
                    <div className="absolute inset-0 bg-gold/20 blur-[100px] rounded-full" />
                    <motion.img
                        src={heroImage}
                        alt="Thoth God of Wisdom"
                        className="relative z-10 w-full max-w-lg mx-auto drop-shadow-[0_0_30px_rgba(209,174,118,0.3)]"
                        animate={{ y: [-10, 10, -10] }}
                        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
                    />
                </motion.div>
            </section>

            {/* Stats Section */}
            <section className="border-y border-gold/10 bg-temple/30 py-12">
                <div className="container mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
                    <StatItem number="800+" label="Supported Sites" />
                    <StatItem number="1M+" label="Files Processed" />
                    <StatItem number="99.9%" label="Uptime" />
                    <StatItem number="50+" label="Languages" />
                </div>
            </section>

            {/* Features Grid */}
            <section className="container mx-auto px-4 py-24">
                <div className="text-center mb-16 space-y-4">
                    <h2 className="text-3xl md:text-4xl font-heading font-bold text-gold">The Sacred Tools</h2>
                    <p className="text-sand max-w-2xl mx-auto">Powerful artifacts designed to handle your media with divine precision.</p>
                </div>
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.8 }}
                    className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto"
                >
                    <FeatureCard
                        icon={
                            <span className="text-6xl text-[#d1ae76]" style={{
                                textShadow: "1px 1px 0 #927952, 2px 2px 0 #927952, 3px 3px 0 #927952, 4px 4px 0 #927952, 5px 5px 10px rgba(0,0,0,0.5)",
                                filter: "drop-shadow(0 0 5px rgba(209, 174, 118, 0.3))"
                            }}>𓉐</span>
                        }
                        title="The Gatherer"
                        description="Extract wisdom from any realm. Download high-fidelity streams from YouTube, Vimeo, and 800+ sources."
                    />
                    <FeatureCard
                        icon={
                            <span className="text-6xl text-[#d1ae76]" style={{
                                textShadow: "1px 1px 0 #927952, 2px 2px 0 #927952, 3px 3px 0 #927952, 4px 4px 0 #927952, 5px 5px 10px rgba(0,0,0,0.5)",
                                filter: "drop-shadow(0 0 5px rgba(209, 174, 118, 0.3))"
                            }}>𓆣</span>
                        }
                        title="The Alchemist"
                        description="Transmute media forms instantly. Convert and compress video & audio without losing their essence."
                    />
                    <FeatureCard
                        icon={
                            <span className="text-6xl text-[#d1ae76]" style={{
                                textShadow: "1px 1px 0 #927952, 2px 2px 0 #927952, 3px 3px 0 #927952, 4px 4px 0 #927952, 5px 5px 10px rgba(0,0,0,0.5)",
                                filter: "drop-shadow(0 0 5px rgba(209, 174, 118, 0.3))"
                            }}>𓏟</span>
                        }
                        title="The Divine Scribe"
                        description="Turn spoken words into eternal scrolls. AI-powered transcription with precise word-level timestamps."
                    />
                    <FeatureCard
                        icon={
                            <span className="text-6xl text-[#d1ae76]" style={{
                                textShadow: "1px 1px 0 #927952, 2px 2px 0 #927952, 3px 3px 0 #927952, 4px 4px 0 #927952, 5px 5px 10px rgba(0,0,0,0.5)",
                                filter: "drop-shadow(0 0 5px rgba(209, 174, 118, 0.3))"
                            }}>𓁹</span>
                        }
                        title="The Rosetta Stone"
                        description="Bridge the tongues of nations. Translate your transcripts into multiple languages for global enlightenment."
                    />
                </motion.div>
            </section>

            {/* CTA Section */}
            <section className="container mx-auto px-4 py-24">
                <div className="bg-gradient-to-r from-temple to-obsidian border border-gold/20 rounded-3xl p-12 text-center relative overflow-hidden">
                    <div className="absolute inset-0 bg-[url('/src/assets/logo-icon.png')] opacity-5 bg-center bg-no-repeat bg-contain" />
                    <div className="relative z-10 space-y-8">
                        <h2 className="text-4xl font-heading font-bold text-papyrus">Ready to Ascend?</h2>
                        <p className="text-xl text-sand max-w-2xl mx-auto">
                            Join thousands of creators and developers who have unlocked the true potential of their media.
                        </p>
                        <Link to="/register">
                            <Button size="lg" className="text-lg px-12 py-6 h-auto">
                                Start Your Journey Now
                            </Button>
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    );
};

const FeatureCard = ({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) => (
    <Card className="bg-temple/50 backdrop-blur-sm border-gold/10 hover:border-gold/40 group">
        <CardHeader>
            <div className="mb-4 p-3 bg-obsidian rounded-lg w-fit group-hover:shadow-[0_0_15px_rgba(209,174,118,0.3)] transition-all">
                {icon}
            </div>
            <CardTitle>{title}</CardTitle>
        </CardHeader>
        <CardContent>
            <CardDescription className="text-base">{description}</CardDescription>
        </CardContent>
    </Card>
);

const StatItem = ({ number, label }: { number: string, label: string }) => (
    <div className="space-y-2">
        <div className="text-4xl font-heading font-bold text-gold">{number}</div>
        <div className="text-sand text-sm uppercase tracking-widest">{label}</div>
    </div>
);
