import React, { useState } from 'react';
import { supabase } from '../../lib/supabase';
import { useNavigate, Link } from 'react-router-dom';
import { Mail, Lock, Loader2, AlertCircle, User } from 'lucide-react';
import logoFull from "../../assets/logo-full.png";

export const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const { data, error } = await supabase.auth.signUp({
                email,
                password,
                options: {
                    data: {
                        full_name: fullName,
                    },
                },
            });

            if (error) throw error;

            if (data.session) {
                navigate('/services/download');
            } else if (data.user) {
                // Check if email confirmation is required
                setError('Registration successful! Please check your email to verify your account.');
            }
        } catch (err: any) {
            setError(err.message || 'Failed to sign up');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="text-center space-y-2">
                <img src={logoFull} alt="VOITH" className="h-12 mx-auto mb-6" />
                <h1 className="text-2xl font-heading font-bold text-papyrus">Join the Order</h1>
                <p className="text-sand text-sm">Create your account to begin transmuting media.</p>
            </div>

            {error && (
                <div className={`p-3 rounded mb-6 flex items-center ${error.includes('successful') ? 'bg-green-500/10 border border-green-500/50 text-green-500' : 'bg-red-500/10 border border-red-500/50 text-red-500'}`}>
                    <AlertCircle className="w-5 h-5 mr-2" />
                    {error}
                </div>
            )}

            <form onSubmit={handleSignup} className="space-y-6">
                <div className="space-y-4">
                    <div className="relative">
                        <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gold/50" />
                        <input
                            type="text"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            className="w-full bg-obsidian border border-gold/20 rounded pl-10 pr-4 py-2 focus:border-gold focus:ring-2 focus:ring-gold/50 focus:outline-none transition-colors text-papyrus"
                            placeholder="Full Name"
                            required
                        />
                    </div>

                    <div className="relative">
                        <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gold/50" />
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full bg-obsidian border border-gold/20 rounded pl-10 pr-4 py-2 focus:border-gold focus:ring-2 focus:ring-gold/50 focus:outline-none transition-colors text-papyrus"
                            placeholder="Email Address"
                            required
                        />
                    </div>

                    <div className="relative">
                        <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gold/50" />
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full bg-obsidian border border-gold/20 rounded pl-10 pr-4 py-2 focus:border-gold focus:ring-2 focus:ring-gold/50 focus:outline-none transition-colors text-papyrus"
                            placeholder="Password"
                            required
                        />
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-gold hover:bg-gold-light text-obsidian font-bold py-3 rounded transition-colors flex items-center justify-center"
                >
                    {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Initiate Ritual'}
                </button>
            </form>

            <div className="text-center text-sm text-sand">
                Already an initiate?{" "}
                <Link to="/login" className="text-gold font-medium hover:underline">
                    Enter the Temple
                </Link>
            </div>
        </div>
    );
};
