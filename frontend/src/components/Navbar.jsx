import { NavLink } from "react-router-dom";
import { useProject } from "../context/ProjectContext.jsx";

function StateEmblemLogo() {
  return (
    <div className="flex items-center gap-3">
      {/* User Uploaded Official MoSPI Emblem & Ministry Title Logo */}
      <img
        src="/mospi_logo.png"
        alt="Ministry of Statistics and Programme Implementation"
        className="h-14 w-auto object-contain"
      />
    </div>
  );
}

export default function Navbar() {
  const { user, logoutUser } = useProject();

  return (
    <header className="sticky top-0 z-50 bg-white shadow-sm">
      {/* Top Header Bar (White Background) */}
      <div className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-2.5 sm:px-6">
          <NavLink to="/" className="flex items-center gap-4">
            <StateEmblemLogo />

            <div className="flex items-center gap-4 border-l border-slate-300 pl-4">
              <div>
                <h1 className="text-3xl font-black tracking-tight text-[#0b2545] font-serif leading-none">
                  SETU
                </h1>
                <p className="text-[11px] font-semibold text-[#002B49] mt-1 hidden sm:block">
                  National Infrastructure Risk Monitoring & Management System
                </p>
              </div>
            </div>
          </NavLink>

          {/* Right Controls: User Login */}
          <div className="flex items-center gap-3.5">
            {user ? (
              <div className="flex items-center gap-3">
                <span className="text-xs font-bold text-[#002B49] hidden md:inline">Hi, {user.name || user.email}</span>
                <button
                  type="button"
                  onClick={logoutUser}
                  className="rounded-md bg-[#f59e0b] px-4 py-1.5 text-xs font-bold text-white shadow-sm hover:bg-amber-600 transition-colors"
                >
                  Logout
                </button>
              </div>
            ) : (
              <NavLink
                to="/auth"
                className="rounded-md bg-[#f59e0b] px-5 py-1.5 text-xs font-extrabold text-white shadow-sm hover:bg-amber-600 transition-colors"
              >
                Login
              </NavLink>
            )}
          </div>
        </div>
      </div>

      {/* Bottom Navigation Strip (Dark Navy Blue Bar) */}
      <div className="bg-[#0b2545] shadow-md border-t border-[#133863]">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-2 sm:px-6">
          <nav className="flex flex-wrap items-center gap-6 sm:gap-8 text-xs font-bold uppercase tracking-wider text-slate-100">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                `pb-0.5 transition-all ${
                  isActive ? "text-amber-400 border-b-2 border-amber-400 font-extrabold" : "hover:text-amber-300"
                }`
              }
            >
              Home
            </NavLink>

            <NavLink
              to="/dashboard"
              className={({ isActive }) =>
                `pb-0.5 transition-all ${
                  isActive ? "text-amber-400 border-b-2 border-amber-400 font-extrabold" : "hover:text-amber-300"
                }`
              }
            >
              Dashboard
            </NavLink>

            <NavLink
              to="/chatbot"
              className={({ isActive }) =>
                `pb-0.5 transition-all ${
                  isActive ? "text-amber-400 border-b-2 border-amber-400 font-extrabold" : "hover:text-amber-300"
                }`
              }
            >
              AI Chatbot
            </NavLink>

            <NavLink
              to="/about"
              className={({ isActive }) =>
                `pb-0.5 transition-all ${
                  isActive ? "text-amber-400 border-b-2 border-amber-400 font-extrabold" : "hover:text-amber-300"
                }`
              }
            >
              About Us
            </NavLink>

            <NavLink
              to="/links"
              className={({ isActive }) =>
                `pb-0.5 transition-all ${
                  isActive ? "text-amber-400 border-b-2 border-amber-400 font-extrabold" : "hover:text-amber-300"
                }`
              }
            >
              Important Links
            </NavLink>
          </nav>
        </div>
      </div>
    </header>
  );
}