import { Link, useLocation } from "react-router-dom";
import { cn } from "../../lib/utils";
import { LayoutDashboard, Download, FileVideo, Mic, FolderOpen, Settings, LogOut } from "lucide-react";
import logoIcon from "../../assets/logo-icon.png";

const NAV_ITEMS = [
    { icon: LayoutDashboard, label: "Sanctum", path: "/dashboard" },
    { icon: Download, label: "The Gatherer", path: "/dashboard/downloader" },
    { icon: FileVideo, label: "The Alchemist", path: "/dashboard/converter" },
    { icon: Mic, label: "The Scribe", path: "/dashboard/transcriber" },
    { icon: FolderOpen, label: "The Archives", path: "/dashboard/files" },
    { icon: Settings, label: "Temple Rites", path: "/dashboard/settings" },
];

export const Sidebar = () => {
    const location = useLocation();

    return (
        <aside className="w-64 bg-obsidian border-r border-gold/20 flex flex-col h-screen fixed left-0 top-0 z-30 shadow-[4px_0_24px_rgba(0,0,0,0.4)]">
            {/* Logo Area */}
            <div className="h-24 flex items-center px-8 border-b border-gold/10">
                <Link to="/dashboard" className="flex items-center gap-4 group">
                    <img
                        src={logoIcon}
                        alt="VOITH"
                        className="w-8 h-8 group-hover:drop-shadow-[0_0_8px_rgba(209,174,118,0.8)] transition-all duration-500"
                    />
                    <span className="font-heading font-bold text-2xl tracking-[0.2em] text-gold group-hover:text-gold-light transition-colors">VOITH</span>
                </Link>
            </div>

            {/* Navigation */}
            <nav className="flex-1 py-10 space-y-2">
                {NAV_ITEMS.map((item) => {
                    const isActive = location.pathname === item.path;
                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={cn(
                                "flex items-center gap-4 px-8 py-4 text-sm font-medium transition-all relative group",
                                isActive
                                    ? "text-gold bg-gold/5" // Active state
                                    : "text-papyrus/60 hover:text-gold hover:bg-gold/5" // Inactive state
                            )}
                        >
                            {/* Active Indicator (Vertical Bar) */}
                            {isActive && (
                                <div className="absolute left-0 top-0 bottom-0 w-[4px] bg-gold shadow-[0_0_10px_#d1ae76]" />
                            )}

                            <item.icon className={cn(
                                "w-5 h-5 transition-colors duration-300",
                                isActive ? "text-gold drop-shadow-md" : "text-papyrus/40 group-hover:text-gold"
                            )} />

                            <span className={cn(
                                "font-heading tracking-wide uppercase text-xs",
                                isActive ? "text-gold" : "group-hover:text-gold"
                            )}>
                                {item.label}
                            </span>
                        </Link>
                    );
                })}
            </nav>

            {/* User Profile / Logout */}
            <div className="p-6 border-t border-gold/10 bg-obsidian/50">
                <Link
                    to="/"
                    className="flex items-center gap-3 px-4 py-3 w-full rounded-lg text-sm font-medium text-sand hover:text-red-400 hover:bg-red-900/10 transition-colors group"
                >
                    <LogOut className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
                    <span className="uppercase tracking-widest text-xs">Leave Temple</span>
                </Link>
            </div>
        </aside>
    );
};
