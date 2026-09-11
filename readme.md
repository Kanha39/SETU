# PAIMANA Project README

PAIMANA is a project risk monitoring and prediction platform for infrastructure projects. It combines a React frontend, a FastAPI backend, ML-based project risk prediction, a chatbot assistant, and optional Telegram alerting.

## 1. Project Overview

### Core objectives
- Predict cost overrun and delay risk for ongoing projects
- Show dashboard summaries for risk distribution and top risky projects
- Allow users to ask contextual questions through the chatbot
- Support project-level risk analysis with historical comparable projects
- Send Telegram alerts when a project is flagged as high risk

### Main components
- Frontend: `frontend/`
- Backend API: `chatbot/api.py`
- Chatbot logic: `chatbot/chatbot.py`
- Model inference and scoring: `chatbot/model_inference.py`
- Risk calculation: `chatbot/risk.py`
- Historical data source: `ml-pipeline/data/processed/merged_projects.csv`
- ML model training scripts: `ml-pipeline/src/`
- Telegram bot service: `telegram_bot/`

---

## 2. Architecture

### High-level flow
1. User enters a project in the frontend prediction form.
2. Frontend sends data to `POST /api/predict` on the FastAPI backend.
3. Backend prepares the feature row, runs the saved ML models, computes risk tiers, and stores session state.
4. Dashboard endpoints read processed summary data and return charts / tables.
5. Chatbot uses the user’s submitted project context and historical data to answer questions.
6. Telegram bot can send alerts when high-risk predictions are detected.

### Current implementation notes
- The backend currently uses the processed CSV (`ml-pipeline/data/processed/merged_projects.csv`) as the historical retrieval dataset for chat context and comparable projects.
- MySQL / database connectivity is not the main retrieval path in the current MVP; the app uses the CSV-based processed data for fast historical lookup and the backend keeps session state in memory.
- If MySQL is later used for persistent application data, the backend can be extended to query it while keeping the current CSV-based retrieval logic for similarity access.

---

## 3. Repository Structure

```text
SIH_PAIMANA/
├── chatbot/
│   ├── api.py
│   ├── chatbot.py
│   ├── config.py
│   ├── context_builder.py
│   ├── data_loader.py
│   ├── db.py
│   ├── entity_extractor.py
│   ├── gemini_client.py
│   ├── model_inference.py
│   ├── predictions_summary.py
│   ├── retrieval.py
│   ├── risk.py
│   ├── requirements.txt
│   └── schema.sql
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── .env
│   └── vite.config.js
├── ml-pipeline/
│   ├── data/
│   ├── notebooks/
│   ├── src/
│   ├── README_cost_model (1).md
│   └── requirements.txt
├── telegram_bot/
│   ├── server.js
│   ├── package.json
│   └── .env
├── docs/
├── config/
├── database/
├── tests/
├── .venv/
├── readme.md
└── .gitignore
```

---

## 4. Tech Stack

### Frontend
- React
- Vite
- React Router
- Recharts
- Axios
- React Markdown

### Backend
- FastAPI
- Python
- Pydantic
- Pandas
- NumPy
- Joblib
- Scikit-learn
- XGBoost
- LightGBM
- Gemini API integration

### Optional supporting services
- Telegram bot server (`telegram_bot/server.js`)
- MySQL / database layer (for future persistence)
- Ngrok for temporary external exposure

---

## 5. Environment Setup

### Python environment
Use the existing project virtual environment if available:

```bash
cd SIH_PAIMANA
source .venv/bin/activate
```

If you are setting up a fresh environment, install the backend requirements:

```bash
cd SIH_PAIMANA
python -m venv .venv
source .venv/bin/activate
pip install -r chatbot/requirements.txt
pip install -r ml-pipeline/requirements.txt
```

### Frontend environment
Install frontend dependencies:

```bash
cd SIH_PAIMANA/frontend
npm install
```

