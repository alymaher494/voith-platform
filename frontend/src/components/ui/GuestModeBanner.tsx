import { Link } from "react-router-dom";
import { AlertCircle, UserPlus } from "lucide-react";

export const GuestModeBanner = () => {
    return (
        <div className="bg-gradient-to-r from-gold/10 via-gold/5 to-gold/10 border border-gold/30 rounded-xl p-4 mb-6">
            <div className="flex items-center justify-between gap-4 flex-wrap">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-gold/10 rounded-lg">
                        <AlertCircle className="w-5 h-5 text-gold" />
                    </div>
                    <div>
                        <p className="text-papyrus font-medium text-sm">
                            You are using <span className="text-gold font-bold">Guest Mode</span>
                        </p>
                        <p className="text-sand text-xs">
                            Limited features available. Sign up for full access.
                        </p>
                    </div>
                </div>
                <Link
                    to="/register"
                    className="flex items-center gap-2 px-4 py-2 bg-gold/10 hover:bg-gold/20 border border-gold/30 rounded-lg text-gold text-sm font-medium transition-all hover:shadow-[0_0_15px_rgba(209,174,118,0.2)]"
                >
                    <UserPlus className="w-4 h-4" />
                    <span>Sign Up Free</span>
                </Link>
            </div>
        </div>
    );
};
