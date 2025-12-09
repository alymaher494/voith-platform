# 🏛️ VOITH UI Specification & Design System

**Version**: 2.0.0 (Final)
**Theme**: Ancient Egyptian Pharaonic + Modern Dark SaaS
**Framework**: React + Tailwind CSS + Framer Motion
**Assets**:
- Logo Icon: `src/assets/logo-icon.png` (Thoth Head)
- Full Logo: `src/assets/logo-full.png` (Thoth + VOITH text)
- Hero Image: `src/assets/hero-thoth.png` (Thoth with Tablet)

---

## 🎨 Global Design System

### 1. Color Palette "The Obsidian & Gold"
| Token | Hex | Usage |
|-------|-----|-------|
| `bg-obsidian` | `#192325` | Main background (Deep Green/Black) |
| `bg-temple` | `#1f2a30` | Card/Surface background |
| `border-gold` | `#d1ae76` | Borders, Icons, Active States (Matte Gold) |
| `text-papyrus` | `#f2f4f7` | Primary Text (Off-white) |
| `text-sand` | `#a8a29e` | Secondary Text (Muted) |
| `accent-glow` | `rgba(209, 174, 118, 0.15)` | Hover states, subtle glows |

### 2. Typography
- **Headings**: `Cinzel` (Weights: 400, 700) - Used for Page Titles, Section Headers.
- **Body**: `Inter` or `Outfit` (Weights: 300, 400, 500) - Used for UI text, data, forms.
- **Monospace**: `JetBrains Mono` - Used for Logs, API Keys, Code snippets.

### 3. The "Living Background" System
Every page features a subtle, animated background layer:
- **Elements**: Floating Ankhs, Eye of Horus outlines, geometric lines.
- **Motion**: Very slow parallax drift (10-20s duration), slight rotation for circular elements.
- **Opacity**: 3-5% (Must not interfere with content).
- **Implementation**: `Framer Motion` SVG layer with `z-index: 0`.

---

## 📱 Component Library (Core)

### `Button` (The Scepter)
- **Variants**:
  - `primary`: Solid Gold (`#d1ae76`) bg, Obsidian text. Hover: Brighten + Glow.
  - `secondary`: Transparent bg, Gold border. Hover: Gold bg (10% opacity).
  - `ghost`: Text only with animated gold underline on hover.
- **Props**: `variant`, `size`, `icon`, `isLoading`.

### `Card` (The Cartouche)
- **Style**: `bg-temple` (`#1f2a30`), `border-gold` (1px, 20% opacity).
- **Hover**: Border opacity increases to 60%, subtle box-shadow (`shadow-gold-sm`).
- **Shape**: Rounded-xl (16px).

### `Input` (The Scroll)
- **Style**: Transparent bg, bottom border only (Gold, 30% opacity).
- **Focus**: Bottom border becomes solid Gold (100%), Label floats up.
- **Icon**: Optional leading icon (e.g., Search, User) in Gold.

---

## 📄 Page Specifications

### 1. Public Pages

#### **Home Page (Landing)**
- **Layout Structure**:
  - **Hero Section**:
    - **Left**: H1 "Unlock the Wisdom of Media", Subtext "Transmute video, audio, and text with the power of Thoth.", CTA "Enter the Temple".
    - **Right**: `hero-thoth.png` (Thoth holding tablet) floating with subtle hover animation.
    - **Background**: Large, slow-rotating Sun Disk behind Thoth.
  - **Features Grid**: 3 Cards (Downloader, Converter, ASR). Icons: Animated SVG lines.
  - **Tech Stack**: "Powered by" section with logos (Python, FFmpeg, Whisper) styled in Gold monochrome.
- **User Interactions**:
  - Scroll-triggered fade-ins (`whileInView`).
  - Hero image follows mouse movement slightly (Parallax).
- **Theme Application**:
  - Gold glow behind the Hero image.
  - H1 in `Cinzel`.
- **API Requirements**: None (Static).

#### **About**
- **Layout Structure**:
  - **Mission**: Text block centered.
  - **Story**: "The Legend of Thoth" - connecting the myth to modern AI.
- **Theme Application**: Background features "Papyrus Scroll" texture overlay (very low opacity).

#### **Pricing**
- **Layout Structure**:
  - **Cards**: 3 Vertical Cards (Scribe, Priest, Pharaoh).
  - **Highlight**: "Pharaoh" plan has a permanent gold glow border and a "Best Value" scarab badge.
  - **Toggle**: Monthly/Yearly switch styled as an ancient scale.
- **User Interactions**: Hovering a card expands it slightly (`scale-105`).

#### **Blog (List + Article)**
- **Layout Structure**:
  - **List**: Grid of cards with image top, title, excerpt.
  - **Article**: Single column text, wide margins.
- **Theme Application**: Drop caps for the first letter of articles in `Cinzel` Gold.

#### **Contact**
- **Layout Structure**:
  - **Form**: Name, Email, Message (The Scroll inputs).
  - **Info**: Email address, Location (Cairo, Egypt).

---

### 2. Auth Pages

#### **Login / Register**
- **Layout Structure**:
  - **Split Screen**:
    - **Left**: Form (Card centered). Logo `logo-full.png` at top.
    - **Right**: `hero-thoth.png` or abstract geometric pattern (Hidden on Mobile).
