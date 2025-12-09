import { Link } from "react-router-dom";
import logoFull from "../../assets/logo-full.png";
import { Github, Twitter, Linkedin } from "lucide-react";

export const Footer = () => {
    return (
        <footer className="border-t border-gold/10 bg-temple/30 pt-16 pb-8">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
                    {/* Brand */}
                    <div className="space-y-4">
                        <img src={logoFull} alt="VOITH" className="h-8 opacity-90" />
                        <p className="text-sand text-sm leading-relaxed">
                            The digital temple of media wisdom. Transmute, transcribe, and transform your content with the power of ancient knowledge and modern AI.
                        </p>
                        <div className="flex gap-4">
                            <SocialIcon icon={<Github className="w-5 h-5" />} />
                            <SocialIcon icon={<Twitter className="w-5 h-5" />} />
                            <SocialIcon icon={<Linkedin className="w-5 h-5" />} />
                        </div>
                    </div>

                    {/* Links Columns */}
                    <FooterColumn title="Product">
                        <FooterLink to="/dashboard">Dashboard</FooterLink>
                        <FooterLink to="/dashboard/downloader">Downloader</FooterLink>
                        <FooterLink to="/dashboard/converter">Converter</FooterLink>
                        <FooterLink to="/dashboard/transcriber">Transcriber</FooterLink>
                    </FooterColumn>

                    <FooterColumn title="Resources">
                        <FooterLink to="/dashboard/files">File Browser</FooterLink>
                        <FooterLink to="/dashboard/settings">Settings</FooterLink>
                        <FooterLink to="/">Documentation</FooterLink>
                    </FooterColumn>

                    <FooterColumn title="Account">
                        <FooterLink to="/login">Login</FooterLink>
                        <FooterLink to="/register">Register</FooterLink>
                        <FooterLink to="/">Help Center</FooterLink>
                    </FooterColumn>
                </div>

                {/* Bottom Bar */}
                <div className="pt-8 border-t border-gold/5 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-sand/60">
                    <p>© 2025 VOITH. All rights reserved.</p>
                    <div className="flex gap-6">
                        <Link to="/" className="hover:text-gold transition-colors">Privacy Policy</Link>
                        <Link to="/" className="hover:text-gold transition-colors">Terms of Service</Link>
                    </div>
                </div>
            </div>
        </footer>
    );
};

const FooterColumn = ({ title, children }: { title: string; children: React.ReactNode }) => (
    <div className="space-y-4">
        <h4 className="font-heading font-bold text-papyrus">{title}</h4>
        <ul className="space-y-2">{children}</ul>
    </div>
);

const FooterLink = ({ to, children }: { to: string; children: React.ReactNode }) => (
    <li>
        <Link to={to} className="text-sm text-sand hover:text-gold transition-colors block w-fit">
            {children}
        </Link>
    </li>
);

const SocialIcon = ({ icon }: { icon: React.ReactNode }) => (
    <a href="#" className="p-2 rounded-full bg-obsidian border border-gold/20 text-gold hover:bg-gold hover:text-obsidian transition-all">
        {icon}
    </a>
);
