# SETU

SETU is a full-stack infrastructure project monitoring and risk intelligence platform for public-sector projects. The repository combines a Java Spring Boot application, a React frontend, a Python ML/AI service, and a Telegram alert bot.

This project is not a single monolithic backend. The main application logic lives in `PAIMANA-backend/` and the AI/ML prediction layer lives in `chatbot/`.

## Project overview

SETU helps teams to:
- register and manage infrastructure projects
- generate risk scores for cost and time overruns
- track project status, ministry, sector, implementation agency, and delivery health
- view dashboard summaries of project risk distribution
- ask project-specific questions through a chatbot
- generate mitigation strategies from a questionnaire
- raise Telegram alerts for high-risk projects

## Architecture

The repository contains four major runtime components:

1. Java Spring Boot application
   - Path: `PAIMANA-backend/`
   - Purpose: primary app backend for auth, user sessions, project CRUD, risk generation, dashboard summary, chatbot orchestration, mitigation logic, and alerts
   - Technology: Java 17, Spring Boot 4, Spring Security, Spring Data JPA, MySQL, JWT

2. React frontend
   - Path: `frontend/`
   - Purpose: user interface for login, project intake, dashboard, risk analysis, chatbot, and alerts
   - Technology: React, Vite, React Router, Axios, Recharts, Tailwind CSS

3. Python AI + ML service
   - Path: `chatbot/`
   - Purpose: exposes prediction and chatbot APIs used by the Spring Boot layer
   - Technology: FastAPI, Python, Pandas, NumPy, Scikit-learn, XGBoost, LightGBM, ChromaDB, Gemini API

4. Telegram alert service
   - Path: `telegram_bot/`
   - Purpose: sends project alerts to a configured Telegram channel/chat
   - Technology: Node.js, Express, dotenv

## Repository structure

```text
SIH_PAIMANA/
├── PAIMANA-backend/
│   ├── src/
│   ├── pom.xml
│   ├── mvnw
│   └── mvnw.cmd
├── chatbot/
│   ├── api.py
│   ├── chatbot.py
│   ├── config.py
│   ├── context_builder.py
│   ├── data_loader.py
│   ├── db.py
│   ├── entity_extractor.py
│   ├── llm_client.py
│   ├── migrate_csv_to_mysql.py
│   ├── model_inference.py
│   ├── predictions_summary.py
│   ├── questionnaire_mitigation.py
│   ├── requirements.txt
│   ├── retrieval.py
│   ├── risk.py
│   ├── schema.sql
│   └── similar_projects.py
├── database/
│   └── chroma_store/
├── frontend/
│   ├── public/
│   ├── src/
│   ├── README.md
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
├── ml-pipeline/
│   ├── data/
│   ├── notebooks/
│   ├── src/
│   ├── README_cost_model (1).md
│   └── requirements.txt
├── telegram_bot/
│   ├── server.js
│   ├── src/
│   ├── package.json
│   └── .env.example
├── .venv/
├── readme.md
├── .gitignore
└── .python-version
```

## Core technical stack

### Spring Boot backend
- Java 17
- Spring Boot 4
- Spring Security
- Spring Data JPA / JDBC
- MySQL / H2 support
- JWT authentication
- WebClient for downstream service calls
- OpenAPI / Swagger support

### Frontend
- React 18
- Vite
- React Router
- Recharts
- Axios
- Tailwind CSS

### Python ML / chatbot service
- Python 3.10+
- FastAPI
- Pydantic
- Pandas, NumPy
- Scikit-learn
- XGBoost
- LightGBM
- Joblib
- Gemini / Google GenAI
- ChromaDB

### Telegram bot
- Node.js 18+
- Express
- dotenv
- CORS

## Actual backend flow in this repo

The app follows a multi-service design:

1. Frontend sends requests to the Spring Boot app in `PAIMANA-backend`.
2. Spring Boot handles authentication, project creation, and user project records.
3. When a project needs risk scoring, Spring Boot calls the Python ML API through `MLServiceClient`.
4. For chatbot responses, Spring Boot calls the Python chatbot endpoint through `ChatbotServiceClient`.
5. The Python service returns prediction/chat answers and Spring Boot persists and returns the result to the frontend.
6. Telegram alerts are triggered by the standalone `telegram_bot` service.

This means the Spring Boot backend is the main application backend, while `chatbot/api.py` is an AI/ML service consumed by the Java app.

## Important Spring Boot details

The Spring Boot app is configured to run on port 8080 and uses environment variables such as:

```properties
server.port=${PORT:8080}

spring.datasource.url=${SPRING_DATASOURCE_URL:...}
spring.datasource.username=${SPRING_DATASOURCE_USERNAME:...}
spring.datasource.password=${SPRING_DATASOURCE_PASSWORD:...}

jwt.secret=${JWT_SECRET:...}
ml.service.base-url=${ML_SERVICE_BASE_URL:...}
chatbot.service.base-url=${CHATBOT_SERVICE_BASE_URL:...}
```

The app also includes security rules, JWT filters, and protected API endpoints.

## Main Spring Boot endpoints

The Java backend exposes the following core routes:

### Authentication
```http
POST /api/auth/register
POST /api/auth/login
```

### Project management
```http
POST /api/projects
GET /api/projects
GET /api/projects/{projectId}
PUT /api/projects/{projectId}
```

