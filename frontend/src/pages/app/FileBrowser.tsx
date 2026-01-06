import { useState, useEffect } from "react";
import { FileVideo, FileAudio, FileText, Trash2, Download, Search, HardDrive, Scroll } from "lucide-react";

// Pharaonic Components
import { CartoucheCard } from "../../components/pharaonic/CartoucheCard";
import { supabase } from "../../lib/supabase";

// Types
interface StoredFile {
    id: string;
    filename: string;
    size_bytes: number;
    created_at: string;
    storage_path: string;
}

interface UsageMetrics {
    storage_used_bytes: number;
    // other fields if needed
}

export const FileBrowser = () => {
    const [searchQuery, setSearchQuery] = useState("");
    const [files, setFiles] = useState<StoredFile[]>([]);
    const [loading, setLoading] = useState(true);
    const [metrics, setMetrics] = useState<UsageMetrics | null>(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const { data: { session } } = await supabase.auth.getSession();
            if (!session) return;

            // Fetch Files
            const { data: fileData, error: fileError } = await supabase
                .from('files')
                .select('*')
                .eq('user_id', session.user.id)
                .order('created_at', { ascending: false });

            if (fileError) throw fileError;
            setFiles(fileData || []);

            // Fetch Usage Metrics
            const { data: metricsData, error: metricsError } = await supabase
                .from('usage_metrics')
                .select('storage_used_bytes')
                .eq('user_id', session.user.id)
                .single();

            // It's possible metrics row doesn't exist yet if they haven't uploaded info
            if (!metricsError && metricsData) {
                setMetrics(metricsData);
            }

        } catch (error) {
            console.error("Error fetching archives:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id: string, storagePath: string) => {
        if (!confirm("Are you sure you want to banish this artifact to the void?")) return;

        try {
            // Delete from Storage
            await supabase.storage.from('processed_files').remove([storagePath]);

            // Delete from DB
            const { error } = await supabase.from('files').delete().eq('id', id);
            if (error) throw error;

            // Update local state
            setFiles(files.filter(f => f.id !== id));
            // Ideally update usage metrics too, but let's just re-fetch or decrement locally
            // Simple re-fetch for accuracy
            fetchData();
        } catch (error) {
            console.error("Error deleting file:", error);
        }
    };

    const handleDownload = async (filename: string) => {
        // Construct public URL or download path
        const { data } = supabase.storage.from('processed_files').getPublicUrl(filename);
        if (data) {
            window.open(data.publicUrl, '_blank');
        }
    };

    const formatBytes = (bytes: number) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    const getFileIcon = (filename: string) => {
        const ext = filename.split('.').pop()?.toLowerCase();
        if (['mp4', 'mkv', 'avi', 'mov'].includes(ext || '')) return <FileVideo className="w-10 h-10 text-gold drop-shadow-[0_0_8px_rgba(209,174,118,0.5)]" />;
        if (['mp3', 'wav', 'aac'].includes(ext || '')) return <FileAudio className="w-10 h-10 text-gold drop-shadow-[0_0_8px_rgba(209,174,118,0.5)]" />;
        return <FileText className="w-10 h-10 text-gold drop-shadow-[0_0_8px_rgba(209,174,118,0.5)]" />;
    };

    const filteredFiles = files.filter(file =>
        file.filename.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="space-y-10 min-h-[calc(100vh-100px)]">
            {/* Header Section */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
                <div>
                    <h1 className="text-4xl font-heading font-bold text-gold drop-shadow-md">The Archives of Thoth</h1>
                    <p className="text-sand mt-2">Browse and manage your preserved artifacts.</p>
                </div>

                {/* Stat Cards - Stone Tablets */}
                <div className="flex gap-4">
                    <div className="bg-obsidian border border-gold/30 p-4 rounded-lg shadow-[0_4px_20px_rgba(0,0,0,0.4)] min-w-[140px] text-center relative overflow-hidden group">
                        <div className="absolute inset-0 bg-gold/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                        <div className="flex justify-center mb-2 text-gold">
                            <HardDrive className="w-5 h-5" />
                        </div>
                        <p className="text-xs text-sand font-mono uppercase tracking-widest">Storage</p>
                        <p className="text-lg font-heading font-bold text-papyrus mt-1">
                            {formatBytes(metrics?.storage_used_bytes || 0)}
                        </p>
                    </div>
                    <div className="bg-obsidian border border-gold/30 p-4 rounded-lg shadow-[0_4px_20px_rgba(0,0,0,0.4)] min-w-[140px] text-center relative overflow-hidden group">
                        <div className="absolute inset-0 bg-gold/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                        <div className="flex justify-center mb-2 text-gold">
                            <Scroll className="w-5 h-5" />
                        </div>
                        <p className="text-xs text-sand font-mono uppercase tracking-widest">Rituals</p>
                        <p className="text-lg font-heading font-bold text-papyrus mt-1">
                            {files.length}
                        </p>
                    </div>
                </div>
            </div>

            {/* Search Bar */}
            <div className="relative max-w-xl">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <Search className="h-5 w-5 text-gold/50" />
                </div>
                <input
                    type="text"
                    placeholder="Search ancient records..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full h-12 pl-12 pr-4 bg-obsidian border border-gold/20 rounded-lg text-papyrus placeholder:text-papyrus/20 focus:border-gold focus:ring-1 focus:ring-gold focus:outline-none transition-all shadow-inner font-mono text-sm"
                />
            </div>

            {/* The Artifacts Grid */}
            {loading ? (
                <div className="text-center py-20">
                    <p className="text-gold animate-pulse font-heading tracking-widest">Consulting the Scrolls...</p>
                </div>
            ) : filteredFiles.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {filteredFiles.map((file) => (
                        <div key={file.id} className="relative group">
                            <CartoucheCard className="h-full hover:border-gold/50 transition-colors duration-300">
                                <div className="flex flex-col h-full space-y-4">
                                    <div className="flex items-start justify-between">
                                        <div className="p-3 bg-obsidian rounded-lg border border-gold/10 group-hover:border-gold/30 transition-colors">
                                            {getFileIcon(file.filename)}
                                        </div>
                                        {/* Actions (Visible on hover/mobile) */}
                                        <div className="flex gap-2">
                                            <button
                                                onClick={() => handleDownload(file.storage_path)}
                                                className="p-2 text-sand hover:text-gold hover:bg-gold/10 rounded-full transition-colors"
                                                title="Download Artifact"
                                            >
                                                <Download className="w-4 h-4" />
                                            </button>
                                            <button
                                                onClick={() => handleDelete(file.id, file.storage_path)}
                                                className="p-2 text-sand hover:text-red-400 hover:bg-red-500/10 rounded-full transition-colors"
                                                title="Destroy Artifact"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                        </div>
                                    </div>

                                    <div className="flex-1">
                                        <h3 className="font-heading font-bold text-papyrus text-lg truncate mb-1" title={file.filename}>
                                            {file.filename}
                                        </h3>
                                        <p className="text-xs text-sand font-mono opacity-70">
                                            Etched on {formatDate(file.created_at)}
                                        </p>
                                    </div>

                                    <div className="pt-4 border-t border-gold/10 flex justify-between items-center">
                                        <span className="text-xs font-bold text-gold uppercase tracking-wider">
                                            {formatBytes(file.size_bytes)}
                                        </span>
                                        <span className="text-[10px] text-sand/50 uppercase tracking-widest">
                                            SECURE
                                        </span>
                                    </div>
                                </div>
                            </CartoucheCard>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center py-20 border-2 border-dashed border-gold/10 rounded-xl bg-obsidian/20">
                    <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gold/5 flex items-center justify-center">
                        <Scroll className="w-10 h-10 text-gold/30" />
                    </div>
                    <h3 className="text-xl font-heading text-gold mb-2">The archives are empty.</h3>
                    <p className="text-sand max-w-sm mx-auto">
                        Begin a ritual to fill them with your digital artifacts.
                    </p>
                </div>
            )}
        </div>
    );
};
