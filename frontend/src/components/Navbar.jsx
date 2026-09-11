import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Predict", end: true },
  { to: "/chat", label: "Ask SETU" },
  { to: "/dashboard", label: "Risk dashboard" },
];

function BrandMark() {
  return (
    <svg
      width="640"
      height="220"
      viewBox="0 0 640 220"
      xmlns="http://www.w3.org/2000/svg"
      className="h-14 w-auto shrink-0"
      aria-label="SETU logo"
      role="img"
    >
      <title>SETU</title>
      <desc>SETU logo: a single-mast cable-stayed bridge whose deck extends into the wordmark, with the tagline "Infrastructure Intelligence" beneath.</desc>

      <rect x="24" y="178" width="592" height="8" rx="4" fill="#1B2A4A" />

      <rect x="100" y="40" width="10" height="138" rx="3" fill="#1B2A4A" />
      <circle cx="105" cy="38" r="7" fill="#1B2A4A" />

      <line x1="105" y1="50" x2="50" y2="178" stroke="#E0A458" strokeWidth="3" strokeLinecap="round" />
      <line x1="105" y1="50" x2="72" y2="178" stroke="#E0A458" strokeWidth="3" strokeLinecap="round" />
      <line x1="105" y1="50" x2="94" y2="178" stroke="#E0A458" strokeWidth="3" strokeLinecap="round" />

      <line x1="105" y1="50" x2="116" y2="178" stroke="#E0A458" strokeWidth="3" strokeLinecap="round" />
      <line x1="105" y1="50" x2="138" y2="178" stroke="#E0A458" strokeWidth="3" strokeLinecap="round" />
      <line x1="105" y1="50" x2="160" y2="178" stroke="#E0A458" strokeWidth="3" strokeLinecap="round" />

      <circle cx="50" cy="178" r="4" fill="#E0A458" />
      <circle cx="72" cy="178" r="4" fill="#E0A458" />
      <circle cx="94" cy="178" r="4" fill="#E0A458" />
      <circle cx="116" cy="178" r="4" fill="#E0A458" />
      <circle cx="138" cy="178" r="4" fill="#E0A458" />
      <circle cx="160" cy="178" r="4" fill="#E0A458" />

      <text x="210" y="132" fontFamily="Arial, Helvetica, sans-serif" fontWeight="800" fontSize="86" letterSpacing="3" fill="#1B2A4A">
        SETU
      </text>
      <text x="213" y="160" fontFamily="Arial, Helvetica, sans-serif" fontWeight="400" fontSize="15" letterSpacing="1.5" fill="#8A7048">
        Infrastructure intelligence
      </text>
    </svg>
  );
}

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-ink/10 bg-paper/80 backdrop-blur-sm">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-6 px-4 py-4 sm:px-6">
        <NavLink to="/" className="flex items-center gap-3">
          <BrandMark />
          
        </NavLink>

        <nav className="flex flex-wrap items-center justify-end gap-5 text-sm">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.end}
              className={({ isActive }) =>
                `pb-1 border-b-2 transition-colors ${
                  isActive ? "border-blueprint text-ink" : "border-transparent text-steel hover:text-ink"
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}
