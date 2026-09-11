# PAIMANA — Frontend + Telegram Alert Bot

Two independent services, neither of which touches `api.py` or Spring Boot:

```
paimana-app/
├── frontend/       React (Vite) app — predict form, chatbot UI, risk dashboard
└── telegram-bot/   Standalone Node/Express service — sends the Telegram messages
```

## Why a separate telegram-bot service at all?

The React app runs in the browser, so it can never hold your Telegram bot
token safely — anyone could read it from devtools and message on your
bot's behalf. `telegram-bot/` is a tiny server that holds the token and
exposes two routes for the frontend to call.

## How the alerting actually works

Nothing in `api.py` or Spring Boot changed. The trigger point lives in the
frontend, right where the risk tier first becomes known:

1. User submits the predict form → frontend calls `POST /api/predict` on
   your existing FastAPI service, unchanged.
2. FastAPI responds with `predictions.overall_risk_tier`.
3. **If it's `"High"`**, the frontend immediately calls
   `POST /alert/high-risk` on `telegram-bot/`, which formats and sends the
   Telegram message. This is a client-side check, not a new backend route.
4. **Regardless of risk tier**, the result panel has a "Send Telegram
   alert" button that calls `POST /alert/manual` on `telegram-bot/` any
   time the user wants to notify the team manually, with an optional note.

Caveat worth knowing: because the trigger lives in the browser, an alert
only fires for projects submitted *through this frontend*. If Spring Boot
or another client calls `/api/predict` directly, no alert fires for that
call — there was no other way to do this without adding a route to
`api.py` or Spring Boot, per your constraint.

## Setup

### 1. Telegram bot service

```bash
cd telegram-bot
cp .env.example .env
# fill in TELEGRAM_BOT_TOKEN (from @BotFather) and TELEGRAM_CHAT_ID
npm install
npm run dev
```

Runs on `http://localhost:4000` by default.

### 2. Frontend

```bash
cd frontend
cp .env.example .env
# defaults point at localhost:8000 (your FastAPI service) and localhost:4000
npm install
npm run dev
```

Runs on `http://localhost:5173` by default. Make sure your FastAPI
service (`uvicorn chatbot.api:app --reload`) is also running — CORS is
already wide open there (`allow_origins=["*"]`), so no backend change is
needed for the frontend to call it.

## Pages

- **Predict** (`/`) — the project form from `ProjectForm` in `api.py`,
  calling `/api/predict`. Shows the returned risk tiers, predicted
  overrun/delay, and the manual alert control.
- **Ask PAIMANA** (`/chat`) — calls `/api/chat`, keeps conversation
  history in the format `chatbot.py` expects (`role: "user" | "model"`).
  If you just submitted a project, there's a toggle to keep the
  conversation focused on it (sends it as `user_project`) or open it up
  to general dataset questions.
- **Risk dashboard** (`/dashboard`) — reads the three read-only endpoints
  backed by `predictions_summary.py`: risk distribution, sector-wise risk,
  and top 10 riskiest projects.

## Notes

- The dashboard endpoints read from the historical dataset directly — if
  `merged_projects.csv` hasn't been run through `score_dataset.py` yet,
  every tier will show as "Unknown" (matches the flag from our earlier
  review).
- Dates on the predict form use `MM/YYYY` to match the convention in your
  cleaning notebooks; `model_inference.py` parses this with
  `pd.to_datetime(errors="coerce")`, so adjust the placeholder if your
  models actually expect a different format.
- `telegram-bot/` is intentionally dumb — it has no idea what "high risk"
  means beyond "the caller says `overall_risk_tier === 'High'`". All risk
  logic still lives in `risk.py`, exactly where it already was.
