const numberFormatter = new Intl.NumberFormat("en-IN", {
  maximumFractionDigits: 2,
});

export function formatNumber(value, fallback = "—") {
  if (value === null || value === undefined || value === "") return fallback;
  const number = Number(value);
  return Number.isFinite(number) ? numberFormatter.format(number) : fallback;
}

export function formatCrore(value, fallback = "—") {
  const formatted = formatNumber(value, fallback);
  return formatted === fallback ? formatted : `${formatted} Cr`;
}

export function formatPercent(value, fallback = "—") {
  const formatted = formatNumber(value, fallback);
  return formatted === fallback ? formatted : `${formatted}%`;
}
