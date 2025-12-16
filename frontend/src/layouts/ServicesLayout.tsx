import { Outlet } from "react-router-dom";
import { LivingBackground } from "../components/ui/LivingBackground";
import { Header } from "../components/ui/Header";
import { Footer } from "../components/ui/Footer";

/**
 * Layout for public service pages accessible by guests and authenticated users.
 * Uses the public Header (with login/register) instead of the Dashboard Sidebar.
 */
export const ServicesLayout = () => {
    return (
        <div className="min-h-screen bg-obsidian text-papyrus font-body selection:bg-gold selection:text-obsidian relative flex flex-col">
            <LivingBackground />
            <Header />
            <main className="relative z-10 flex-grow pt-24 pb-12">
                <div className="container mx-auto px-4 max-w-6xl">
                    <Outlet />
                </div>
            </main>
            <div className="relative z-10">
                <Footer />
            </div>
        </div>
    );
};
