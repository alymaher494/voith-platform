import { Link } from "react-router-dom";
import { Button } from "./Button";
import logoIcon from "../../assets/logo-icon.png";

export const Header = () => {
    return (
        <header className="fixed top-0 left-0 right-0 z-50 border-b border-gold/10 bg-obsidian/80 backdrop-blur-md">
            <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                {/* Logo */}
                <Link to="/" className="flex items-center gap-3 group">
                    <img
                        src={logoIcon}
                        alt="VOITH Logo"
                        className="w-10 h-10 group-hover:drop-shadow-[0_0_8px_rgba(209,174,118,0.5)] transition-all"
                    />
                    <span className="font-heading font-bold text-xl tracking-widest text-gold">VOITH</span>
                </Link>

                {/* Navigation */}
                <nav className="hidden md:flex items-center gap-8">
                    <NavLink to="/">Home</NavLink>
                    <NavLink to="/features">Features</NavLink>
                    <NavLink to="/pricing">Pricing</NavLink>
                    <NavLink to="/blog">Blog</NavLink>
                    <NavLink to="/contact">Contact</NavLink>
                </nav>

                {/* Actions */}
                <div className="flex items-center gap-4">
                    <Link to="/login">
                        <Button variant="ghost" size="sm">Login</Button>
                    </Link>
                    <Link to="/register">
                        <Button size="sm" className="hidden sm:flex">Get Started</Button>
                    </Link>
                </div>
            </div>
        </header>
    );
};

const NavLink = ({ to, children }: { to: string; children: React.ReactNode }) => (
    <Link
        to={to}
        className="text-sm font-medium text-sand hover:text-gold transition-colors relative group"
    >
        {children}
        <span className="absolute -bottom-1 left-0 w-0 h-[1px] bg-gold transition-all group-hover:w-full" />
    </Link>
);
