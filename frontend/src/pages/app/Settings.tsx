import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import { User, Key, Bell, Shield } from "lucide-react";

export const Settings = () => {
    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-heading font-bold text-gold mb-2">Sanctum Configuration</h1>
                <p className="text-sand">Manage your account and preferences.</p>
            </div>

            {/* Profile Settings */}
            <Card className="bg-temple/40 backdrop-blur-md border-gold/10">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <User className="w-5 h-5 text-gold" />
                        Profile Information
                    </CardTitle>
                    <CardDescription>Update your personal details</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <Input placeholder="First Name" defaultValue="Initiate" />
                        <Input placeholder="Last Name" defaultValue="User" />
                    </div>
                    <Input placeholder="Email Address" type="email" defaultValue="initiate@voith.temple" />
                    <Button>Save Changes</Button>
                </CardContent>
            </Card>

            {/* Security */}
            <Card className="bg-temple/40 backdrop-blur-md border-gold/10">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Shield className="w-5 h-5 text-gold" />
                        Security
                    </CardTitle>
                    <CardDescription>Manage your password and authentication</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <Input placeholder="Current Password" type="password" />
                    <Input placeholder="New Password" type="password" />
                    <Input placeholder="Confirm New Password" type="password" />
                    <Button>Update Password</Button>
                </CardContent>
            </Card>

            {/* Notifications */}
            <Card className="bg-temple/40 backdrop-blur-md border-gold/10">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Bell className="w-5 h-5 text-gold" />
                        Notifications
                    </CardTitle>
                    <CardDescription>Configure your notification preferences</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <label className="flex items-center justify-between p-4 rounded-lg bg-obsidian/30 border border-gold/5 cursor-pointer hover:border-gold/20 transition-colors">
                        <span className="text-papyrus">Email notifications for completed jobs</span>
                        <input type="checkbox" defaultChecked className="w-5 h-5 rounded border-gold/20 bg-obsidian text-gold focus:ring-gold/50" />
                    </label>
                    <label className="flex items-center justify-between p-4 rounded-lg bg-obsidian/30 border border-gold/5 cursor-pointer hover:border-gold/20 transition-colors">
                        <span className="text-papyrus">Desktop notifications</span>
                        <input type="checkbox" className="w-5 h-5 rounded border-gold/20 bg-obsidian text-gold focus:ring-gold/50" />
                    </label>
                    <label className="flex items-center justify-between p-4 rounded-lg bg-obsidian/30 border border-gold/5 cursor-pointer hover:border-gold/20 transition-colors">
                        <span className="text-papyrus">Weekly summary reports</span>
                        <input type="checkbox" defaultChecked className="w-5 h-5 rounded border-gold/20 bg-obsidian text-gold focus:ring-gold/50" />
                    </label>
                </CardContent>
            </Card>

            {/* API Keys */}
            <Card className="bg-temple/40 backdrop-blur-md border-gold/10">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Key className="w-5 h-5 text-gold" />
                        API Access
                    </CardTitle>
                    <CardDescription>Manage your API keys for programmatic access</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="p-4 bg-obsidian/50 rounded-lg border border-gold/10 font-mono text-sm text-papyrus">
                        voith_sk_************************************
                    </div>
                    <Button variant="secondary">Generate New API Key</Button>
                </CardContent>
            </Card>
        </div>
    );
};
