import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Suspense, lazy } from "react";
import { DebugEnv } from "./components/DebugEnv";

// Lazy load layouts
const LandingLayout = lazy(() => import("./layouts/LandingLayout").then(m => ({ default: m.LandingLayout })));
const AuthLayout = lazy(() => import("./layouts/AuthLayout").then(m => ({ default: m.AuthLayout })));
const DashboardLayout = lazy(() => import("./layouts/DashboardLayout").then(m => ({ default: m.DashboardLayout })));
const ServicesLayout = lazy(() => import("./layouts/ServicesLayout").then(m => ({ default: m.ServicesLayout })));

// Lazy load pages
const Home = lazy(() => import("./pages/Home").then(m => ({ default: m.Home })));
const Features = lazy(() => import("./pages/Features").then(m => ({ default: m.Features })));
const Pricing = lazy(() => import("./pages/Pricing").then(m => ({ default: m.Pricing })));
const Blog = lazy(() => import("./pages/Blog").then(m => ({ default: m.Blog })));
const Contact = lazy(() => import("./pages/Contact").then(m => ({ default: m.Contact })));
const Login = lazy(() => import("./pages/auth/Login").then(m => ({ default: m.Login })));
const Register = lazy(() => import("./pages/auth/Register").then(m => ({ default: m.Register })));
const Dashboard = lazy(() => import("./pages/app/Dashboard").then(m => ({ default: m.Dashboard })));
const Downloader = lazy(() => import("./pages/app/Downloader").then(m => ({ default: m.Downloader })));
const Converter = lazy(() => import("./pages/app/Converter").then(m => ({ default: m.Converter })));
const Transcriber = lazy(() => import("./pages/app/Transcriber").then(m => ({ default: m.Transcriber })));
const FileBrowser = lazy(() => import("./pages/app/FileBrowser").then(m => ({ default: m.FileBrowser })));
const Settings = lazy(() => import("./pages/app/Settings").then(m => ({ default: m.Settings })));
const ServicesPage = lazy(() => import("./pages/ServicesPage").then(m => ({ default: m.ServicesPage })));

// Loading fallback
const LoadingFallback = () => (
  <div className="min-h-screen bg-obsidian flex items-center justify-center">
    <div className="text-gold font-heading animate-pulse tracking-widest">
      Loading...
    </div>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingFallback />}>
        <Routes>
          {/* Public Routes */}
          <Route element={<LandingLayout />}>
            <Route path="/" element={<Home />} />
            <Route path="/features" element={<Features />} />
            <Route path="/pricing" element={<Pricing />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/contact" element={<Contact />} />
          </Route>

          {/* Auth Routes */}
          <Route element={<AuthLayout />}>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Route>

          {/* Public Services (Guest + Authenticated Users) */}
          <Route element={<ServicesLayout />}>
            <Route path="/services" element={<ServicesPage />} />
            <Route path="/services/transcribe" element={<Transcriber />} />
            <Route path="/services/download" element={<Downloader />} />
            <Route path="/services/convert" element={<Converter />} />
          </Route>

          {/* Protected Dashboard Routes (Requires Authentication) */}
          <Route path="/dashboard" element={<DashboardLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="files" element={<FileBrowser />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
        <DebugEnv />
      </Suspense>
    </BrowserRouter>
  );
}

export default App;