Make sure the frontend environment file contains the correct values:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_TELEGRAM_BOT_URL=http://localhost:4000
```

### Telegram bot environment
Configure Telegram bot secrets in `telegram_bot/.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
PORT=4000
ALLOWED_ORIGIN=*
```

### Gemini environment
The chatbot uses Gemini for answer generation. Ensure the backend environment has:

```env
GEMINI_API_KEY=your_gemini_api_key
```

---

## 6. Running the Project

### 1) Start the backend
```bash
cd SIH_PAIMANA
source .venv/bin/activate
python -m chatbot.api
```

The FastAPI server will run on:

```text
http://localhost:8000
```

### 2) Start the Telegram bot service
```bash
cd SIH_PAIMANA/telegram_bot
npm install
npm start
```

The Telegram service runs on:

```text
http://localhost:4000
```

### 3) Start the frontend
```bash
cd SIH_PAIMANA/frontend
npm run dev
```

The frontend will run on the Vite default port, typically:

```text
http://localhost:5173
```

---

## 7. Backend and API Overview

### Predict endpoint
`POST /api/predict`

Used to submit a new project and get:
- predicted overrun percentage
- predicted delay in days
- cost risk tier
- time risk tier
- overall risk tier
- session ID for follow-up chat

### Chat endpoint
`POST /api/chat`

Used for chatbot interaction with the user’s session.

### Dashboard endpoints
- `GET /api/dashboard/risk-summary`
- `GET /api/dashboard/sector-risk`
- `GET /api/dashboard/top-risky`

### Telegram alert endpoint
`POST /api/telegram/alert`

Used by the frontend or bot flow to send an operational Telegram alert.

---

## 8. Backend and Database Tunneling

### Why tunneling is useful
You may need to expose the backend or database to someone outside your local network, for example:
- a teammate testing the API
- a friend validating the chatbot endpoints
- a remote database connection from another machine

### Recommended tunneling approach
#### Option A: expose the FastAPI backend with ngrok
Run the backend locally first:

```bash
cd SIH_PAIMANA
source .venv/bin/activate
python -m chatbot.api
```

Then expose it with ngrok:

```bash
ngrok http 8000
```

Use the generated public URL only when you need remote access. For normal local frontend usage, keep the frontend pointed to:

```text
http://localhost:8000
```

This avoids unnecessary cross-origin and local-network issues.

#### Option B: expose MySQL / database access via SSH tunnel or a secure tunnel
If your database is hosted remotely and you want to access it from another machine, use a secure tunnel rather than exposing the database directly.

Typical patterns:
- SSH tunnel to localhost port forwarding
- cloud VPN / bastion-host access
- private tunnel service for internal users

Do not expose the database directly to the public internet unless it is properly secured.

### Important tunneling guidance
- Frontend should normally use the local backend URL during local development.
- Use ngrok only for temporary external testing.
- Backend and database access should be protected using credentials, whitelisting, or private network routing.

---

## 9. Historical Data and Retrieval Strategy

### Current historical retrieval approach
The current system uses the processed CSV file:

```text
ml-pipeline/data/processed/merged_projects.csv
```

This file is loaded by the chatbot-related retrieval flow so that related project history can be used for:
- contextual answers
- comparable project matching
- risk explanation grounded in past data

### Why this approach is used
- low-latency access
- no need to depend on a database query for every chat request
- easier deployment and consistent behavior on server environments

### Future scalability option
For larger-scale deployment, the project can evolve toward:
- a vector database for semantic retrieval
- MySQL-backed structured storage
- a hybrid setup where structured data stays in SQL and retrieval uses a vector store

---

## 10. ML Pipeline Notes

The ML pipeline is under `ml-pipeline/`.

### Key files
- `ml-pipeline/src/04_COST_MODEL (1).py` → cost overrun model
- `ml-pipeline/src/time_model.py` → delay model
- `ml-pipeline/data/models/cost_model.pkl` → saved cost model
- `ml-pipeline/data/models/time_model.pkl` → saved delay model
- `ml-pipeline/README_cost_model (1).md` → model design notes

### Model compatibility note
The saved model artifacts were previously generated with older package versions. If you retrain or regenerate models, use the same environment versions used during training to avoid compatibility issues.

---

## 11. Telegram Bot Notes

The Telegram bot is a lightweight independent service that sends alerts to a configured chat.

### Typical usage
- High-risk predictions trigger automatic Telegram alerts
- Manual alert sending is also supported from the frontend

### Important note
The Telegram bot is separate from the main FastAPI backend and does not replace the backend API.

---

## 12. Common Troubleshooting

### Frontend shows blank page after prediction
Check:
- backend is running on `http://localhost:8000`
- `frontend/.env` uses the correct backend URL
- `apiClient` has the right base URL

### Chat endpoint returns 422
Check that the request payload matches the backend schema:

```json
{
  "session_id": "<session-id>",
  "message": "your question"
}
```

### Prediction endpoint not loading model
Check:
- environment is activated
- model files exist in `ml-pipeline/data/models/`
- required model packages are installed
- the saved model artifacts were recreated in the current environment if compatibility issues occur

### Dashboard does not load data
Check:
- backend dashboard endpoints are running
- CSV data exists in `ml-pipeline/data/processed/`
- frontend `VITE_API_BASE_URL` is correct

---

## 13. Recommended Local Development Workflow

1. Activate the Python environment
2. Start the backend
3. Start the Telegram bot service
4. Start the frontend
5. Submit a project on the prediction page
6. Open the chatbot and send a question
7. Check the dashboard and risk summaries

---

## 14. Deployment Suggestions

### Minimal deployment setup
- Host the FastAPI backend on a server or cloud VM
- Host the frontend static build on Vercel / Netlify / cloud storage
- Keep the Telegram bot as a separate service
- Use a proper environment variable setup for secrets

### Better production setup
- Use a proper MySQL service for persistent application data
- Use a vector database for semantic retrieval if chatbot search becomes scale-heavy
- Add authentication / authorization if multiple users must be separated
- Add logging, monitoring, and health checks

---

## 15. Key Takeaways

- The project is a full-stack AI risk prediction and chatbot system.
- Main local development flow is: backend + telegram service + frontend.
- Current historical data retrieval is CSV-based for speed and simplicity.
- Local frontend should use `http://localhost:8000`, not an ngrok URL, unless you are testing external access.
- Database tunneling should be done securely, ideally through SSH / private tunnel mechanisms.

---

## 16. Useful Commands Summary

### Backend
```bash
cd SIH_PAIMANA
source .venv/bin/activate
python -m chatbot.api
```

### Frontend
```bash
cd SIH_PAIMANA/frontend
npm install
npm run dev
```

### Telegram bot
```bash
cd SIH_PAIMANA/telegram_bot
npm install
npm start
```

### ML pipeline
```bash
cd SIH_PAIMANA
source .venv/bin/activate
pip install -r ml-pipeline/requirements.txt
```

---

## 17. Notes for Future Improvements

- Add proper authentication and session management
- Move persistent data to a real database
- Improve retrieval via vector search
- Add automated health checks and monitoring
- Rebuild model artifacts in a pinned environment for reproducibility

If you want, this README can also be expanded into a deployment-specific version that documents your exact server setup, database credentials flow, and ngrok usage for public testing.
