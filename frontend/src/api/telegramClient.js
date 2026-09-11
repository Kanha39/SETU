import axios from "axios";

// Talks to the standalone telegram-bot/ service, not api.py.
const telegramClient = axios.create({
  baseURL: import.meta.env.VITE_TELEGRAM_BOT_URL || "http://localhost:4000",
  headers: { "Content-Type": "application/json" },
});

export function sendHighRiskAlert(project, predictions) {
  return telegramClient.post("/alert/high-risk", { project, predictions });
}

export function sendManualAlert(project, predictions, note) {
  return telegramClient.post("/alert/manual", { project, predictions, note });
}

export default telegramClient;
