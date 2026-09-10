export const TELEGRAM_CONFIG = {
  chatId: '8951589926',
  botToken: '8891945925:AAEw7HUakcT3cCnOlCwzls8qtW1Bbmhued8',
}

export async function sendTelegramAlert(project, source = 'Manual dispatch') {
  try {
    if (!project || (!project.id && !project.project_name && !project.name)) {
      return { success: false, error: 'Project data missing.' }
    }

    const payload = {
      project_name: project.project_name || project.name || project.id || 'Unknown Project',
      risk_level: project.risk_level || project.overall_risk_tier || project.riskBand || 'High',
      source,
    }

    const response = await fetch('/api/telegram/alert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    const result = await response.json()

    if (!response.ok) {
      return { success: false, error: result?.detail || 'Telegram message failed.' }
    }

    return { success: true, message: result.message || 'Alert sent successfully.' }
  } catch (error) {
    return { success: false, error: error?.message || 'Telegram message failed.' }
  }
}

export async function sendHighRiskSummaryAlert(projects) {
  try {
    const response = await fetch('/api/telegram/alert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_name: 'Portfolio High Risk Summary',
        risk_level: 'High',
        source: 'Portfolio summary',
      }),
    })

    const result = await response.json()
    return response.ok
      ? { ok: true, count: Array.isArray(projects) ? projects.length : 0, message: result.message }
      : { ok: false, error: result?.detail || 'Summary alert failed.' }
  } catch (error) {
    return { ok: false, error: error?.message || 'Summary alert failed.' }
  }
}
