import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LandingLayout } from "./layouts/LandingLayout";
import { AuthLayout } from "./layouts/AuthLayout";
import { DashboardLayout } from "./layouts/DashboardLayout";
import { Home } from "./pages/Home";
import { Features } from "./pages/Features";
import { Pricing } from "./pages/Pricing";
import { Blog } from "./pages/Blog";
import { Contact } from "./pages/Contact";
import { Login } from "./pages/auth/Login";
import { Register } from "./pages/auth/Register";
import { Dashboard } from "./pages/app/Dashboard";
import { Downloader } from "./pages/app/Downloader";
import { Converter } from "./pages/app/Converter";
import { Transcriber } from "./pages/app/Transcriber";
import { FileBrowser } from "./pages/app/FileBrowser";
import { Settings } from "./pages/app/Settings";

function App() {
  return (
    <BrowserRouter>
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

        {/* App Routes */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="downloader" element={<Downloader />} />
          <Route path="converter" element={<Converter />} />
          <Route path="transcriber" element={<Transcriber />} />
          <Route path="files" element={<FileBrowser />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
