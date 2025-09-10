# Software Requirements Specification (SRS)

## Scope
Local‑first calorie prediction service with secure API and web dashboard for authenticated users.

## Actors
- User (member)
- System (FastAPI service)
- Database (SQLite)

## Functional Requirements
- FR1: Users can register and login (JWT auth).
- FR2: Authenticated users can submit inputs (age, gender, height, weight, duration, heart_rate, body_temp) and receive predicted calories.
- FR3: System stores each prediction with inputs, user, and timestamp.
- FR4: Users can retrieve recent history (≤ 50).
- FR5: Admin/system can train a model via CLI and store the artifact.

## Non‑Functional Requirements
- NFR1: Latency < 1s per request on target hardware.
- NFR2: MAE within target threshold on held‑out split.
- NFR3: Local‑first storage; no external data egress by default.
- NFR4: Availability ≥ 99% for demo; graceful error handling.
- NFR5: Security: hashed passwords, JWT tokens, CSRF‑safe usage from SPA, CORS restrictions in prod.

## Data Requirements
- Tables: `users(id, username, password_hash, created_at)`, `predictions(id, user_id, inputs..., calories, created_at)`.
- Artifact: `backend/models/calories_xgb.joblib`.

## Constraints
- Python 3.11; dataset shape/features as per Kaggle demo files.
