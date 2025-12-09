import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../components/ui/Card";
import { Download, FileVideo, Languages, Zap, Shield, Globe, Clock, Database, Users, Code } from "lucide-react";

const FEATURES = [
    {
        icon: Download,
        title: "Universal Media Downloader",
        description: "Download from 800+ platforms including YouTube, Vimeo, TikTok, Instagram, and more with lightning speed.",
        details: ["Multi-platform support", "Batch downloads", "Auto quality selection"]
    },
    {
        icon: FileVideo,
        title: "Format Transmutation",
        description: "Convert between any video or audio format with zero quality loss. Support for MP4, AVI, MKV, MP3, WAV, and more.",
        details: ["50+ format support", "GPU acceleration", "Lossless conversion"]
    },
    {
        icon: Languages,
        title: "AI Speech Recognition",
        description: "Powered by OpenAI Whisper, transcribe speech to text in 50+ languages with industry-leading accuracy.",
        details: ["99% accuracy", "Multi-language", "Real-time processing"]
    },
    {
        icon: Zap,
        title: "Lightning Fast Processing",
        description: "Optimized infrastructure with GPU acceleration ensures your media is processed in seconds, not minutes.",
        details: ["GPU powered", "Sub-second response", "Parallel processing"]
    },
    {
        icon: Shield,
        title: "Enterprise-Grade Security",
        description: "Your files are encrypted at rest and in transit. Automatic deletion after 24 hours ensures privacy.",
        details: ["End-to-end encryption", "Auto-deletion", "GDPR compliant"]
    },
    {
        icon: Globe,
        title: "Global CDN",
        description: "Distributed servers across 6 continents ensure low latency and high availability wherever you are.",
        details: ["99.9% uptime", "Global reach", "Edge caching"]
    },
    {
        icon: Clock,
        title: "Queue Management",
        description: "Process multiple files simultaneously with intelligent queue management and priority handling.",
        details: ["Batch processing", "Priority queues", "Progress tracking"]
    },
    {
        icon: Database,
        title: "Cloud Storage",
        description: "Store your processed files in the cloud with generous storage limits on all plans.",
        details: ["Up to 100GB storage", "Version history", "Instant access"]
    },
    {
        icon: Users,
        title: "Team Collaboration",
        description: "Share files and collaborate with your team. Set permissions and track activity across your organization.",
        details: ["Role management", "Activity logs", "Shared workspaces"]
    },
    {
        icon: Code,
        title: "Developer API",
        description: "Integrate VOITH into your applications with our RESTful API. Full documentation and SDKs included.",
        details: ["REST API", "Webhooks", "SDK libraries"]
    }
];

export const Features = () => {
    return (
        <div className="relative min-h-screen flex flex-col pb-24">
            {/* Hero Section */}
            <section className="container mx-auto px-4 pt-20 pb-16 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="space-y-6"
                >
                    <h1 className="text-5xl md:text-6xl font-heading font-bold text-transparent bg-clip-text bg-gradient-to-r from-papyrus via-gold to-papyrus">
                        Ancient Power, Modern Tools
                    </h1>
                    <p className="text-xl text-sand max-w-3xl mx-auto">
                        Discover the sacred artifacts that make VOITH the most powerful media processing platform in the digital realm.
                    </p>
                </motion.div>
            </section>

            {/* Features Grid */}
            <section className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {FEATURES.map((feature, index) => (
                        <motion.div
                            key={feature.title}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                        >
                            <FeatureCard {...feature} />
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* Comparison Table */}
            <section className="container mx-auto px-4 mt-24">
                <div className="text-center mb-12">
                    <h2 className="text-3xl md:text-4xl font-heading font-bold text-gold mb-4">
                        How We Compare
                    </h2>
                    <p className="text-sand">VOITH vs Traditional Solutions</p>
                </div>

                <Card className="bg-temple/50 backdrop-blur-sm border-gold/10">
                    <CardContent className="p-0">
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="border-b border-gold/10">
                                    <tr>
                                        <th className="text-left p-6 text-papyrus font-heading">Feature</th>
                                        <th className="text-center p-6 text-gold font-heading">VOITH</th>
                                        <th className="text-center p-6 text-sand font-heading">Others</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <ComparisonRow feature="Platform Support" voith="800+" others="20-50" />
                                    <ComparisonRow feature="Processing Speed" voith="Sub-second" others="Minutes" />
                                    <ComparisonRow feature="File Size Limit" voith="Unlimited" others="100MB-2GB" />
                                    <ComparisonRow feature="Storage Included" voith="Up to 100GB" others="5-10GB" />
                                    <ComparisonRow feature="API Access" voith="✓ Full API" others="Limited" />
                                    <ComparisonRow feature="Batch Processing" voith="✓ Unlimited" others="5-10 files" />
                                    <ComparisonRow feature="AI Transcription" voith="✓ 50+ languages" others="10-20 languages" />
                                    <ComparisonRow feature="Uptime SLA" voith="99.9%" others="95-99%" />
                                </tbody>
                            </table>
                        </div>
                    </CardContent>
                </Card>
            </section>
        </div>
    );
};

const FeatureCard = ({ icon: Icon, title, description, details }: typeof FEATURES[0]) => (
    <Card className="bg-temple/50 backdrop-blur-sm border-gold/10 hover:border-gold/40 group h-full">
        <CardHeader>
            <div className="mb-4 p-3 bg-obsidian rounded-lg w-fit group-hover:shadow-[0_0_15px_rgba(209,174,118,0.3)] transition-all">
                <Icon className="w-8 h-8 text-gold" />
            </div>
            <CardTitle>{title}</CardTitle>
            <CardDescription className="text-base">{description}</CardDescription>
        </CardHeader>
        <CardContent>
            <ul className="space-y-2">
                {details.map((detail, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm text-sand">
                        <div className="w-1.5 h-1.5 rounded-full bg-gold" />
                        {detail}
                    </li>
                ))}
            </ul>
        </CardContent>
    </Card>
);

const ComparisonRow = ({ feature, voith, others }: { feature: string; voith: string; others: string }) => (
    <tr className="border-b border-gold/5 hover:bg-gold/5 transition-colors">
        <td className="p-6 text-papyrus">{feature}</td>
        <td className="p-6 text-center text-gold font-medium">{voith}</td>
        <td className="p-6 text-center text-sand/60">{others}</td>
    </tr>
);
