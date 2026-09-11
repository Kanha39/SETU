import { Link, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import PredictPage from "./pages/PredictPage.jsx";
import ChatPage from "./pages/ChatPage.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";

export default function App() {
  return (
    <div className="min-h-screen bg-paper text-ink">
      <Navbar />
      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        <Routes>
          <Route path="/" element={<PredictPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </main>

      <Link
        to="/chat"
        aria-label="Open PAIMANA chatbot"
        className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full border border-ink/10 bg-ink text-lg text-paper shadow-lg shadow-ink/20 transition-transform hover:scale-105"
      >
        ✦
      </Link>
    </div>
  );
}
