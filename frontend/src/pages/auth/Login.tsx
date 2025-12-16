import React, { useState } from 'react';
import { supabase } from '../../lib/supabase';
import { useNavigate, Link } from 'react-router-dom';
import { Mail, Lock, Loader2, AlertCircle } from 'lucide-react';

export const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const { data, error } = await supabase.auth.signInWithPassword({
                email,
                password,
            });

            if (error) throw error;

            if (data.session) {
                navigate('/services/download');
            }
        } catch (err: any) {
            setError(err.message || 'Failed to sign in');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-obsidian text-papyrus p-4">
            <div className="w-full max-w-md bg-temple p-8 rounded-lg border border-gold/20 shadow-2xl">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-heading text-gold mb-2">Welcome Back</h1>
                    <p className="text-papyrus/60">Sign in to access your vault</p>
                </div>

                {error && (
                    <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded mb-6 flex items-center">
                        <AlertCircle className="w-5 h-5 mr-2" />
                        {error}
                    </div>
                )}

                <form onSubmit={handleLogin} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium mb-2">Email</label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gold/50" />
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full bg-obsidian border border-gold/20 rounded pl-10 pr-4 py-2 focus:border-gold focus:ring-2 focus:ring-gold/50 focus:outline-none transition-colors"
                                placeholder="scribe@temple.com"
                                required
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium mb-2">Password</label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gold/50" />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full bg-obsidian border border-gold/20 rounded pl-10 pr-4 py-2 focus:border-gold focus:ring-2 focus:ring-gold/50 focus:outline-none transition-colors"
                                placeholder="••••••••"
                                required
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-gold hover:bg-gold-light text-obsidian font-bold py-3 rounded transition-colors flex items-center justify-center"
                    >
                        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Enter the Temple'}
                    </button>
                </form>

                <div className="mt-6 text-center text-sm text-papyrus/60">
                    Don't have an account?{' '}
                    <Link to="/register" className="text-gold hover:text-gold-light font-medium underline underline-offset-4 transition-colors">
                        Join the Order
                    </Link>
                </div>
            </div>
        </div>
    );
}
