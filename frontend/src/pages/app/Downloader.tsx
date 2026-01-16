import { useState, useEffect } from "react";
import { Download, Video, Music, CheckCircle, AlertCircle, Loader2, Sparkles, FileText, Volume2, Eye, FileSearch, Clock, ExternalLink } from "lucide-react";

// Pharaonic Components
import { CartoucheCard } from "../../components/pharaonic/CartoucheCard";
import { ScepterButton } from "../../components/pharaonic/ScepterButton";

// Guest Mode Components
import { GuestModeBanner } from "../../components/ui/GuestModeBanner";
import { PaywallModal } from "../../components/ui/PaywallModal";

// Auth & Guest Tracking
import { useAuth } from "../../hooks/useAuth";
import { useGuestTracker } from "../../hooks/useGuestTracker";
import { downloaderService } from "../../lib/api";

type JobStatus = "idle" | "fetching_formats" | "processing" | "completed" | "error";

interface FormatOption {
    quality: string;
    resolution: string;
    filesize: number | null;
    fps: number;
    ext: string;
}

interface OriginalFile {
    url: string;
    expires_at: string;
    filename: string;
    size: number;
}

interface ProcessedFile {
    type: string;
    url: string;
    filename: string;
    size: number;
}

interface DownloadResult {
    original_file: OriginalFile;
    processed_files?: ProcessedFile[];
}

// Processing types configuration
const PROCESSING_TYPES = [
    { id: "transcribe", label: "Transcribe", icon: FileText, description: "Generate subtitle file (.srt)" },
    { id: "convert", label: "Convert", icon: Video, description: "Convert to different format" },
    { id: "extract_audio", label: "Extract Audio", icon: Volume2, description: "Extract MP3 audio" },
    { id: "ocr", label: "OCR", icon: Eye, description: "Text recognition from video" },
    { id: "summarize", label: "Summarize", icon: FileSearch, description: "Generate text summary" },
];

// Format file size to human readable
const formatFileSize = (bytes: number | null): string => {
    if (!bytes) return "Unknown size";
    const mb = bytes / (1024 * 1024);
    if (mb >= 1024) {
        return `${(mb / 1024).toFixed(1)} GB`;
    }
    return `${mb.toFixed(1)} MB`;
};

// Format expiry time
const formatExpiry = (expiresAt: string): string => {
    const expiry = new Date(expiresAt);
    return expiry.toLocaleString();
};

