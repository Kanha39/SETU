export default function StatCard({ label, value, sub }) {
  return (
    <div className="border border-ink/15 bg-white/40 p-5">
      <p className="text-xs text-steel">{label}</p>
      <p className="font-display text-3xl text-ink mt-1">{value}</p>
      {sub && <p className="text-xs text-steel mt-1">{sub}</p>}
    </div>
  );
}
