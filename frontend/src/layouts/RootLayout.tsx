import { Outlet } from "react-router-dom";
import { LivingBackground } from "../components/ui/LivingBackground";
import { Header } from "../components/ui/Header";
import { Footer } from "../components/ui/Footer";

export const RootLayout = () => {
    return (
        <div className="min-h-screen bg-obsidian text-papyrus font-body selection:bg-gold selection:text-obsidian relative flex flex-col">
            <LivingBackground />
            <Header />
            <main className="relative z-10 flex-grow pt-16">
                <Outlet />
            </main>
            <div className="relative z-10">
                <Footer />
            </div>
        </div>
    );
};
