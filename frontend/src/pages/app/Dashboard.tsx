import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/Card";
import { Activity, HardDrive, Clock, Zap } from "lucide-react";
import { cn } from "../../lib/utils";

export const Dashboard = () => {
    return (
        <div className="space-y-8">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Active Rituals"
                    value="3"
                    icon={<Activity className="w-5 h-5 text-gold" />}
                    trend="+2 from yesterday"
                />
                <StatCard
                    title="Storage Used"
                    value="45.2 GB"
                    icon={<HardDrive className="w-5 h-5 text-gold" />}
                    trend="12% available"
                />
                <StatCard
                    title="Processing Time"
                    value="1.2s"
                    icon={<Zap className="w-5 h-5 text-gold" />}
                    trend="-0.3s improvement"
                />
                <StatCard
                    title="Total Transmutations"
                    value="1,284"
                    icon={<Clock className="w-5 h-5 text-gold" />}
                    trend="+124 this week"
                />
            </div>

            {/* Recent Activity & Queue */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <Card className="lg:col-span-2 bg-temple/40 backdrop-blur-md border-gold/10">
                    <CardHeader>
                        <CardTitle>Recent Transmutations</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {[1, 2, 3, 4, 5].map((i) => (
                                <div key={i} className="flex items-center justify-between p-4 rounded-lg bg-obsidian/50 border border-gold/5 hover:border-gold/20 transition-all">
                                    <div className="flex items-center gap-4">
                                        <div className="w-10 h-10 rounded bg-gold/10 flex items-center justify-center text-gold">
                                            <Activity className="w-5 h-5" />
                                        </div>
                                        <div>
                                            <h4 className="font-medium text-papyrus">Project_Alpha_v{i}.mp4</h4>
                                            <p className="text-xs text-sand">MP4 to MP3 • 2 mins ago</p>
                                        </div>
                                    </div>
                                    <span className="text-xs px-2 py-1 rounded bg-green-500/10 text-green-400 border border-green-500/20">
                                        Completed
                                    </span>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-temple/40 backdrop-blur-md border-gold/10">
                    <CardHeader>
                        <CardTitle>System Status</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-6">
                            <StatusItem label="Downloader Service" status="Operational" />
                            <StatusItem label="Converter Engine" status="Operational" />
                            <StatusItem label="Transcriber AI" status="Processing" />
                            <StatusItem label="Storage Vault" status="Operational" />
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

const StatCard = ({ title, value, icon, trend }: { title: string, value: string, icon: React.ReactNode, trend: string }) => (
    <Card className="bg-temple/40 backdrop-blur-md border-gold/10 hover:border-gold/30">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-sand">{title}</CardTitle>
            {icon}
        </CardHeader>
        <CardContent>
            <div className="text-2xl font-bold text-papyrus">{value}</div>
            <p className="text-xs text-gold/70 mt-1">{trend}</p>
        </CardContent>
    </Card>
);

const StatusItem = ({ label, status }: { label: string, status: string }) => (
    <div className="flex items-center justify-between">
        <span className="text-sm text-sand">{label}</span>
        <div className="flex items-center gap-2">
            <div className={cn("w-2 h-2 rounded-full", status === "Operational" ? "bg-green-500" : "bg-yellow-500 animate-pulse")} />
            <span className={cn("text-xs font-medium", status === "Operational" ? "text-green-400" : "text-yellow-400")}>
                {status}
            </span>
        </div>
    </div>
);
