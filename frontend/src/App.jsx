import { Link, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import HomePage from "./pages/HomePage.jsx";
import ProjectFormPage from "./pages/ProjectFormPage.jsx";
import ProjectAnalysisPage from "./pages/ProjectAnalysisPage.jsx";
import ProjectOverviewPage from "./pages/ProjectOverviewPage.jsx";
import ProjectRiskPage from "./pages/ProjectRiskPage.jsx";
import ChatPage from "./pages/ChatPage.jsx";
import AlertsPage from "./pages/AlertsPage.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";
import AuthPage from "./pages/AuthPage.jsx";
import MinistryPage from "./pages/MinistryPage.jsx";
import SectorPage from "./pages/SectorPage.jsx";

export default function App() {
  return (
    <div className="min-h-screen bg-[#FFFDF8] font-sans text-slate-800">
      <Navbar />
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/projects/new" element={<ProjectFormPage />} />
          <Route path="/projects/analysis" element={<ProjectAnalysisPage />} />
          <Route path="/projects/:projectId" element={<ProjectOverviewPage />} />
          <Route path="/projects/:projectId/risk" element={<ProjectRiskPage />} />
          <Route path="/projects/:projectId/risk/latest" element={<ProjectRiskPage />} />
          <Route path="/ministries" element={<MinistryPage />} />
          <Route path="/sectors" element={<SectorPage />} />
          <Route path="/chatbot" element={<ChatPage />} />
          <Route path="/alerts" element={<AlertsPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/auth" element={<AuthPage />} />
        </Routes>
      </main>

      <Link
        to="/chatbot"
        aria-label="Open SETU chatbot"
        className="fixed bottom-6 right-6 flex h-12 w-12 items-center justify-center rounded-full bg-[#002B49] text-white shadow-lg transition-transform hover:scale-105"
      >
        ✦
      </Link>
    </div>
  );
}