export const Downloader = () => {
    const { isAuthenticated } = useAuth();
    const { checkGuestLimit, incrementGuestUsage, getRemainingTrials } = useGuestTracker();

    // Form state
    const [url, setUrl] = useState("");
    const [format, setFormat] = useState("video");
    const [quality, setQuality] = useState("best");
    const [selectedProcessingTypes, setSelectedProcessingTypes] = useState<string[]>([]);

    // Format options from API
    const [availableFormats, setAvailableFormats] = useState<FormatOption[]>([]);
    const [platform, setPlatform] = useState<string>("");

    // Status state
    const [status, setStatus] = useState<JobStatus>("idle");
    const [progress, setProgress] = useState(0);
    const [progressMessage, setProgressMessage] = useState("");
    const [result, setResult] = useState<DownloadResult | null>(null);
    const [errorMessage, setErrorMessage] = useState("");

    // Paywall Modal State
    const [showPaywall, setShowPaywall] = useState(false);

    // Debounce timer for URL input
    const [urlDebounceTimer, setUrlDebounceTimer] = useState<NodeJS.Timeout | null>(null);

    // Fetch formats when URL changes
    useEffect(() => {
        if (urlDebounceTimer) {
            clearTimeout(urlDebounceTimer);
        }

        if (!url || url.length < 10) {
            setAvailableFormats([]);
            setPlatform("");
            return;
        }

        const timer = setTimeout(async () => {
            try {
                setStatus("fetching_formats");
                console.log("🔍 Fetching formats for URL:", url);
                const response = await downloaderService.getFormats(url);
                console.log("📦 Formats response:", response.data);

                if (response.data.formats && response.data.formats.length > 0) {
                    setAvailableFormats(response.data.formats);
                    setPlatform(response.data.platform || "Unknown");
                    // Auto-select first quality
                    setQuality(response.data.formats[0].quality);
                } else {
                    setAvailableFormats([]);
                }
                setStatus("idle");
            } catch (error) {
                console.error("Failed to fetch formats:", error);
                setAvailableFormats([]);
                setStatus("idle");
            }
        }, 800);

        setUrlDebounceTimer(timer);

        return () => clearTimeout(timer);
    }, [url]);

    // Toggle processing type selection
    const toggleProcessingType = (typeId: string) => {
        setSelectedProcessingTypes(prev =>
            prev.includes(typeId)
                ? prev.filter(t => t !== typeId)
                : [...prev, typeId]
        );
    };

    // Poll for job status
    const pollJobStatus = async (taskId: string) => {
        const interval = setInterval(async () => {
            try {
                console.log("📡 Polling job status for task:", taskId);
                const statusRes = await downloaderService.getJobStatus(taskId);
                const job = statusRes.data;
                console.log("✅ Status response:", job);

                setProgress(job.progress || 0);

                // Set progress message based on progress percentage
                if (job.progress < 30) {
                    setProgressMessage("Downloading from source...");
                } else if (job.progress < 90) {
                    setProgressMessage("Processing media...");
                } else {
                    setProgressMessage("Finalizing upload...");
                }

                if (job.status === 'completed') {
                    clearInterval(interval);
                    setStatus("completed");
                    setResult({
                        original_file: job.original_file,
                        processed_files: job.processed_files || []
                    });

                    // Increment usage for guests AFTER successful operation
                    if (!isAuthenticated) {
                        incrementGuestUsage();
                    }
                } else if (job.status === 'error') {
                    clearInterval(interval);
                    setStatus("error");
                    setErrorMessage(job.message || "Download failed");
                }
            } catch (err) {
                console.error("❌ Polling error:", err);
            }
        }, 1000);
    };

    // Quick Download handler
    const handleQuickDownload = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!url) return;

        // Check guest limit before processing
        if (!isAuthenticated && checkGuestLimit()) {
            setShowPaywall(true);
            return;
        }

        setStatus("processing");
        setProgress(0);
        setProgressMessage("Starting download...");
        setResult(null);
        setErrorMessage("");

        try {
            console.log("🚀 Starting quick download:", { url, quality });
            const response = await downloaderService.quickDownload(url, quality);

            if (response.data.task_id) {
                pollJobStatus(response.data.task_id);
            } else {
                setStatus("error");
                setErrorMessage("Failed to start download");
            }
        } catch (error: any) {
            console.error("Quick download failed:", error);
            setStatus("error");
            setErrorMessage(error.response?.data?.detail || "Download failed");
        }
    };

    // Process & Download handler
    const handleProcessDownload = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!url || selectedProcessingTypes.length === 0) return;

        // Check guest limit before processing
        if (!isAuthenticated && checkGuestLimit()) {
            setShowPaywall(true);
            return;
        }

        setStatus("processing");
        setProgress(0);
        setProgressMessage("Starting download and processing...");
        setResult(null);
        setErrorMessage("");

        try {
            console.log("🚀 Starting process download:", { url, quality, processing_types: selectedProcessingTypes });
            const response = await downloaderService.processDownload(url, quality, selectedProcessingTypes);

            if (response.data.task_id) {
                pollJobStatus(response.data.task_id);
            } else {
                setStatus("error");
                setErrorMessage("Failed to start processing");
            }
        } catch (error: any) {
            console.error("Process download failed:", error);
            setStatus("error");
            setErrorMessage(error.response?.data?.detail || "Processing failed");
        }
    };

    // Download file via signed URL
    const handleDownloadFile = (fileUrl: string, filename: string) => {
        const link = document.createElement('a');
        link.href = fileUrl;
        link.download = filename;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="relative min-h-[calc(100vh-100px)]">
            {/* Paywall Modal */}
            <PaywallModal
                isOpen={showPaywall}
                onClose={() => setShowPaywall(false)}
            />

            <div className="space-y-8 relative z-10 p-4">
                {/* Guest Mode Banner */}
                {!isAuthenticated && <GuestModeBanner />}

                {/* Remaining Trials Indicator for Guests */}
                {!isAuthenticated && getRemainingTrials() > 0 && (
                    <div className="text-center">
                        <span className="inline-flex items-center gap-2 px-4 py-2 bg-gold/10 border border-gold/30 rounded-full text-sm text-gold">
                            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                            {getRemainingTrials()} free trial remaining today
                        </span>
                    </div>
                )}

                <div className="text-center space-y-2">
                    <h1 className="text-4xl font-heading font-bold text-gold drop-shadow-md">The Gatherer</h1>
                    <p className="text-sand max-w-2xl mx-auto">
                        Summon media from the digital ether and preserve it in the sacred vault.
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {/* Main Form */}
                    <div className="lg:col-span-2 space-y-6">
                        <CartoucheCard title="Extraction Ritual">
                            <form className="space-y-8">
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
                                    {status === "fetching_formats" && (
                                        <div className="flex items-center gap-2 text-gold/70 text-sm">
                                            <Loader2 className="w-4 h-4 animate-spin" />
                                            <span>Analyzing source...</span>
                                        </div>
                                    )}
                                    {platform && (
                                        <div className="flex items-center gap-2 text-green-400 text-sm">
                                            <CheckCircle className="w-4 h-4" />
                                            <span>Detected: {platform}</span>
                                        </div>
                                    )}
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

                                    {/* Quality Selection - Dynamic from API */}
                                    <div className="space-y-2">
                                        <label className="text-xs font-heading font-bold text-gold uppercase tracking-[0.2em] ml-1">Clarity Level</label>
                                        <select
                                            value={quality}
                                            onChange={(e) => setQuality(e.target.value)}
                                            disabled={status === "processing"}
                                            className="w-full h-14 px-4 bg-obsidian border border-gold/30 rounded-lg text-papyrus focus:border-gold focus:ring-1 focus:ring-gold focus:outline-none transition-colors appearance-none"
                                        >
                                            {availableFormats.length > 0 ? (
                                                availableFormats.map((fmt) => (
                                                    <option key={fmt.quality} value={fmt.quality}>
                                                        {fmt.resolution || fmt.quality} {fmt.filesize ? `(${formatFileSize(fmt.filesize)})` : ''} {fmt.fps ? `${fmt.fps}fps` : ''}
                                                    </option>
                                                ))
                                            ) : (
                                                <>
                                                    <option value="best">Highest (Original)</option>
                                                    <option value="1080p">High Definition (1080p)</option>
                                                    <option value="720p">Standard (720p)</option>
                                                    <option value="480p">Low (480p)</option>
                                                    <option value="360p">Minimal (360p)</option>
                                                </>
                                            )}
                                        </select>
                                    </div>
                                </div>

                                {/* Download Buttons */}
                                <div className="flex flex-col sm:flex-row gap-4">
                                    <ScepterButton
                                        type="button"
                                        className="flex-1 h-14"
                                        disabled={!url || status === "processing"}
                                        isLoading={status === "processing"}
                                        onClick={handleQuickDownload}
                                    >
                                        <Download className="w-5 h-5 mr-2" />
                                        {status === "processing" ? "Summoning..." : "Quick Download"}
                                    </ScepterButton>
                                </div>
                            </form>
                        </CartoucheCard>

                        {/* Processing Options Card */}
                        <CartoucheCard title="Divine Processing">
                            <div className="space-y-4">
                                <p className="text-xs text-sand/70">
                                    Select additional processing to apply to your download
                                </p>
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                                    {PROCESSING_TYPES.map((type) => {
                                        const Icon = type.icon;
                                        const isSelected = selectedProcessingTypes.includes(type.id);
                                        return (
                                            <button
                                                key={type.id}
                                                type="button"
                                                onClick={() => toggleProcessingType(type.id)}
                                                disabled={status === "processing"}
                                                className={`flex items-start gap-3 p-4 rounded-lg border transition-all text-left ${isSelected
                                                    ? "border-gold bg-gold/10 shadow-[0_0_10px_rgba(209,174,118,0.15)]"
                                                    : "border-gold/20 hover:border-gold/40 hover:bg-gold/5"
                                                    }`}
                                            >
                                                <div className={`p-2 rounded-lg ${isSelected ? 'bg-gold/20' : 'bg-obsidian'}`}>
                                                    <Icon className={`w-4 h-4 ${isSelected ? 'text-gold' : 'text-sand'}`} />
                                                </div>
                                                <div className="flex-1 min-w-0">
                                                    <div className={`font-heading font-bold text-sm ${isSelected ? 'text-gold' : 'text-papyrus'}`}>
                                                        {type.label}
                                                    </div>
                                                    <div className="text-xs text-sand/70 truncate">
                                                        {type.description}
                                                    </div>
                                                </div>
                                                <div className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${isSelected
                                                    ? 'border-gold bg-gold'
                                                    : 'border-gold/30'
                                                    }`}>
                                                    {isSelected && <CheckCircle className="w-3 h-3 text-obsidian" />}
                                                </div>
                                            </button>
                                        );
                                    })}
                                </div>

                                {/* Process & Download Button */}
                                {selectedProcessingTypes.length > 0 && (
                                    <ScepterButton
                                        type="button"
                                        variant="secondary"
                                        className="w-full h-14 mt-4"
                                        disabled={!url || status === "processing"}
                                        isLoading={status === "processing"}
                                        onClick={handleProcessDownload}
                                    >
                                        <Sparkles className="w-5 h-5 mr-2" />
                                        Process & Download ({selectedProcessingTypes.length} selected)
                                    </ScepterButton>
                                )}
                            </div>
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
                                        {status === "fetching_formats" && "Analyzing Source"}
                                        {status === "processing" && "Performing Extraction"}
                                        {status === "completed" && "Extraction Successful"}
                                        {status === "error" && "Ritual Failed"}
                                    </div>

                                    {status === "idle" && (
                                        <div className="p-6 bg-gold/5 rounded-full inline-block mb-4">
                                            <Download className="w-8 h-8 text-gold/50" />
                                        </div>
                                    )}
                                    {status === "fetching_formats" && (
                                        <div className="p-6 bg-gold/5 rounded-full inline-block mb-4">
                                            <Loader2 className="w-8 h-8 text-gold animate-spin" />
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
                                            <span className="truncate pr-2">{progressMessage}</span>
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

                                {/* Error Display */}
                                {status === "error" && errorMessage && (
                                    <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
                                        <p className="text-sm text-red-400">{errorMessage}</p>
                                    </div>
                                )}

                                {/* Result Display */}
                                {status === "completed" && result && (
                                    <div className="space-y-4">
                                        {/* Original File */}
                                        <div className="p-4 bg-obsidian/50 rounded-xl border border-gold/20 shadow-lg space-y-3">
                                            <h4 className="font-heading font-bold text-gold text-sm flex items-center gap-2">
                                                <Video className="w-4 h-4" />
                                                Original File
                                            </h4>
                                            <div className="text-xs text-sand font-mono space-y-1">
                                                <div className="truncate">{result.original_file.filename}</div>
                                                <div className="text-sand/50">{formatFileSize(result.original_file.size)}</div>
                                            </div>
                                            <ScepterButton
                                                variant="secondary"
                                                className="w-full"
                                                onClick={() => handleDownloadFile(result.original_file.url, result.original_file.filename)}
                                            >
                                                <Download className="w-4 h-4 mr-2" />
                                                Download
                                            </ScepterButton>
                                            {/* Expiry Warning */}
                                            <div className="flex items-center gap-2 text-xs text-amber-400/80 bg-amber-500/10 px-3 py-2 rounded-lg">
                                                <Clock className="w-3 h-3 flex-shrink-0" />
                                                <span>Available until {formatExpiry(result.original_file.expires_at)}</span>
                                            </div>
                                        </div>

                                        {/* Processed Files */}
                                        {result.processed_files && result.processed_files.length > 0 && (
                                            <div className="space-y-3">
                                                <h4 className="font-heading font-bold text-gold text-sm flex items-center gap-2">
                                                    <Sparkles className="w-4 h-4" />
                                                    Processed Files
                                                </h4>
                                                {result.processed_files.map((file, index) => (
                                                    <div key={index} className="p-3 bg-obsidian/50 rounded-lg border border-gold/10 space-y-2">
                                                        <div className="flex items-center justify-between">
                                                            <span className="text-xs text-gold uppercase font-mono">{file.type}</span>
                                                            <span className="text-xs text-sand/50">{formatFileSize(file.size)}</span>
                                                        </div>
                                                        <div className="text-xs text-papyrus truncate">{file.filename}</div>
                                                        <button
                                                            onClick={() => handleDownloadFile(file.url, file.filename)}
                                                            className="flex items-center gap-1 text-xs text-gold hover:text-gold/80 transition-colors"
                                                        >
                                                            <ExternalLink className="w-3 h-3" />
                                                            Download
                                                        </button>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
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
