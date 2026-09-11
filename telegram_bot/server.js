import "dotenv/config";
import express from "express";
import cors from "cors";
import { sendTelegramMessage } from "./src/telegram.js";
import { formatAlertMessage } from "./src/formatMessage.js";

const app = express();
app.use(cors({ origin: process.env.ALLOWED_ORIGIN || "*" }));
app.use(express.json());

app.get("/health", (_req, res) => res.json({ status: "ok" }));

// Called by the frontend immediately after /api/predict responds with
// predictions.overall_risk_tier === "High". This service never talks to
// api.py or MySQL itself -- the frontend is what noticed the risk tier
// and is reporting it here, which is why api.py doesn't need any changes.
app.post("/alert/high-risk", async (req, res) => {
  try {
    const { project, predictions } = req.body || {};

    if (!predictions || predictions.overall_risk_tier !== "High") {
      return res.status(400).json({
        error: "This endpoint only accepts predictions with overall_risk_tier === 'High'.",
      });
    }

    const text = formatAlertMessage(project, predictions, "auto");
    await sendTelegramMessage(text);
    res.json({ sent: true });
  } catch (err) {
    console.error("[alert/high-risk]", err.message);
    res.status(500).json({ error: err.message });
  }
});

// Called by the "Send Telegram alert" button in the UI. Fires regardless
// of risk tier -- the user decides when this is worth flagging.
app.post("/alert/manual", async (req, res) => {
  try {
    const { project, predictions, note } = req.body || {};
    let text = formatAlertMessage(project, predictions, "manual");
    if (note && note.trim()) {
      text += `\n\nNote: ${note.trim()}`;
    }
    await sendTelegramMessage(text);
    res.json({ sent: true });
  } catch (err) {
    console.error("[alert/manual]", err.message);
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`PAIMANA telegram-alert service listening on port ${PORT}`);
});
