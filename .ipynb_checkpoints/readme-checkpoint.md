# PAIMANA - Team Collaboration Guide

Welcome to the **PAIMANA** (Project Analysis & Infrastructure Monitoring Analytics) team! 🚀

This guide explains how we work together over the next 10 days to build a production-grade AI system for predicting high-risk government infrastructure projects.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Team Structure](#team-structure)
3. [Development Setup](#development-setup)
4. [Git Workflow](#git-workflow)
5. [Communication](#communication)
6. [Daily Standup](#daily-standup)
7. [Code Review Process](#code-review-process)
8. [Testing Standards](#testing-standards)
9. [Documentation](#documentation)
10. [Common Commands](#common-commands)
11. [Troubleshooting](#troubleshooting)
12. [File Handoffs](#file-handoffs)
13. [Deployment](#deployment)
14. [House Rules](#house-rules)
15. [Success Criteria](#success-criteria)
16. [Quick Reference](#quick-reference)
17. [Important Links](#important-links)
18. [FAQ](#faq)

---

## Quick Start

### Before Day 1 (Everyone)

```bash
# 1. Clone repository
git clone https://github.com/your-org/paimana-infrastructure-monitoring.git
cd paimana-infrastructure-monitoring

# 2. Create your personal branch
git checkout -b feature/person{1-5}-{name}
# Example: git checkout -b feature/person1-kanhaapandey

# 3. Install dependencies (your role-specific)
# See "Development Setup" section below

# 4. Read your role documentation
# See "Team Structure" section below

# 5. Join Slack/Discord channel
# Link: [Your communication channel]
```

### Day 1 Morning (Everyone)

- [ ] Complete setup
- [ ] Introduce yourself in Slack with your role & timezone
- [ ] Confirm you can run your module
- [ ] Ask questions (no question is stupid!)

---

## Team Structure

### Person 1: Data Engineer (You)

**Role:** ML Pipeline - Data Processing  
**Responsibility:** Extract, clean, merge data  
**Days:** 1-2  
**Deliverable:** `paimana_merged_cleaned.csv` (18,485 rows)

**Your Guide:** `docs/DATA_MERGING_CLEANING_STRATEGY.md`

```
What you do:
├── Extract 14 PDFs using pdfplumber
├── Clean 4 raw CSVs
├── Merge into single dataset
├── Create ML features
└── Save to data/processed/

Who needs your work:
├── Person 2 (Cost model training)
├── Person 3 (Time model training)
├── Person 4 (Database loading)
└── Person 5 (Frontend visualization)
```

**Critical Path:** Person 2, 3, and 4 are all blocked waiting for your CSV on Day 2!

---

### Person 2: ML Engineer - Cost Model

**Role:** Cost Overrun Prediction  
**Responsibility:** Train XGBoost model  
**Days:** 3-4  
**Deliverable:** `cost_model.pkl` (R² > 0.65)

**Your Guide:** `docs/PAIMANA_PROJECT_PLAN.md` (Section 2B)

```
What you do:
├── Read Person 1's CSV
├── Train XGBoost regression
├── Tune hyperparameters
├── Achieve R² > 0.65
└── Save model + metrics

Dependencies:
└── Waits for Person 1's CSV (Day 2 EOD)

Who needs your work:
├── Person 4 (Backend API)
└── Person 3 (Risk scoring)
```

---

### Person 3: ML Engineer - Time Model

**Role:** Time Delay Prediction  
**Responsibility:** Train LightGBM model  
**Days:** 3-4  
**Deliverable:** `time_model.pkl` (AUC > 0.70)

**Your Guide:** `docs/PAIMANA_PROJECT_PLAN.md` (Section 2C)

```
What you do:
├── Read Person 1's CSV
├── Train LightGBM binary classifier
├── Handle class imbalance
├── Achieve AUC > 0.70
└── Save model + metrics

Dependencies:
└── Waits for Person 1's CSV (Day 2 EOD)

Who needs your work:
├── Person 4 (Backend API)
└── Person 2 (Risk scoring)
```

---

### Person 4: Backend Engineer

**Role:** REST API + AI Integration  
**Responsibility:** Spring Boot backend + Gemini  
**Days:** 5-6  
**Deliverable:** Live REST API at `http://localhost:8080`

**Your Guide:** `docs/SPRINGBOOT_BACKEND_GUIDE.md`

```
What you do:
├── Create Spring Boot project
├── Design 4 entities (Project, Prediction, Analysis, Alert)
├── Build 4 REST controllers
├── Integrate Gemini API
├── Load PostgreSQL with 18,485 projects
└── Create batch prediction endpoint

Dependencies:
├── Person 1's CSV (for database seeding)
└── Person 2 & 3's models (for predictions)

Who needs your work:
└── Person 5 (Frontend + Bot)
```

---

### Person 5: Full-Stack Engineer

**Role:** Frontend Dashboard + Telegram Bot  
**Responsibility:** React UI + Bot  
**Days:** 7-8  
**Deliverables:**
- Dashboard at `http://localhost:3000`
- Telegram bot running

**Your Guides:**
- `docs/REACT_FRONTEND_GUIDE.md`
- `docs/PAIMANA_PROJECT_PLAN.md` (Section 4)

```
Part 1: React Dashboard
├── Create 5 pages (Home, Dashboard, Projects, Detail, Alerts)
├── Build 10+ reusable components
├── Connect to Person 4's API
└── Display predictions from Person 2 & 3

Part 2: Telegram Bot
├── Setup bot handlers (5 commands)
├── Connect to Person 4's API
├── Schedule daily 7 AM alerts
└── Format responses with emojis

Dependencies:
└── Person 4's live API (Day 6 EOD)

Who needs your work:
└── Demo team (Day 10)
```

---

## Development Setup

### All Team Members

```bash
# Clone and setup
git clone https://github.com/your-org/paimana-infrastructure-monitoring.git
cd paimana-infrastructure-monitoring

# Copy environment template
cp .env.example .env
# Fill in your variables (API keys, tokens, etc.)

# Install Docker (required for local dev)
# Download: https://www.docker.com/products/docker-desktop
```

---

### Person 1 - Data Engineer Setup

```bash
# Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd ml-pipeline
pip install -r requirements.txt

# Verify setup
python -c "import pandas, pdfplumber, numpy; print('✅ All dependencies installed')"

# Open Jupyter
jupyter notebook notebooks/

# Your first notebook: 02_data_cleaning.ipynb
```

**Check:** Can you run `import pdfplumber` without errors?

---

### Person 2 & 3 - ML Engineer Setup

```bash
# Python environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd ml-pipeline
pip install -r requirements.txt

# Verify setup
python -c "import xgboost, lightgbm, sklearn; print('✅ ML libraries ready')"

# Open Jupyter
jupyter notebook notebooks/

# Wait for Person 1's CSV before starting training
```

**Check:** Can you run `import xgboost` and `import lightgbm`?

---

### Person 4 - Backend Engineer Setup

```bash
# Prerequisites
# 1. Install Java 11+: https://www.oracle.com/java/technologies/downloads/
# 2. Install Maven: https://maven.apache.org/download.cgi

# Navigate to backend
cd backend

# Create Spring Boot project (if not already created)
# Option 1: Use Spring Boot CLI
spring boot new --from=gs/rest-service paimana-backend

# Option 2: Use IDE (IntelliJ/VS Code)
# Create new Maven project

# Install dependencies
mvn clean install

# Run application
mvn spring-boot:run

# Check: http://localhost:8080/health
# Expected: {"status":"UP"}
```

**Check:** Can you access `http://localhost:8080/health`?

---

### Person 5 - Frontend Engineer Setup

```bash
# Prerequisites
# 1. Install Node.js 16+ (includes npm): https://nodejs.org/

# Create React app
cd frontend
npx create-react-app . --template typescript

# Install dependencies
npm install

# Install additional packages
npm install axios react-router-dom @mui/material @emotion/react @emotion/styled
npm install recharts  # For charts

# Start development server
npm start

# Check: http://localhost:3000
# You should see the React welcome screen
```

**Telegram Bot Setup:**

```bash
# Python environment
cd telegram-bot
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Get Telegram bot token
# 1. Message @BotFather on Telegram
# 2. Create new bot
# 3. Copy token to .env file

# Verify setup
python -c "import telegram, apscheduler; print('✅ Bot libraries ready')"
```

**Check:** Can you access `http://localhost:3000`?

---

## Git Workflow

### Branching Strategy

We use **feature branches** with PR reviews.

```
main (production)
  ↓
develop (integration branch)
  ↓
feature/person{1-5}-{feature-name} (your branch)
```

### Your Branch Naming

```bash
# Create your personal feature branch
git checkout -b feature/person1-data-cleaning
git checkout -b feature/person2-cost-model
git checkout -b feature/person3-time-model
git checkout -b feature/person4-backend-api
git checkout -b feature/person5-frontend-dashboard
```

### Daily Workflow

```bash
# Start of day
git checkout develop
git pull origin develop

# Sync your branch with latest develop
git checkout feature/person1-data-cleaning
git merge develop

# Do your work
# Edit files, test locally

# Check what you changed
git status

# Stage your changes
git add .

# Commit with clear message
git commit -m "feat(data): Extract and clean monthly_completed_projects.csv"

# Push to your branch
git push origin feature/person1-data-cleaning

# Create Pull Request on GitHub
# Go to: https://github.com/your-org/paimana
# Click "Create Pull Request"
# Add description: what you did, blockers, etc.
```

### Commit Message Format

Follow this format for clarity:

```
<type>(<scope>): <subject>

feat(data): Extract 14 PDFs using pdfplumber
fix(ml): Handle NaN values in cost_model
docs(readme): Add collaboration guide
test(pipeline): Add unit tests for data cleaning
chore(deps): Update pandas to 2.0
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `test` - Tests
- `chore` - Dependencies, config, etc.
- `refactor` - Code cleanup

### Pull Request Process

```
1. Push your branch
   git push origin feature/person1-data-cleaning

2. Go to GitHub → Create Pull Request
   - Title: feat(data): Extract and clean projects
   - Description: What did you do? Any blockers?
   - Assign reviewers: 1-2 team members

3. Wait for review (target: within 1 hour)
   - Respond to comments
   - Make requested changes
   - Push updates: git push origin feature/person1-data-cleaning

4. Get approval (at least 1 review)

5. Merge to develop
   - GitHub will show "Merge Pull Request" button
   - Delete branch after merging

6. Sync your local repo
   git checkout develop
   git pull origin develop
```

### Handling Conflicts

If someone else pushed to develop:

```bash
# Fetch latest
git fetch origin

# Rebase your branch on develop
git rebase origin/develop

# If conflicts occur:
# 1. Open conflicted files
# 2. Resolve conflicts manually
# 3. git add .
# 4. git rebase --continue
# 5. git push origin feature/person1-data-cleaning --force-with-lease
```

---

## Communication

### Communication Channels

| Channel | Purpose | Frequency |
|---------|---------|-----------|
| **Slack #standup** | Daily updates | 10 AM daily |
| **Slack #blockers** | Problem solving | As needed |
| **Slack #wins** | Celebrate progress | Daily |
| **Discord/Video Call** | Meetings | Scheduled |
| **GitHub Issues** | Technical issues | As needed |
| **GitHub Discussions** | Architecture Q&A | As needed |

### Slack Etiquette

- ✅ Do ask questions anytime
- ✅ Do share errors/logs when stuck
- ✅ Do ping relevant person for review
- ❌ Don't wait silently if blocked
- ❌ Don't work on someone else's deliverable
- ❌ Don't commit secrets (API keys, tokens)

**Example Slack Message:**

```
Person 1: Hey team! Just extracted 14 PDFs ✅
Merged 3 datasets - looking good. Will have CSV ready by EOD today.
Any blockers? Need anything from me?

Person 2: Awesome! Can't wait. Will start training as soon as you push.

Person 4: Great! I'll prepare the database schema while we wait.
```

---

## Daily Standup

### Time: 10 AM (Your Timezone)

**Duration:** 15 minutes max

**Format (Post in Slack #standup):**

```
🟢 Person 1 - Data Engineer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Completed:
   - Extracted 7 of 14 PDFs
   - Cleaned monthly_ongoing dataset

🔄 In Progress:
   - Extracting remaining 7 PDFs
   - Starting merge process

⛔ Blockers:
   - None - on track!

📅 Next:
   - Merge 3 datasets tomorrow
   - Deliver CSV by EOD Day 2

🌐 Timezone: IST
```

**Everyone Does This Every Morning:**

```markdown
✅ What did you finish yesterday?
🔄 What are you working on today?
⛔ What's blocking you?
📅 What's your next milestone?
```

### Weekly Sync (Friday 5 PM)

```
Duration: 30 minutes
Agenda:
1. Integration status (all pieces working together?)
2. Any architectural changes needed?
3. Prepare for next week
4. Celebrate wins 🎉
```

---

## Code Review Process

### You Are Reviewing Someone's Code?

```
1. Read the PR description first
2. Understand what they're trying to do
3. Check the code for:
   ✅ Does it work?
   ✅ Is it clean/readable?
   ✅ Are there tests?
   ✅ Is it documented?
   ✅ Does it follow our standards?

4. Comment constructively:
   ❌ Bad: "This is wrong"
   ✅ Good: "Consider using pandas.apply() instead - it's more idiomatic"

5. Approve when satisfied
```

### Your Code Is Being Reviewed?

```
1. Respond to all comments (even if just "will fix")
2. Don't feel bad about feedback - it's about the code, not you
3. Ask for clarification if unclear
4. Push updates quickly
5. Re-request review after changes
```

### Review Checklist

Before asking for review, check:

- [ ] Code runs without errors
- [ ] All tests pass
- [ ] Code is formatted (consistent style)
- [ ] No hardcoded paths or secrets
- [ ] Has comments for complex logic
- [ ] Follows naming conventions
- [ ] PR description explains what & why

---

## Testing Standards

### Before You Push:

**Person 1 (Data):**
```bash
cd ml-pipeline
python -m pytest tests/test_data_cleaning.py -v
# All tests should pass ✅
```

**Person 2 & 3 (ML):**
```bash
cd ml-pipeline
python -m pytest tests/test_models.py -v
# Check model metrics meet targets
```

**Person 4 (Backend):**
```bash
cd backend
mvn test
# All unit tests pass
mvn integration-test
# All integration tests pass
```

**Person 5 (Frontend):**
```bash
cd frontend
npm test
# All component tests pass

# Manual test:
npm start
# Verify no console errors
```

### Test Coverage

Everyone should have at least **80% code coverage** in their module.

```bash
# Check coverage
cd ml-pipeline
pytest --cov=src tests/

# View HTML report
open htmlcov/index.html
```

---

## Documentation

### Documenting Your Code

**Python (docstrings):**
```python
def merge_datasets(df1, df2):
    """
    Merge two project datasets.
    
    Args:
        df1: DataFrame with completed projects
        df2: DataFrame with ongoing projects
    
    Returns:
        DataFrame: Combined dataset with 18,485 rows
    
    Raises:
        ValueError: If required columns missing
    
    Example:
        >>> merged = merge_datasets(completed, ongoing)
        >>> print(len(merged))
        18485
    """
    pass
```

**Java (Javadoc):**
```java
/**
 * Predict cost overrun for a project.
 * 
 * @param projectId ID of project
 * @return PredictionDTO with cost_risk (0-1)
 * @throws ResourceNotFoundException if project not found
 */
public PredictionDTO predictCost(String projectId) {
    // implementation
}
```

**TypeScript (JSDoc):**
```typescript
/**
 * Fetch high-risk projects
 * @param threshold Risk threshold (0-1)
 * @param limit Number of projects to return
 * @returns Promise<Project[]> High-risk projects
 */
async function getHighRiskProjects(
  threshold: number,
  limit: number = 20
): Promise<Project[]> {
  // implementation
}
```

### README Files

Each component should have a `README.md`:

```markdown
# Component Name

## Purpose
What does this do?

## Usage
How do you use it?

## Input/Output
What goes in? What comes out?

## Example
Show an example

## Dependencies
What's needed?

## Testing
How to run tests?
```

### API Documentation

Backend: Use Swagger annotations
```java
@GetMapping("/api/predictions/high-risk")
@ApiOperation("Get high-risk projects")
@ApiParam("Risk threshold 0-1")
public List<PredictionDTO> getHighRisk(@RequestParam double threshold) {
    // implementation
}

// Accessible at: http://localhost:8080/swagger-ui.html
```

---

## Common Commands

### Git

```bash
# Sync your branch with develop
git fetch origin
git rebase origin/develop

# Push your work
git push origin feature/person1-data-cleaning

# Check status
git status
git log --oneline

# Undo last commit
git reset --soft HEAD~1

# See what changed
git diff
```

### Python

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Jupyter
jupyter notebook

# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_data_cleaning.py::test_merge_datasets -v
```

### Maven (Java)

```bash
# Clean & build
mvn clean install

# Run application
mvn spring-boot:run

# Run tests only
mvn test

# Skip tests (fast build)
mvn clean install -DskipTests
```

### npm (React)

```bash
# Install dependencies
npm install

# Start dev server
npm start

# Run tests
npm test

# Build for production
npm run build

# Install new package
npm install package-name
```

### Docker

```bash
# Build all services
docker-compose build

# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f service-name
# Example: docker-compose logs -f paimana-backend

# Run command in service
docker-compose exec paimana-backend sh
```

---

## Troubleshooting

### "I'm stuck and blocked"

1. **Post in Slack #blockers** (Don't sit silently!)
   ```
   @team I'm stuck on extracting PDFs - pdfplumber keeps crashing.
   Error: [paste error message]
   Anyone faced this before?
   ```

2. **Check GitHub Issues** (Similar problems solved?)

3. **Ask your mentor/tech lead** (That's what they're here for)

### Common Issues

**Problem:** `ModuleNotFoundError: No module named 'pandas'`
```bash
# Solution:
cd ml-pipeline
source venv/bin/activate
pip install pandas
```

**Problem:** `Port 8080 already in use`
```bash
# Solution: Kill the process
lsof -i :8080
kill -9 <PID>

# Or change port in application.properties:
# server.port=8081
```

**Problem:** `npm ERR! code ERESOLVE`
```bash
# Solution:
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

**Problem:** Git merge conflicts
```bash
# Solution:
git status  # See conflicted files
# Open files and manually resolve conflicts
# Look for: <<<<<<< HEAD ... >>>>>>> branch-name
git add .
git rebase --continue
```

**Problem:** `docker-compose: command not found`
```bash
# Solution:
# Install Docker Desktop (includes docker-compose)
# Or use: docker compose up (newer Docker versions)
```

### Getting Help

| Problem | Ask | Where |
|---------|-----|-------|
| Code question | Your team | Slack |
| Git issue | Tech lead | Slack + Screen share |
| Architecture decision | Tech lead | Discord call |
| Data question | Person 1 | Any channel |
| Model question | Person 2 or 3 | Any channel |
| API question | Person 4 | Any channel |
| UI question | Person 5 | Any channel |

---

## File Handoffs

### Day 2 → Person 2 & 3 (From Person 1)

```
Person 1 completes:
├── ml-pipeline/data/processed/paimana_merged_cleaned.csv
├── ml-pipeline/config/feature_schema.py
└── Documentation: README.md with column descriptions

Person 2 & 3 receive:
└── Start training on the CSV

Handoff process:
1. Person 1 commits to develop
2. Person 1 posts in Slack: "CSV ready! Linked to branch feature/person1-data-cleaning"
3. Person 2 & 3 pull latest develop
4. Person 2 & 3 start notebooks/04_cost_model.ipynb and 05_time_model.ipynb
```

### Day 4 → Person 4 (From Person 2 & 3)

```
Person 2 & 3 complete:
├── ml-pipeline/data/models/cost_model.pkl
├── ml-pipeline/data/models/time_model.pkl
├── ml-pipeline/data/models/scaler.pkl
└── ml-pipeline/data/models/model_metrics.json

Person 4 receives:
└── Load models into Spring Boot PredictionService

Handoff process:
1. Person 2 & 3 push models to ml-pipeline/data/models/
2. Person 2 & 3 posts: "Models ready! cost_model.pkl (R²=0.68), time_model.pkl (AUC=0.72)"
3. Person 4 loads models in PredictionService.java
4. Person 4 tests with: /api/predictions/predict?projectCode=xxx
```

### Day 6 → Person 5 (From Person 4)

```
Person 4 completes:
├── Live API at http://localhost:8080
├── All 4 REST controllers working
├── PostgreSQL loaded with 18,485 projects
└── Swagger docs at http://localhost:8080/swagger-ui.html

Person 5 receives:
└── Build React dashboard + Telegram bot

Handoff process:
1. Person 4 posts API endpoints list
2. Person 5 reads Swagger docs
3. Person 5 calls endpoints from React
4. Person 5 calls endpoints from Telegram bot
5. Test with: npm start (React) and python bot.py (Telegram)
```

---

## Deployment

### Day 9 - Integration Testing

```bash
# Run everything together
docker-compose -f docker-compose.yml up

# Test endpoints
curl http://localhost:8080/api/projects
curl http://localhost:8080/api/predictions/high-risk

# Access dashboard
open http://localhost:3000

# Test bot
/alert  # Should return top 5 high-risk projects

# Check logs
docker-compose logs -f
```

### Day 10 - Final Demo Setup

```bash
# Clean startup
docker-compose down
docker-compose build --no-cache
docker-compose up

# Pre-load demo data (optional)
docker-compose exec paimana-backend python /scripts/seed_demo_data.py

# Verify all services
✅ http://localhost:3000 (Dashboard loads)
✅ http://localhost:8080/swagger-ui.html (API docs visible)
✅ Telegram bot responds to /alert
✅ Click project → shows cost/time predictions
✅ Gemini analysis displays root causes
```

### Production Checklist (After Hackathon)

- [ ] Remove hardcoded secrets (use .env)
- [ ] Add error handling & logging
- [ ] Setup monitoring (New Relic, DataDog)
- [ ] Configure CI/CD (GitHub Actions)
- [ ] Setup automated backups (PostgreSQL)
- [ ] Add rate limiting (API)
- [ ] Setup load testing
- [ ] Create runbooks for operations

---

## House Rules

### Do's ✅

- ✅ Ask questions early and often
- ✅ Push to your branch daily (even if not finished)
- ✅ Review others' code promptly (within 1 hour)
- ✅ Celebrate milestones 🎉
- ✅ Document as you go
- ✅ Test locally before pushing
- ✅ Communicate blockers immediately
- ✅ Give constructive feedback
- ✅ Help teammates when they're stuck

### Don'ts ❌

- ❌ Work on someone else's component without asking
- ❌ Merge your own PR (always need review)
- ❌ Commit API keys or secrets
- ❌ Work in main/develop directly (use feature branches)
- ❌ Skip testing before pushing
- ❌ Forget to pull before starting work
- ❌ Sit silently when blocked (ask for help!)
- ❌ Rewrite someone's code without discussion
- ❌ Leave breaking changes without warning

---

## Success Criteria

### By Day 2
- [ ] Person 1 has delivered paimana_merged_cleaned.csv
- [ ] Everyone has tested their local environment
- [ ] No blocker issues in Day 1-2

### By Day 4
- [ ] Person 2's cost model: R² > 0.65
- [ ] Person 3's time model: AUC > 0.70
- [ ] Models saved and tested

### By Day 6
- [ ] Person 4's API live and responding
- [ ] All endpoints tested
- [ ] PostgreSQL loaded with data

### By Day 8
- [ ] React dashboard displays projects
- [ ] Telegram bot sends alerts
- [ ] No console errors

### By Day 9
- [ ] docker-compose up works end-to-end
- [ ] All services communicate
- [ ] Demo data loaded

### By Day 10
- [ ] 5-minute demo runs smoothly
- [ ] Everyone can explain their part
- [ ] GitHub submission ready

---

## Quick Reference

### I Need To...

| Task | Command | Location |
|------|---------|----------|
| Clone repo | `git clone ...` | Terminal |
| Start coding | `git checkout -b feature/...` | Terminal |
| Save work | `git commit -m "..."` + `git push` | Terminal |
| Ask for review | Create PR on GitHub | Browser |
| See what changed | `git diff` | Terminal |
| Find my status | Check GitHub Issues/Projects | Browser |
| Ask for help | Post in Slack #blockers | Slack |
| See API docs | Open http://localhost:8080/swagger-ui.html | Browser |
| Run tests | `pytest` / `mvn test` / `npm test` | Terminal |
| View logs | `docker-compose logs -f` | Terminal |

---

## Important Links

- **Repository:** [GitHub Link]
- **Project Board:** [GitHub Projects Link]
- **Documentation:** `docs/` folder in repo
- **Slack Channel:** #paimana-team
- **Video Calls:** [Discord/Zoom Link]
- **API Docs:** http://localhost:8080/swagger-ui.html (when running)
- **Dashboard:** http://localhost:3000 (when running)

---

## FAQ

**Q: What if Person 1 is late delivering the CSV?**

A: Person 2 & 3 can prepare notebooks, explore data structure, setup environments. Person 4 can create database schema. No one is completely blocked.

**Q: What if my code breaks someone else's code?**

A: That's why we have PR reviews! We catch issues before merging to develop. If it happens, we rollback and fix together.

**Q: Can I work on multiple modules?**

A: No - stay focused on your module. If you finish early, help another person's module, but don't own it.

**Q: What if I find a bug in someone else's code?**

A: Create a GitHub Issue or tell them in Slack. Don't fix it without asking (they might be fixing it already).

**Q: How do we handle time zone differences?**

A: Standups happen at a set time (10 AM). Record updates in Slack for those not present. Async is key.

**Q: What's the deadline if I'm blocked?**

A: Tell the team IMMEDIATELY in #blockers. We have tech leads to help. Blocking yourself is not an option.

**Q: How do I know if my code quality is good?**

A: Ask your reviewers! They'll check for:
- Readability (Can someone else understand it?)
- Maintainability (Can we update it 6 months later?)
- Performance (Does it run fast enough?)
- Testability (Can we test it?)

**Q: What if I disagree with feedback in a code review?**

A: Have a respectful discussion! 
- Explain your reasoning
- Ask for clarification if confused
- Agree to compromise if needed
- Escalate to tech lead only if really stuck

**Q: Can I commit partially finished work?**

A: Yes! Use work-in-progress (WIP) branches:
```bash
git commit -m "wip(data): Halfway through cleaning"
git push
```
Then convert to real PR when ready for review.

---

## Final Thoughts

This is a **collaborative sprint**, not a solo project. Everyone's success depends on everyone else.

- 🤝 Be a good teammate
- 🚀 Communicate clearly
- ✅ Deliver on time
- 📝 Document your work
- 🎓 Help others learn

**Let's build something amazing together!** 🚀

---

**Questions?** Drop them in Slack #blockers or tag @tech-lead

**Ready to go?** See you on Day 1! 💪

---

## Document Metadata

- **Last Updated:** September 3, 2026
- **Version:** 1.0
- **Maintained By:** Tech Lead
- **For Questions:** Contact @tech-lead on Slack
- **Repository:** [Your GitHub Link]
- **License:** MIT

---

*This document should be reviewed and updated after the hackathon with lessons learned.*