- **Component Breakdown**:
  - `AuthForm`: Handles email/password state.
  - `SocialLogin`: "Sign in with Google" (Gold border).
- **User Interactions**:
  - "Enter" button triggers a "Door Opening" animation (slide out).
  - Success: Redirects to Dashboard.
- **API Requirements**:
  - `POST /auth/login` (Mock).
  - `POST /auth/register` (Mock).

#### **Forgot Password**
- **Layout**: Simple centered card. Input: Email. Action: "Send Carrier Pigeon".

---

### 3. App Pages (The Sanctum)

#### **Dashboard (Overview)**
- **Layout Structure**:
  - **Grid**: 12 columns.
  - **Top**: Welcome Message ("Greetings, [User]").
  - **Widgets**:
    - **Stats (Top)**: 3 Cards (Total Jobs, Storage Used, Credits). Icons: Ankh, Pyramid, Scroll.
    - **Recent Activity (Main)**: Table of last 5 jobs.
    - **System Status (Side)**: Service Health (Green/Gold dots).
- **Theme Application**:
  - Table rows have a thin gold line on hover.
  - Background has floating "Eye of Horus".
- **API Requirements**:
  - `GET /api/stats` (Mock).
  - `GET /api/jobs/recent` (Mock).

#### **New Job (The Ritual)**
- **Layout Structure**:
  - **Tabs**: Downloader | Converter | ASR | Translator (Styled as stone tablets).
  - **Content Area**: Changes based on Tab.
- **Components**:
  - **Downloader**:
    - `UrlInput`: Large, centered.
    - `FormatSelector`: Gold dropdown.
  - **Converter**:
    - `FileDropzone`: Dashed gold border. "Drag artifact here".
  - **ASR**:
    - `LanguageSelect`: Searchable.
- **User Interactions**:
  - Clicking "Start" triggers a "Ritual Start" animation (Gold light fills the button).
- **API Requirements**:
  - `POST /downloader/download`
  - `POST /converter/convert/video`
  - `POST /asr/transcribe/audio`

#### **Job List**
- **Layout**: Full-width Table.
- **Columns**: ID, Type (Icon), Name, Status, Date, Actions.
- **Status Badges**:
  - Running: Pulsing Gold text.
  - Failed: Red text.
  - Completed: Green text.
- **API Requirements**: `GET /api/jobs` (Mock).

#### **Job Detail (The Scroll)**
- **Layout**:
  - **Header**: Job ID, Status, "Back to Temple" button.
  - **Split View**:
    - **Left**: Preview (Video Player / Audio Player).
    - **Right**: Logs / Metadata / Download Links.
- **Theme Application**: Video player controls are styled gold.
- **API Requirements**: `GET /api/jobs/{id}` (Mock).

#### **File Browser (The Archive)**
- **Layout**: Grid of file icons (Video, Audio, Text).
- **Interactions**: Right-click context menu (Custom gold menu).
- **API Requirements**: `GET /api/files` (Mock).

#### **Account / Billing**
- **Layout**: Settings form. Avatar upload. Plan details.
- **Theme Application**: "Delete Account" is a "Banish" button (Red/Gold).

#### **Static File Preview**
- **Layout**: Minimal viewer. Text content or Media player.

---

### 4. Admin Pages

#### **Admin Users**
- **Layout**: Table of users. Actions: Ban, Promote.

#### **Admin Jobs Queue**
- **Layout**: Kanban board or List.
- **States**: Pending, Processing, Completed, Failed.

#### **Admin Analytics**
- **Layout**: Charts (Recharts styled with Gold lines).
- **Metrics**: API Usage, Error Rates.

---

## 🔌 API Requirements (Frontend Contract)

Since the backend is currently stateless/file-based, the Frontend will need a **BFF (Backend for Frontend)** or a wrapper to handle state if we want a rich experience, OR we strictly follow the existing API.

**Existing Endpoints to Map:**
- `POST /downloader/download` -> Triggers download job.
- `POST /converter/convert/video` -> Triggers conversion.
- `POST /asr/transcribe/audio` -> Triggers transcription.

**Missing / Recommended Endpoints (for full SaaS feel):**
- `GET /jobs`: List all past jobs (Needs DB or file-system scan).
- `GET /jobs/{id}`: Get specific job status.
- `GET /files`: List files in `downloads/` and `converted/`.
- `POST /auth/login`: (Mock for now).

---

## 🏃 Interaction & Motion Guidelines

- **Hover**: Elements should lift (`translate-y-1`) and glow.
- **Transitions**: Page transitions should be a smooth "Fade + Scale" (0.98 -> 1.00).
- **Loading**: Never use default browser spinners. Use a **Rotating Ankh** or **Filling Bar** (Gold liquid).
- **Success**: A burst of gold particles or a drawn checkmark.

---

## ✅ Developer Checklist
- [ ] Set up `frontend` folder with Vite + React + TS.
- [ ] Install `tailwindcss`, `framer-motion`, `lucide-react`.
- [ ] Configure `tailwind.config.js` with the Obsidian/Gold palette.
- [ ] Create `Layout.tsx` with the Living Background.
- [ ] Build `Button`, `Card`, `Input` components.
- [ ] Implement Routing (`react-router-dom`).
- [ ] Build Pages one by one (Home -> Auth -> Dashboard).
