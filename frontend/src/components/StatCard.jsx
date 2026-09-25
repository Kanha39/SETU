export default function StatCard({ label, value, sub }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-6 text-center shadow-sm transition-shadow hover:shadow-md">
      <p className="text-3xl font-extrabold tracking-tight text-[#002B49] font-sans">{value}</p>
      <p className="mt-2 text-xs font-semibold uppercase tracking-[0.12em] text-slate-500">{label}</p>
      {sub && <p className="mt-2 text-xs text-slate-500">{sub}</p>}
    </div>
  );
}