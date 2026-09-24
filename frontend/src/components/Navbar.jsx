import { NavLink } from "react-router-dom";
import { useProject } from "../context/ProjectContext.jsx";

const links = [
  { to: "/", label: "Home", end: true },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/chatbot", label: "Chatbot" },
];

function BrandMark() {
  return (
    <div className="flex items-center gap-3">
      <div className="flex h-10 w-10 items-center justify-center rounded-md bg-[#D4AF37] font-bold text-[#002B49]">
        P
      </div>
      <div>
        <span className="block text-xl font-bold tracking-wider text-white">SETU</span>
        <span className="block text-[10px] uppercase tracking-widest text-slate-300">
          Infrastructure Intelligence
        </span>
      </div>
    </div>
  );
}

export default function Navbar() {
  const { user, logoutUser } = useProject();

  return (
    <header className="sticky top-0 z-40 bg-[#002B49] shadow-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-4 py-3 sm:px-6">
        <NavLink to="/" className="flex items-center gap-3">
          <BrandMark />
        </NavLink>

        <nav className="flex flex-wrap items-center justify-end gap-6 text-sm font-medium">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.end}
              className={({ isActive }) =>
                `pb-1 transition-all ${
                  isActive
                    ? "border-b-2 border-[#D4AF37] font-semibold text-[#D4AF37]"
                    : "text-slate-200 hover:text-[#D4AF37]"
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}

          {user ? (
            <>
              <span className="text-slate-200">Hi, {user.name || user.email}</span>
              <button
                type="button"
                onClick={logoutUser}
                className="rounded border border-[#D4AF37] px-3 py-1.5 text-[#D4AF37]"
              >
                Logout
              </button>
            </>
          ) : (
            <NavLink to="/auth" className="rounded bg-[#D4AF37] px-3 py-1.5 font-bold text-[#002B49]">
              Login / Signup
            </NavLink>
          )}
        </nav>
      </div>
    </header>
  );
}