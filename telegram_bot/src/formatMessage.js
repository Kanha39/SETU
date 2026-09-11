function escapeHtml(str) {
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/**
 * project: the enriched `project_data` object returned by /api/predict
 * predictions: the `predictions` block returned by /api/predict
 * mode: "auto" | "manual"
 */
export function formatAlertMessage(project = {}, predictions = {}, mode = "manual") {
  const { project_name, project_code, agency, state, sector, ministry } = project || {};
  const {
    predicted_overrun_pct,
    predicted_delay_days,
    cost_risk_tier,
    time_risk_tier,
    overall_risk_tier,
  } = predictions || {};

  const heading =
    mode === "auto"
      ? "\u{1F6A8} <b>High-risk project detected</b>"
      : "\u{1F4E3} <b>Project alert</b>";

  const locationLine = [state, sector].filter(Boolean).map(escapeHtml).join(" \u00B7 ");

  const lines = [
    heading,
    "",
    `<b>${escapeHtml(project_name || "Unknown project")}</b>${
      project_code ? ` (${escapeHtml(project_code)})` : ""
    }`,
    agency ? `Agency: ${escapeHtml(agency)}` : null,
    locationLine || null,
    ministry ? `Ministry: ${escapeHtml(ministry)}` : null,
    "",
    predicted_overrun_pct != null ? `Predicted cost overrun: ${predicted_overrun_pct}%` : null,
    predicted_delay_days != null ? `Predicted delay: ${predicted_delay_days} days` : null,
    overall_risk_tier ? `Overall risk: ${overall_risk_tier}` : null,
    cost_risk_tier ? `Cost risk: ${cost_risk_tier}` : null,
    time_risk_tier ? `Time risk: ${time_risk_tier}` : null,
  ].filter(Boolean);

  return lines.join("\n");
}
