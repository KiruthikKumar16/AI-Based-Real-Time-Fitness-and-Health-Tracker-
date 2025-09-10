# AI-Based Real-Time Fitness and Health Tracker

End-to-end capstone-ready system for calorie prediction and fitness tracking with:
- Data science notebook and training pipeline (baselines + Optuna tuning)
- FastAPI backend with JWT auth, predict, and history on SQLite
- Minimal web dashboard (login, predict, view history)
- Docker + docker-compose, and CI (GitHub Actions)

## Repo Structure
```
.
├── backend/                    # FastAPI service, model service, training CLI
│   ├── app/
│   │   ├── main.py             # FastAPI app (auth, predict, history)
│   │   ├── routers.py          # /predict, /history
│   │   ├── auth.py             # JWT, password hashing
│   │   ├── database.py         # SQLAlchemy engine/session
│   │   ├── models.py           # User, Prediction models
│   │   ├── model_service.py    # Load/train XGBoost, save joblib
│   │   └── train_cli.py        # Baselines + Optuna tuning; saves best model
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
├── frontend/                   # Minimal dashboard (static)
│   ├── index.html
│   ├── styles.css
│   └── main.js
├── calories-burnt-prediction/  # Original notebook + data placement
│   ├── Calories Burnt Prediction.py
│   ├── README.md
│   └── ...
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Prerequisites
- Python 3.11
- (Optional) Docker + Docker Compose
- Place dataset CSVs in `calories-burnt-prediction/`:
  - `calories.csv`
  - `exercise.csv`

## Quick Start (Windows PowerShell)
Setup venv and install
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\pip install -r backend\requirements.txt
```

Train best model (baselines + Optuna)
```powershell
.\.venv\Scripts\python -m backend.app.train_cli --data-dir calories-burnt-prediction
```

Run API
```powershell
.\.venv\Scripts\python -m uvicorn backend.app.main:app --reload
# Health: http://127.0.0.1:8000/health
```

Register/Login/Predict (PowerShell)
```powershell
$reg = @{ username='demo'; password='demo123!' } | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8000/auth/register -Method POST -Body $reg -ContentType 'application/json'
$login = @{ username='demo'; password='demo123!' } | ConvertTo-Json
$tok = Invoke-RestMethod http://127.0.0.1:8000/auth/login -Method POST -Body $login -ContentType 'application/json'
$token = $tok.access_token
$body = @{ age=25; gender=0; height=175; weight=70; duration=45; heart_rate=140; body_temp=37.5 } | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8000/predict -Method POST -Body $body -ContentType 'application/json' -Headers @{ Authorization = "Bearer $token" }
Invoke-RestMethod http://127.0.0.1:8000/history -Headers @{ Authorization = "Bearer $token" }
```

Open Dashboard
- Open `frontend/index.html` in your browser
- Login with your credentials
- Enter parameters and Predict; history updates live

## Docker
```bash
docker compose up --build
# API on http://127.0.0.1:8000
```

## CI (GitHub Actions)
- On push/PR to `main` or `next`, installs backend deps and runs tests

## Branching
- `v1` baseline (frozen)
- `next` ongoing development

## Notes
- CORS enabled for local development
- Data stays local; SQLite DB file lives under `backend/`
- Original exploratory notebook remains in `calories-burnt-prediction/`
