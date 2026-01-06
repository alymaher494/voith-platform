import { useState } from "react";
import { Upload, CheckCircle, Loader2, Download, RefreshCcw } from "lucide-react";

// Pharaonic Components
import { CartoucheCard } from "../../components/pharaonic/CartoucheCard";
import { ScepterButton } from "../../components/pharaonic/ScepterButton";

// Guest Mode Components
import { GuestModeBanner } from "../../components/ui/GuestModeBanner";
import { PaywallModal } from "../../components/ui/PaywallModal";

// Auth & Guest Tracking
import { useAuth } from "../../hooks/useAuth";
import { useGuestTracker } from "../../hooks/useGuestTracker";
import { GUEST_MAX_SIZE, formatFileSize } from "../../config/limits";

type JobStatus = "idle" | "processing" | "completed" | "error";

export const Converter = () => {
    const { isAuthenticated } = useAuth();
    const { checkGuestLimit, incrementGuestUsage, getRemainingTrials } = useGuestTracker();

    const [file, setFile] = useState<File | null>(null);
    const [outputFormat, setOutputFormat] = useState("mp4");
    const [status, setStatus] = useState<JobStatus>("idle");
    const [result, setResult] = useState<any>(null);

    // Paywall Modal State
    const [showPaywall, setShowPaywall] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];

            // Check file size limit for guests
            if (!isAuthenticated && selectedFile.size > GUEST_MAX_SIZE) {
                setShowPaywall(true);
                return;
            }

            setFile(selectedFile);
            setResult(null);
            setStatus("idle");
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return;

        // Check guest limit before processing
        if (!isAuthenticated && checkGuestLimit()) {
            setShowPaywall(true);
            return;
        }

        setStatus("processing");
        setResult(null);

        try {
            const { converterService } = await import("../../lib/api");
            const response = await converterService.convert(file, outputFormat);

            if (response.data.success) {
                setStatus("completed");
                setResult(response.data);

                // Increment usage for guests AFTER successful operation
                if (!isAuthenticated) {
                    incrementGuestUsage();
                }
            } else {
                setStatus("error");
            }
        } catch (error) {
            console.error("Conversion failed:", error);
            setStatus("error");
        }
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
                    <h1 className="text-4xl font-heading font-bold text-gold drop-shadow-md">The Alchemist</h1>
                    <p className="text-sand max-w-2xl mx-auto">
                        Transmute the essence of media into new forms. Lead to Gold, MKV to MP4.
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    <div className="lg:col-span-2">
                        <CartoucheCard title="Transmutation Circle">
                            <form onSubmit={handleSubmit} className="space-y-8">
                                {/* File Upload Zone */}
                                <div className="group relative border-2 border-dashed border-gold/40 rounded-xl p-12 text-center hover:border-gold hover:bg-gold/5 transition-all duration-300 cursor-pointer">
                                    <input
                                        type="file"
                                        id="file-upload"
                                        className="hidden"
                                        onChange={handleFileChange}
                                        accept="video/*,audio/*"
                                        disabled={status === "processing"}
                                    />
                                    <label htmlFor="file-upload" className="cursor-pointer block w-full h-full relative z-10">
                                        <div className="mb-6 relative inline-block">
                                            {/* Spinning Alchemical Circle Effect */}
                                            <div className="absolute inset-0 bg-gold/20 blur-xl rounded-full scale-0 group-hover:scale-150 transition-transform duration-700" />
                                            <Upload className="w-20 h-20 text-gold relative z-10 drop-shadow-lg group-hover:-translate-y-2 transition-transform duration-300" />
                                        </div>
                                        <p className="text-2xl font-heading text-papyrus mb-2 tracking-wide group-hover:text-gold transition-colors">
                                            {file ? file.name : "Present the Material"}
                                        </p>
                                        <p className="text-sm text-sand font-mono uppercase tracking-widest opacity-70">
                                            MP4 • AVI • MKV • WAV
                                            {!isAuthenticated && (
                                                <span className="block mt-1 text-gold/70">Max {formatFileSize(GUEST_MAX_SIZE)} for guests</span>
                                            )}
                                        </p>
                                    </label>
                                </div>

                                {/* Target Format */}
                                <div className="space-y-4">
                                    <label className="text-xs font-heading font-bold text-gold uppercase tracking-[0.2em] ml-1">Example of the New Form</label>
                                    <div className="grid grid-cols-3 gap-4">
                                        {["mp4", "mp3", "avi", "mkv", "wav", "webm"].map((fmt) => (
                                            <button
                                                key={fmt}
                                                type="button"
                                                onClick={() => setOutputFormat(fmt)}
                                                disabled={status === "processing"}
                                                className={`p-4 rounded-lg border transition-all font-heading font-bold uppercase tracking-widest text-sm ${outputFormat === fmt
                                                    ? "border-gold bg-gold/10 text-gold shadow-[0_0_10px_rgba(209,174,118,0.2)]"
                                                    : "border-gold/20 text-sand hover:border-gold/40 hover:bg-gold/5"
                                                    }`}
                                            >
                                                {fmt}
                                            </button>
                                        ))}
                                    </div>
                                </div>

                                <ScepterButton
                                    type="submit"
                                    className="w-full h-16 text-xl"
                                    disabled={!file || status === "processing"}
                                    isLoading={status === "processing"}
                                >
                                    {status === "processing" ? "Transmuting..." : "Transmute"}
                                </ScepterButton>
                            </form>
                        </CartoucheCard>
                    </div>

                    {/* Status Panel */}
                    <div className="lg:col-span-1">
                        <CartoucheCard title="Alchemy Status" className="h-full">
                            <div className="flex flex-col h-full items-center justify-center space-y-8 min-h-[300px]">
                                <div className="text-center w-full">
                                    {status === "idle" && (
                                        <>
                                            <div className="w-24 h-24 mx-auto mb-6 rounded-full border-2 border-gold/10 flex items-center justify-center">
                                                <RefreshCcw className="w-10 h-10 text-gold/30" />
                                            </div>
                                            <p className="text-sand font-mono text-sm">The circle is dormant.</p>
                                        </>
                                    )}

                                    {status === "processing" && (
                                        <>
                                            <div className="relative w-32 h-32 mx-auto mb-6">
                                                <div className="absolute inset-0 border-4 border-gold/30 rounded-full animate-[spin_4s_linear_infinite]" />
                                                <div className="absolute inset-2 border-4 border-t-gold border-r-transparent border-b-transparent border-l-transparent rounded-full animate-[spin_2s_linear_infinite_reverse]" />
                                                <Loader2 className="absolute inset-0 m-auto w-10 h-10 text-gold animate-pulse" />
                                            </div>
                                            <p className="text-gold font-heading tracking-widest animate-pulse">Alchemy in Progress</p>
                                        </>
                                    )}

                                    {status === "completed" && (
                                        <>
                                            <div className="relative w-24 h-24 mx-auto mb-6">
                                                <div className="absolute inset-0 bg-green-500/20 rounded-full animate-ping" />
                                                <div className="relative z-10 w-full h-full bg-green-500/10 rounded-full border border-green-500/50 flex items-center justify-center">
                                                    <CheckCircle className="w-10 h-10 text-green-400" />
                                                </div>
                                            </div>
                                            <p className="text-green-400 font-heading tracking-widest mb-6">Transmutation Complete</p>
                                            <ScepterButton
                                                variant="secondary"
                                                className="w-full"
                                                onClick={() => {
                                                    const fileName = result?.output_file?.split('\\').pop()?.split('/').pop();
                                                    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                                                    window.open(`${apiUrl}/files/${fileName}`, '_blank');
                                                }}
                                            >
                                                <Download className="w-4 h-4 mr-2" />
                                                Collect Result
                                            </ScepterButton>
                                        </>
                                    )}

                                    {status === "error" && (
                                        <>
                                            <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-red-500/10 border border-red-500/30 flex items-center justify-center">
                                                <p className="text-3xl">⚠️</p>
                                            </div>
                                            <p className="text-red-400 font-mono">The alchemy backfired.</p>
                                        </>
                                    )}
                                </div>
                            </div>
                        </CartoucheCard>
                    </div>
                </div>
            </div>
        </div>
    );
};
