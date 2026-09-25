import { Link } from "react-router-dom";

export default function ActionCard({ title, description, to, badge, highlight }) {
  return (
    <Link
      to={to}
      className={`group relative flex flex-col justify-between rounded-lg border bg-white p-6 transition-all hover:-translate-y-0.5 hover:shadow-md ${
        highlight ? "border-[#D4AF37] ring-1 ring-[#D4AF37]/50" : "border-slate-200"
      }`}
    >
      <div>
        <span className="inline-block rounded bg-slate-100 px-2.5 py-1 text-xs font-semibold text-[#002B49]">
          {badge}
        </span>
        <h3 className="mt-3 text-lg font-bold text-[#002B49] group-hover:text-[#1A5276]">
          {title}
        </h3>
        <p className="mt-2 text-sm leading-relaxed text-slate-600">{description}</p>
      </div>
      <span className="mt-4 text-xs font-bold text-[#D4AF37] group-hover:underline">
        Explore section →
      </span>
    </Link>
  );
}