import { Outlet } from "react-router-dom";
import { LivingBackground } from "../components/ui/LivingBackground";
import heroImage from "../assets/hero-thoth.png";

export const AuthLayout = () => {
    return (
        <div className="min-h-screen bg-obsidian text-papyrus font-body selection:bg-gold selection:text-obsidian relative flex overflow-hidden">
            <LivingBackground />

            {/* Left Side - Art */}
            <div className="hidden lg:flex lg:w-1/2 relative items-center justify-center p-12">
                <div className="relative z-10 text-center space-y-8">
                    <img
                        src={heroImage}
                        alt="Thoth"
                        className="w-full max-w-md mx-auto drop-shadow-[0_0_50px_rgba(209,174,118,0.2)] animate-float"
                    />
                    <h2 className="text-4xl font-heading font-bold text-gold">The Temple of Knowledge</h2>
                    <p className="text-sand text-lg max-w-md mx-auto">
                        Enter the sanctum where media is transmuted into wisdom.
                    </p>
                </div>
            </div>

            {/* Right Side - Form */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-4 sm:p-12 relative z-10 bg-obsidian/80 backdrop-blur-sm lg:bg-transparent lg:backdrop-blur-none">
                <div className="w-full max-w-md space-y-8 bg-temple/50 p-8 rounded-2xl border border-gold/10 shadow-2xl backdrop-blur-md">
                    <Outlet />
                </div>
            </div>
        </div>
    );
};
