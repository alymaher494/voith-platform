import { useState } from "react";
import { Mic, Download, Languages, FileAudio, Copy, Check } from "lucide-react";

// Pharaonic Components
import { LivingBackground } from "../../components/layout/LivingBackground";
import { CartoucheCard } from "../../components/pharaonic/CartoucheCard";
import { ScepterButton } from "../../components/pharaonic/ScepterButton";

type JobStatus = "idle" | "processing" | "completed" | "error";

export const Transcriber = () => {
    const [file, setFile] = useState<File | null>(null);
    const [language, setLanguage] = useState("auto");
    const [model, setModel] = useState("medium");
    const [status, setStatus] = useState<JobStatus>("idle");
    const [progress, setProgress] = useState(0);
    const [transcript, setTranscript] = useState("");
    const [copied, setCopied] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleCopy = () => {
        if (!transcript) return;
        navigator.clipboard.writeText(transcript);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return;

        setStatus("processing");
        setProgress(0);

        try {
            // Updated to use the new simplified integration
            const { processMedia } = await import("../../lib/api");

            // Artificial progress for better UX
            const progressInterval = setInterval(() => {
                setProgress(prev => Math.min(prev + 5, 95));
            }, 600);

            const result = await processMedia(file, language);

            clearInterval(progressInterval);
            setProgress(100);

            if (result && result.text) {
                setStatus("completed");
                setTranscript(result.text);
            } else {
                setStatus("error");
            }
        } catch (error) {
            console.error("Transcription failed:", error);
            setStatus("error");
        }
    };

    return (
        <div className="relative min-h-[calc(100vh-100px)]">
            <div className="space-y-8 relative z-10 p-4">
                <div className="text-center space-y-2">
                    <h1 className="text-4xl font-heading font-bold text-gold drop-shadow-md">The Scribe's Chamber</h1>
                    <p className="text-sand max-w-2xl mx-auto">
                        Offer your voice to the archives of Thoth. The ancient algorithms shall etch your words into eternity.
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {/* Main Input Area */}
                    <div className="lg:col-span-2">
                        <CartoucheCard title="The Rosetta Stone">
                            <form onSubmit={handleSubmit} className="space-y-8">
                                {/* File Upload Zone */}
                                <div className="group relative border-2 border-dashed border-gold/40 rounded-xl p-12 text-center hover:border-gold hover:bg-gold/5 transition-all duration-300 cursor-pointer">
                                    <input
                                        type="file"
                                        id="audio-upload"
                                        className="hidden"
                                        onChange={handleFileChange}
                                        accept="audio/*,video/*"
                                        disabled={status === "processing"}
                                    />
                                    <label htmlFor="audio-upload" className="cursor-pointer block w-full h-full relative z-10">
                                        <div className="mb-6 relative inline-block">
                                            <div className="absolute inset-0 bg-gold/20 blur-2xl rounded-full scale-0 group-hover:scale-125 transition-transform duration-700" />
                                            <FileAudio className="w-20 h-20 text-gold relative z-10 drop-shadow-lg group-hover:scale-110 transition-transform duration-300" />
                                        </div>
                                        <p className="text-2xl font-heading text-papyrus mb-2 tracking-wide group-hover:text-gold transition-colors">
                                            {file ? file.name : "Place your Artifact Here"}
                                        </p>
                                        <p className="text-sm text-sand font-mono uppercase tracking-widest opacity-70">
                                            MP3 • WAV • MP4
                                        </p>
                                    </label>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    {/* Language Selection */}
                                    <div className="space-y-2">
                                        <label className="text-xs font-heading font-bold text-gold uppercase tracking-[0.2em] ml-1">Tongue</label>
                                        <select
                                            value={language}
                                            onChange={(e) => setLanguage(e.target.value)}
                                            disabled={status === "processing"}
                                            className="w-full h-14 px-4 bg-obsidian border border-gold/30 rounded-lg text-papyrus focus:border-gold focus:ring-1 focus:ring-gold focus:outline-none transition-colors appearance-none"
                                        >
                                            <option value="auto">Auto-detect (Magic)</option>
                                            <option value="en">English</option>
                                            <option value="ar">Arabic - العربية</option>
                                            <option value="fr">French</option>
                                            <option value="de">German</option>
                                            <option value="zh">Chinese</option>
                                        </select>
                                    </div>

                                    {/* Model Selection */}
                                    <div className="space-y-2">
                                        <label className="text-xs font-heading font-bold text-gold uppercase tracking-[0.2em] ml-1">Scribe Skill</label>
                                        <select
                                            value={model}
                                            onChange={(e) => setModel(e.target.value)}
                                            disabled={status === "processing"}
                                            className="w-full h-14 px-4 bg-obsidian border border-gold/30 rounded-lg text-papyrus focus:border-gold focus:ring-1 focus:ring-gold focus:outline-none transition-colors appearance-none"
                                        >
                                            <option value="tiny">Novice (Fastest)</option>
                                            <option value="base">Apprentice (Balanced)</option>
                                            <option value="small">Scribe (Good)</option>
                                            <option value="medium">High Priest (Better)</option>
                                            <option value="large">Pharaoh (Best)</option>
                                        </select>
                                    </div>
                                </div>

                                <ScepterButton
                                    type="submit"
                                    className="w-full h-16 text-xl"
                                    disabled={!file || status === "processing"}
                                    isLoading={status === "processing"}
                                >
                                    {status === "processing" ? "Transmuting..." : "Decipher Audio"}
                                </ScepterButton>
                            </form>
                        </CartoucheCard>
                    </div>

                    {/* Status Panel */}
                    <div className="lg:col-span-1">
                        <CartoucheCard title="Scroll of Truth" className="h-full flex flex-col">
                            <div className="flex flex-col h-full min-h-[500px]">
                                {/* Progress Display */}
                                <div className="mb-6 text-center">
                                    <div className={`text-xs mb-3 font-bold uppercase tracking-[0.2em] ${status === 'error' ? 'text-red-400' : 'text-gold'}`}>
                                        {status === 'idle' && "Awaiting Offering..."}
                                        {status === 'processing' && "The Scribes are Working..."}
                                        {status === 'completed' && "Inscription Complete"}
                                        {status === 'error' && "The Ritual Failed"}
                                    </div>

                                    {status === 'processing' && (
                                        <div className="w-full h-1 bg-obsidian rounded-full overflow-hidden border border-gold/20">
                                            <div
                                                className="h-full bg-gold shadow-[0_0_10px_#d1ae76] relative overflow-hidden"
                                                style={{ width: `${progress}%`, transition: 'width 0.5s ease-out' }}
                                            >
                                                <div className="absolute inset-0 bg-white/30 w-full animate-[shimmer_1s_infinite]" />
                                            </div>
                                        </div>
                                    )}
                                </div>

                                {/* Transcript Output - Papyrus Style */}
                                <div className="flex-grow bg-[#f2f4f7]/10 border border-gold/20 rounded-lg p-6 font-sans text-base text-papyrus leading-relaxed overflow-y-auto custom-scrollbar relative group">
                                    {transcript ? (
                                        <>
                                            <p className="whitespace-pre-wrap">{transcript}</p>
                                            <button
                                                onClick={handleCopy}
                                                className="absolute top-4 right-4 p-2 bg-obsidian/80 text-gold rounded-md opacity-0 group-hover:opacity-100 transition-opacity hover:bg-gold hover:text-obsidian"
                                                title="Copy to Clipboard"
                                            >
                                                {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                                            </button>
                                        </>
                                    ) : (
                                        <div className="h-full flex flex-col items-center justify-center opacity-30 select-none">
                                            <Languages className="w-16 h-16 mb-4" />
                                            <p className="text-center font-heading uppercase tracking-widest text-sm">The scroll is empty</p>
                                        </div>
                                    )}
                                </div>

                                {/* Actions */}
                                {status === 'completed' && transcript && (
                                    <div className="mt-6 pt-4 border-t border-gold/10">
                                        <ScepterButton variant="ghost" className="w-full text-sm">
                                            <Download className="w-4 h-4 mr-2" />
                                            Download Scroll
                                        </ScepterButton>
                                    </div>
                                )}
                            </div>
                        </CartoucheCard>
                    </div>
                </div>
            </div>
        </div>
    );
};
