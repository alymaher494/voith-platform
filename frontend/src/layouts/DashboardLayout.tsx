import { useState, useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { Sidebar } from "../components/ui/Sidebar";
import { LivingBackground } from "../components/layout/LivingBackground";
import { supabase } from "../lib/supabase";
import { Loader2 } from "lucide-react";

export const DashboardLayout = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [session, setSession] = useState<any>(null);

    useEffect(() => {
        // Check active session
        supabase.auth.getSession().then(({ data: { session } }) => {
            setSession(session);
            if (!session) {
                navigate("/"); // Redirect to landing/login
            }
            setLoading(false);
        });

        // Listen for auth changes
        const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
            setSession(session);
            if (!session) {
                navigate("/");
            }
        });

        return () => subscription.unsubscribe();
    }, [navigate]);

    if (loading) {
        return (
            <div className="min-h-screen bg-obsidian flex items-center justify-center relative overflow-hidden">
                <LivingBackground />
                <div className="relative z-10 flex flex-col items-center">
                    <div className="relative w-24 h-24 mb-6">
                        <div className="absolute inset-0 border-4 border-gold/30 rounded-full animate-[spin_3s_linear_infinite]" />
                        <div className="absolute inset-2 border-4 border-t-gold border-r-transparent border-b-transparent border-l-transparent rounded-full animate-spin" />
                        <Loader2 className="absolute inset-0 m-auto w-8 h-8 text-gold animate-pulse" />
                    </div>
                    <p className="text-gold font-heading tracking-[0.3em] text-lg animate-pulse">ENTERING SANCTUM</p>
                </div>
            </div>
        );
    }

    // Only render dashboard if session exists (although navigate handles redirect, this prevents flash)
    if (!session) return null;

    const userEmail = session.user.email;
    const userInitial = userEmail ? userEmail[0].toUpperCase() : "A";

    return (
        <div className="min-h-screen bg-obsidian text-papyrus font-body selection:bg-gold selection:text-obsidian relative flex overflow-hidden">
            <LivingBackground />

            <Sidebar />

            <main className="flex-1 ml-64 relative z-10 h-screen overflow-y-auto custom-scrollbar">
                <div className="max-w-7xl mx-auto p-8 lg:p-12 space-y-10">
                    {/* Header */}
                    <header className="flex items-center justify-between border-b border-gold/10 pb-6">
                        <div>
                            <h1 className="text-3xl font-heading font-bold text-gold tracking-wide drop-shadow-sm">Sanctum Overview</h1>
                            <p className="text-sand text-sm mt-1">Managed by Thoth's Algorithm</p>
                        </div>

                        <div className="flex items-center gap-6">
                            {/* User Avatar Cartouche */}
                            <div className="flex items-center gap-3 pl-6 border-l border-gold/10">
                                <div className="text-right hidden sm:block">
                                    <p className="text-sm font-bold text-gold truncate max-w-[150px]">{userEmail}</p>
                                    <p className="text-xs text-sand uppercase tracking-wider">Initiate</p>
                                </div>
                                <div className="w-12 h-12 rounded-full border-2 border-gold/40 bg-obsidian p-1 cursor-pointer hover:border-gold transition-colors shadow-[0_0_15px_rgba(209,174,118,0.2)]">
                                    <div className="w-full h-full rounded-full bg-gold/10 flex items-center justify-center text-gold font-bold font-heading">
                                        {userInitial}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </header>

                    {/* Content Area */}
                    <div className="relative fade-in-up">
                        <Outlet />
                    </div>
                </div>
            </main>
        </div>
    );
};