### Risk generation
```http
POST /api/projects/{projectId}/risk/generate
GET /api/projects/{projectId}/risk/latest
```

### Chatbot
```http
POST /api/chatbot/query
GET /api/chatbot/sessions
GET /api/chatbot/sessions/{sessionId}/messages
```

### Dashboard
```http
GET /api/dashboard/summary
```

### Mitigation
```http
POST /api/mitigation/questionnaire
POST /api/mitigation/generate
GET /api/mitigation/{projectName}/{sessionId}/strategies
```

### Alerts
```http
GET /api/alerts
POST /api/alerts/{alertId}/acknowledge
```

## Python FastAPI endpoints

The Python service in `chatbot/` exposes its own API layer:

### Health and general checks
```http
GET /api/health
```

### ML prediction
```http
POST /api/predict
```

### Chatbot answer generation
```http
POST /api/chat
```

### Dashboard summary
```http
GET /api/dashboard/risk-summary
GET /api/dashboard/sector-risk
GET /api/dashboard/top-risky
GET /api/dashboard/mega-projects
```

### Mitigation generation
```http
POST /api/project/mitigation
```

## Frontend API configuration

The frontend uses axios clients with environment variables:

```js
baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
```

This is important because the frontend can talk to the Python FastAPI service directly for ML/dashboard functions, while the Java backend is the core application layer. The frontend also talks to the Telegram bot separately:

```js
baseURL: import.meta.env.VITE_TELEGRAM_BOT_URL || "http://localhost:4000"
```

## Environment variables

### Java Spring Boot backend
Create environment variables or use `.env`/shell exports:

```bash
export PORT=8080
export SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/setu_db
export SPRING_DATASOURCE_USERNAME=root
export SPRING_DATASOURCE_PASSWORD=your_password
export JWT_SECRET=your_long_jwt_secret
export ML_SERVICE_BASE_URL=http://localhost:8000
export CHATBOT_SERVICE_BASE_URL=http://localhost:8000
```

### Python chatbot service
```bash
export GEMINI_API_KEY=your_gemini_api_key
```

### Telegram bot
Create `telegram_bot/.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
PORT=4000
ALLOWED_ORIGIN=http://localhost:5173
```

### Frontend
Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8080
VITE_ML_API_BASE_URL=http://localhost:8000
VITE_TELEGRAM_BOT_URL=http://localhost:4000
```

## Local setup and run commands

### 1. Start the Spring Boot backend

```bash
cd SIH_PAIMANA/PAIMANA-backend
./mvnw spring-boot:run
```

Default URL:
```text
http://localhost:8080
```

### 2. Start the Python AI/ML service

```bash
cd SIH_PAIMANA
source .venv/bin/activate
python -m chatbot.api
```

Default URL:
```text
http://localhost:8000
```

### 3. Start the Telegram bot

```bash
cd SIH_PAIMANA/telegram_bot
npm install
npm start
```

Default URL:
```text
http://localhost:4000
```

### 4. Start the frontend

```bash
cd SIH_PAIMANA/frontend
npm install
npm run dev
```

Default URL:
```text
http://localhost:5173
```

## Data and model notes

The project uses historical infrastructure project datasets and trained ML models for predictions and dashboard insights.

Relevant locations:
- `ml-pipeline/data/processed/merged_projects.csv`
- `ml-pipeline/src/04_COST_MODEL (1).py`
- `ml-pipeline/src/time_model.py`
- `ml-pipeline/data/models/`

The Python service reads historical data for similar-project retrieval and dashboard summaries, and the Spring Boot app orchestrates these calls.

## Typical workflow

1. User registers or logs in through the Spring Boot backend.
2. User creates a project in the React app.
3. Spring Boot stores the project record and calls the ML service for risk prediction.
4. The ML service computes predicted overrun and delay values.
5. The Spring Boot app stores the risk results and exposes them via dashboard/project APIs.
6. The chatbot service answers project-specific questions using historical and current context.
7. High-risk projects can trigger Telegram alerts.

## Troubleshooting

### Spring Boot fails to start
Check:
- Java 17 is installed
- MySQL credentials are valid
- `SPRING_DATASOURCE_URL` is correct
- JWT secret is configured

### Python service is not responding
Check:
- virtual environment is activated
- `pip install -r chatbot/requirements.txt` was run
- `GEMINI_API_KEY` exists if chatbot generation is enabled
- `ml-pipeline` data files are present

### Frontend cannot reach backend
Check:
- `VITE_API_BASE_URL` points to the right backend port
- the Java app is running on port 8080
- CORS settings are allowed for the frontend origin

### Telegram alerts are not sent
Check:
- `telegram_bot/.env` is populated
- the Telegram bot token is valid
- the chat ID is correct
- the Node service is running on port 4000

## Deployment guidance

For production deployment, keep the service split as follows:
- `PAIMANA-backend` as the main secured application backend
- `chatbot/` as the Python ML + LLM service
- `frontend/` as the client application
- `telegram_bot/` as a separate notification service

Use environment variables for secrets and keep MySQL/JWT credentials out of source control.

## Summary

SETU is a multi-service infrastructure risk platform with:
- a Java Spring Boot core application
- a Python AI/ML backend for prediction and chatbot logic
- a React frontend for user interaction
- a Node Telegram notification service

The README now reflects the actual architecture of the repository rather than an older single-backend assumption.
