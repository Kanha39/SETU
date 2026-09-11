const TIER_STYLES = {
  High: "bg-brick/10 text-brick border-brick/30",
  Medium: "bg-ochre/10 text-ochre border-ochre/30",
  Low: "bg-moss/10 text-moss border-moss/30",
  Unknown: "bg-steel/10 text-steel border-steel/30",
};

export default function RiskBadge({ tier, label }) {
  const style = TIER_STYLES[tier] || TIER_STYLES.Unknown;
  return (
    <span className={`inline-flex items-center gap-1.5 rounded border px-2.5 py-1 text-xs font-medium ${style}`}>
      {label ? `${label}: ${tier || "Unknown"}` : tier || "Unknown"}
    </span>
  );
}
