import { useState } from "react";
import { Download, Video, Music, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

// Pharaonic Components
import { LivingBackground } from "../../components/layout/LivingBackground";
import { CartoucheCard } from "../../components/pharaonic/CartoucheCard";
import { ScepterButton } from "../../components/pharaonic/ScepterButton";

type JobStatus = "idle" | "processing" | "completed" | "error";

export const Downloader = () => {
    const [url, setUrl] = useState("");
    const [format, setFormat] = useState("video");
    const [quality, setQuality] = useState("best");
    const [status, setStatus] = useState<JobStatus>("idle");
    const [progress, setProgress] = useState(0);
    const [result, setResult] = useState<any>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!url) return;

        setStatus("processing");
        setProgress(0);

        try {
            // Start the download via API
            // @ts-ignore
            const { downloaderService } = await import("../../lib/api");
            const response = await downloaderService.download(url, format, quality, format === "audio");

            if (response.data.success) {
                const jobId = response.data.job_id;

                // Start polling
                const interval = setInterval(async () => {
                    try {
                        const statusRes = await downloaderService.getJobStatus(jobId);
                        const job = statusRes.data;

                        setProgress(job.progress);

                        if (job.status === 'completed') {
                            clearInterval(interval);
                            setStatus("completed");
                            setResult({
                                title: "Download Complete",
                                filename: job.filename,
                                size: "Ready",
                                duration: "Done",
                                downloadUrl: `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/downloads/${job.filename}`
                            });
                        } else if (job.status === 'error') {
                            clearInterval(interval);
                            setStatus("error");
                            console.error("Job failed:", job.message);
                        }
                    } catch (err) {
                        console.error("Polling error:", err);
                    }
                }, 1000);
            } else {
                setStatus("error");
            }
        } catch (error) {
            console.error("Download failed:", error);
            setStatus("error");
        }
    };

    return (
        <div className="relative min-h-[calc(100vh-100px)]">
            <div className="space-y-8 relative z-10 p-4">
                <div className="text-center space-y-2">
                    <h1 className="text-4xl font-heading font-bold text-gold drop-shadow-md">The Gatherer</h1>
                    <p className="text-sand max-w-2xl mx-auto">
                        Summon media from the digital ether and preserve it in the sacred vault.
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {/* Main Form */}
                    <div className="lg:col-span-2">
                        <CartoucheCard title="Extraction Ritual">
                            <form onSubmit={handleSubmit} className="space-y-8">
                                {/* URL Input */}
                                <div className="space-y-2">
                                    <label className="text-xs font-heading font-bold text-gold uppercase tracking-[0.2em] ml-1">Archive Location (URL)</label>
                                    <input
                                        type="url"
                                        placeholder="Paste the sacred link here..."
                                        value={url}
                                        onChange={(e) => setUrl(e.target.value)}
                                        disabled={status === "processing"}
                                        className="w-full h-14 px-6 bg-obsidian border border-gold/30 rounded-lg text-papyrus placeholder:text-papyrus/20 focus:border-gold focus:ring-1 focus:ring-gold focus:outline-none transition-all shadow-inner font-mono text-sm"
                                    />
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    {/* Format Selection - Styled as Toggles */}
                                    <div className="space-y-2">
                                        <label className="text-xs font-heading font-bold text-gold uppercase tracking-[0.2em] ml-1">Essence Type</label>
                                        <div className="grid grid-cols-2 gap-4">
                                            <button
                                                type="button"
                                                onClick={() => setFormat("video")}
                                                disabled={status === "processing"}
                                                className={`flex items-center justify-center gap-2 p-4 rounded-lg border transition-all ${format === "video"
                                                    ? "border-gold bg-gold/10 text-gold shadow-[0_0_10px_rgba(209,174,118,0.2)]"
                                                    : "border-gold/20 text-sand hover:border-gold/40 hover:bg-gold/5"
                                                    }`}
                                            >
                                                <Video className="w-5 h-5" />
                                                <span className="font-heading font-bold text-sm tracking-wide">Video</span>
                                            </button>
                                            <button
                                                type="button"
                                                onClick={() => setFormat("audio")}
                                                disabled={status === "processing"}
                                                className={`flex items-center justify-center gap-2 p-4 rounded-lg border transition-all ${format === "audio"
                                                    ? "border-gold bg-gold/10 text-gold shadow-[0_0_10px_rgba(209,174,118,0.2)]"
                                                    : "border-gold/20 text-sand hover:border-gold/40 hover:bg-gold/5"
                                                    }`}
                                            >
                                                <Music className="w-5 h-5" />
                                                <span className="font-heading font-bold text-sm tracking-wide">Audio</span>
                                            </button>
                                        </div>
                                    </div>

                                    {/* Quality Selection */}
                                    <div className="space-y-2">
                                        <label className="text-xs font-heading font-bold text-gold uppercase tracking-[0.2em] ml-1">Clarity Level</label>
                                        <select
                                            value={quality}
                                            onChange={(e) => setQuality(e.target.value)}
                                            disabled={status === "processing"}
                                            className="w-full h-14 px-4 bg-obsidian border border-gold/30 rounded-lg text-papyrus focus:border-gold focus:ring-1 focus:ring-gold focus:outline-none transition-colors appearance-none"
                                        >
                                            <option value="best">Highest (Original)</option>
                                            <option value="1080p">High Definition (1080p)</option>
                                            <option value="720p">Standard (720p)</option>
                                            <option value="480p">Low (480p)</option>
                                            <option value="360p">Minimal (360p)</option>
                                        </select>
                                    </div>
                                </div>

                                {/* Submit Button */}
                                <ScepterButton
                                    type="submit"
                                    className="w-full h-16 text-xl"
                                    disabled={!url || status === "processing"}
                                    isLoading={status === "processing"}
                                >
                                    {status === "processing" ? "Summoning..." : "Summon Media"}
                                </ScepterButton>
                            </form>
                        </CartoucheCard>
                    </div>

                    {/* Status Panel */}
                    <div className="lg:col-span-1">
                        <CartoucheCard title="Ritual Status" className="h-full">
                            <div className="space-y-8">
                                {/* Status Indicator */}
                                <div className="text-center pt-4">
                                    <div className={`text-xs mb-3 font-bold uppercase tracking-[0.2em] ${status === 'error' ? 'text-red-400' :
                                        status === 'completed' ? 'text-green-400' :
                                            status === 'processing' ? 'text-gold' : 'text-sand'
                                        }`}>
                                        {status === "idle" && "Awaiting Coordinates"}
                                        {status === "processing" && "Performing Extraction"}
                                        {status === "completed" && "Extraction Successful"}
                                        {status === "error" && "Ritual Failed"}
                                    </div>

                                    {status === "idle" && (
                                        <div className="p-6 bg-gold/5 rounded-full inline-block mb-4">
                                            <Download className="w-8 h-8 text-gold/50" />
                                        </div>
                                    )}
                                    {status === "processing" && (
                                        <div className="relative w-20 h-20 mx-auto">
                                            <div className="absolute inset-0 border-2 border-gold/30 rounded-full animate-[spin_3s_linear_infinite]" />
                                            <div className="absolute inset-2 border-2 border-t-gold border-r-transparent border-b-transparent border-l-transparent rounded-full animate-spin" />
                                            <Loader2 className="absolute inset-0 m-auto w-8 h-8 text-gold animate-pulse" />
                                        </div>
                                    )}
                                    {status === "completed" && (
                                        <div className="p-6 bg-green-500/10 rounded-full inline-block mb-4 border border-green-500/30">
                                            <CheckCircle className="w-8 h-8 text-green-400" />
                                        </div>
                                    )}
                                    {status === "error" && (
                                        <div className="p-6 bg-red-500/10 rounded-full inline-block mb-4 border border-red-500/30">
                                            <AlertCircle className="w-8 h-8 text-red-400" />
                                        </div>
                                    )}
                                </div>

                                {/* Progress Bar */}
                                {status === "processing" && (
                                    <div className="space-y-2">
                                        <div className="flex justify-between text-xs text-gold font-mono">
                                            <span>RIVER OF DATA</span>
                                            <span>{progress}%</span>
                                        </div>
                                        <div className="h-4 bg-obsidian rounded-full overflow-hidden border border-gold/20 relative">
                                            <div
                                                className="h-full bg-gold shadow-[0_0_15px_#d1ae76]"
                                                style={{ width: `${progress}%`, transition: 'width 0.3s ease-out' }}
                                            />
                                            {/* Water shimmer effect */}
                                            <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgdmlld0JveD0iMCAwIDIwIDIwIiBmaWxsPSJub25lIiBzdHJva2U9InJnYmEoMjU1LDI1NSwyNTUsMC4yKSIgc3Ryb2tlLXdpZHRoPSIxIj48cGF0aCBkPSJNMCAxMFE1IDUgMTAgMTBUMjAgMTAiIC8+PC9zdmc+')] opacity-30 animate-[slide_1s_linear_infinite]" />
                                        </div>
                                    </div>
                                )}

                                {/* Result Display */}
                                {status === "completed" && result && (
                                    <div className="space-y-4 p-6 bg-obsidian/50 rounded-xl border border-gold/20 shadow-lg">
                                        <h4 className="font-heading font-bold text-gold text-lg truncate border-b border-gold/10 pb-2">{result.title}</h4>
                                        <div className="space-y-3 text-sm text-sand font-mono">
                                            <div className="flex justify-between">
                                                <span className="opacity-50">ARTIFACT</span>
                                                <span className="text-papyrus text-right truncate pl-4">{result.filename}</span>
                                            </div>
                                            <div className="flex justify-between">
                                                <span className="opacity-50">SIZE</span>
                                                <span className="text-papyrus">{result.size}</span>
                                            </div>
                                            <div className="flex justify-between">
                                                <span className="opacity-50">LENGTH</span>
                                                <span className="text-papyrus">{result.duration}</span>
                                            </div>
                                        </div>
                                        <ScepterButton
                                            variant="secondary"
                                            className="w-full mt-4"
                                            onClick={() => window.open(result.downloadUrl, '_blank')}
                                        >
                                            <Download className="w-4 h-4 mr-2" />
                                            Retrieve from Vault
                                        </ScepterButton>
                                    </div>
                                )}

                                {/* Helper Text */}
                                {status === "idle" && (
                                    <div className="p-4 bg-gold/5 border border-gold/10 rounded-lg">
                                        <p className="text-xs text-sand/70 text-center leading-relaxed font-mono">
                                            COMPATIBLE SOURCES<br />
                                            YouTube • Vimeo • Twitter • TikTok
                                        </p>
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
