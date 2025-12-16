import { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "./Button";
import { ChevronDown, Mic, FileVideo, Download, Grid3X3, Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import logoIcon from "../../assets/logo-icon.png";

const SERVICES = [
    {
        icon: Mic,
        label: "Transcribe Audio/Video",
        path: "/services/transcribe",
        description: "AI-powered speech to text"
    },
    {
        icon: FileVideo,
        label: "File Converter",
        path: "/services/convert",
        description: "Convert & compress media"
    },
    {
        icon: Download,
        label: "Video Downloader",
        path: "/services/download",
        description: "Download from 800+ sites"
    },
];

export const Header = () => {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [servicesOpen, setServicesOpen] = useState(false);

    return (
        <>
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

                    {/* Desktop Navigation */}
                    <nav className="hidden md:flex items-center gap-8">
                        <NavLink to="/">Home</NavLink>

                        {/* Services Dropdown - Click/Hover */}
                        <div className="relative group">
                            <button
                                onClick={() => setServicesOpen(!servicesOpen)}
                                className="flex items-center gap-1 text-sm font-medium text-sand hover:text-gold transition-colors"
                            >
                                Services
                                <ChevronDown className={`w-4 h-4 transition-transform ${servicesOpen ? 'rotate-180' : ''} group-hover:rotate-180`} />
                            </button>

                            {/* Dropdown Menu - Shows on hover OR click */}
                            <div className={`absolute top-full left-1/2 -translate-x-1/2 pt-4 transition-all duration-200 ${servicesOpen ? 'opacity-100 visible' : 'opacity-0 invisible group-hover:opacity-100 group-hover:visible'}`}>
                                <div className="bg-obsidian/95 backdrop-blur-lg border border-gold/20 rounded-xl shadow-[0_8px_30px_rgba(0,0,0,0.4)] p-2 min-w-[280px]">
                                    {/* Arrow */}
                                    <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-obsidian/95 border-l border-t border-gold/20 rotate-45" />

                                    {SERVICES.map((service) => (
                                        <Link
                                            key={service.path}
                                            to={service.path}
                                            onClick={() => setServicesOpen(false)}
                                            className="flex items-center gap-3 p-3 rounded-lg hover:bg-gold/10 transition-colors group/item"
                                        >
                                            <div className="w-10 h-10 rounded-lg bg-gold/10 flex items-center justify-center group-hover/item:bg-gold/20 transition-colors">
                                                <service.icon className="w-5 h-5 text-gold" />
                                            </div>
                                            <div>
                                                <div className="text-sm font-medium text-papyrus group-hover/item:text-gold transition-colors">
                                                    {service.label}
                                                </div>
                                                <div className="text-xs text-sand/70">
                                                    {service.description}
                                                </div>
                                            </div>
                                        </Link>
                                    ))}

                                    {/* View All */}
                                    <div className="border-t border-gold/10 mt-2 pt-2">
                                        <Link
                                            to="/services"
                                            onClick={() => setServicesOpen(false)}
                                            className="flex items-center gap-3 p-3 rounded-lg hover:bg-gold/10 transition-colors group/item"
                                        >
                                            <div className="w-10 h-10 rounded-lg bg-gold/5 border border-gold/20 flex items-center justify-center group-hover/item:bg-gold/10 transition-colors">
                                                <Grid3X3 className="w-5 h-5 text-gold" />
                                            </div>
                                            <div>
                                                <div className="text-sm font-medium text-gold">
                                                    View All Services
                                                </div>
                                                <div className="text-xs text-sand/70">
                                                    Explore all tools
                                                </div>
                                            </div>
                                        </Link>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <NavLink to="/pricing">Pricing</NavLink>
                        <NavLink to="/blog">Blog</NavLink>
                        <NavLink to="/contact">Contact</NavLink>
                    </nav>

                    {/* Desktop Actions */}
                    <div className="hidden md:flex items-center gap-4">
                        <Link to="/login">
                            <Button variant="ghost" size="sm">Login</Button>
                        </Link>
                        <Link to="/register">
                            <Button size="sm">Get Started</Button>
                        </Link>
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="md:hidden p-2 text-gold hover:bg-gold/10 rounded-lg transition-colors"
                        aria-label="Toggle menu"
                    >
                        {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                    </button>
                </div>
            </header>

            {/* Mobile Menu Overlay */}
            <AnimatePresence>
                {mobileMenuOpen && (
                    <>
                        {/* Backdrop */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setMobileMenuOpen(false)}
                            className="fixed inset-0 bg-obsidian/80 backdrop-blur-sm z-40 md:hidden"
                        />

                        {/* Slide-out Menu */}
                        <motion.div
                            initial={{ x: "100%" }}
                            animate={{ x: 0 }}
                            exit={{ x: "100%" }}
                            transition={{ type: "spring", damping: 25, stiffness: 300 }}
                            className="fixed top-0 right-0 bottom-0 w-80 max-w-full bg-obsidian border-l border-gold/20 z-50 md:hidden overflow-y-auto"
                        >
                            {/* Mobile Menu Header */}
                            <div className="flex items-center justify-between p-4 border-b border-gold/10">
                                <span className="font-heading font-bold text-lg text-gold">Menu</span>
                                <button
                                    onClick={() => setMobileMenuOpen(false)}
                                    className="p-2 text-gold hover:bg-gold/10 rounded-lg transition-colors"
                                >
                                    <X className="w-5 h-5" />
                                </button>
                            </div>

                            {/* Mobile Nav Links */}
                            <nav className="p-4 space-y-2">
                                <MobileNavLink to="/" onClick={() => setMobileMenuOpen(false)}>
                                    Home
                                </MobileNavLink>

                                {/* Services Section */}
                                <div className="pt-4">
                                    <div className="text-xs text-gold uppercase tracking-widest mb-3 px-3">Services</div>
                                    {SERVICES.map((service) => (
                                        <Link
                                            key={service.path}
                                            to={service.path}
                                            onClick={() => setMobileMenuOpen(false)}
                                            className="flex items-center gap-3 p-3 rounded-lg hover:bg-gold/10 transition-colors"
                                        >
                                            <div className="w-10 h-10 rounded-lg bg-gold/10 flex items-center justify-center">
                                                <service.icon className="w-5 h-5 text-gold" />
                                            </div>
                                            <div>
                                                <div className="text-sm font-medium text-papyrus">{service.label}</div>
                                                <div className="text-xs text-sand/70">{service.description}</div>
                                            </div>
                                        </Link>
                                    ))}
                                    <Link
                                        to="/services"
                                        onClick={() => setMobileMenuOpen(false)}
                                        className="flex items-center gap-3 p-3 rounded-lg hover:bg-gold/10 transition-colors border border-gold/20 mt-2"
                                    >
                                        <Grid3X3 className="w-5 h-5 text-gold" />
                                        <span className="text-sm font-medium text-gold">View All Services</span>
                                    </Link>
                                </div>

                                {/* Other Links */}
                                <div className="pt-4 border-t border-gold/10">
                                    <MobileNavLink to="/pricing" onClick={() => setMobileMenuOpen(false)}>
                                        Pricing
                                    </MobileNavLink>
                                    <MobileNavLink to="/blog" onClick={() => setMobileMenuOpen(false)}>
                                        Blog
                                    </MobileNavLink>
                                    <MobileNavLink to="/contact" onClick={() => setMobileMenuOpen(false)}>
                                        Contact
                                    </MobileNavLink>
                                </div>
                            </nav>

                            {/* Mobile Auth Buttons */}
                            <div className="p-4 border-t border-gold/10 space-y-3">
                                <Link to="/login" onClick={() => setMobileMenuOpen(false)} className="block">
                                    <Button variant="secondary" className="w-full">Login</Button>
                                </Link>
                                <Link to="/register" onClick={() => setMobileMenuOpen(false)} className="block">
                                    <Button className="w-full">Get Started Free</Button>
                                </Link>
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </>
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

const MobileNavLink = ({ to, onClick, children }: { to: string; onClick: () => void; children: React.ReactNode }) => (
    <Link
        to={to}
        onClick={onClick}
        className="block px-3 py-3 text-base font-medium text-papyrus hover:text-gold hover:bg-gold/10 rounded-lg transition-colors"
    >
        {children}
    </Link>
);
