# CodeMind AI

CodeMind AI is a learning workspace for Python practice. It checks submissions against exercise tests, gives evidence-based feedback and progressive hints, saves attempts, estimates concept mastery, and chooses an exercise to try next.

This repository is a complete local prototype. The learning model and diagnosis rules are inspectable heuristics, not evidence of educational effectiveness. It currently uses a single local learner profile and does not include account management or classroom administration.

## Contents

- [Features](#included)
- [Technology stack](#technology-stack)
- [Project layout](#project-layout)
- [Quick start](#start-the-application-on-windows)
- [Architecture and submission flow](#architecture)
- [Configuration](#configuration)
- [API reference](#api)
- [Build and checks](#build-and-checks)
- [Troubleshooting](#troubleshooting)
- [Security and current limitations](#safety-and-prototype-limits)

## Included

- React + TypeScript dashboard and practice studio with Monaco Editor.
- FastAPI API for exercises, submissions, hints, attempt history, mastery estimates, progress, and recommendations.
- Eight starter Python exercises with deterministic checks and difficulty levels.
- AST-based structural observations and explainable diagnosis rules. Diagnoses are possibilities, not claims about student intent.
- Progressive conceptual and structural hints; a worked solution is returned only on explicit request.
- BKT-style per-concept estimates and concept prerequisite foundations.
- PostgreSQL for Docker Compose and SQLite for simple local API development.
- A disposable Docker execution container with no network, read-only root filesystem, CPU, memory, process, and time limits, and a read-only submission mount. Student code never runs in the FastAPI process.

## Technology stack

| Area | Technology | Role |
|---|---|---|
| Web application | React, TypeScript, Vite | Dashboard, practice flow, progress, and history views |
| Code editor | Monaco Editor | Python editing with syntax highlighting and editor conveniences |
| UI icons and styles | Lucide React, CSS | Interface icons and responsive layout |
| API | Python 3.11+, FastAPI, Pydantic | HTTP API, request validation, and orchestration |
| Code inspection | Python `ast` | Structural facts that support diagnosis rules |
| Code execution | Docker runner image | Isolated execution and test evaluation |
| Persistence | SQLite or PostgreSQL | Exercises, submissions, test results, and mastery estimates |
| Data access | SQLAlchemy | Database models and queries |

Frontend dependency versions are recorded in `package-lock.json`; backend dependency ranges are in `requirements.txt`. Explanations currently use deterministic templates, so no LLM API key is required.

## Project layout

```text
CODEMIND_AI/
├── backend/
│   ├── catalog.py       # Seed exercises and expected test cases
│   ├── db.py            # SQLite/PostgreSQL connection setup
│   ├── main.py          # FastAPI routes and startup
│   ├── models.py        # Exercise, submission, and mastery tables
│   ├── runner.py        # Docker invocation and bounded output handling
│   ├── schemas.py       # Validated API request models
│   └── tutor.py         # AST facts, diagnoses, hints, and BKT updates
├── src/
│   ├── App.tsx          # Screens and API interactions
│   ├── styles.css       # Responsive interface styles
│   ├── types.ts         # Frontend data types
│   ├── main.tsx         # React entry point
│   └── vite-env.d.ts    # Vite TypeScript definitions
├── Dockerfile.runner    # Disposable Python execution image
├── docker-compose.yml   # Optional PostgreSQL and runner-image build target
├── .env.example         # Local environment defaults
├── package.json         # Frontend scripts and dependencies
├── package-lock.json    # Reproducible frontend dependency tree
├── requirements.txt     # Backend dependencies
├── tsconfig*.json       # TypeScript compiler settings
└── README.md
```

## Start the application on Windows

Requirements: Python 3.11+, Node.js 22.12+ (or Node.js 20.19+), npm, and Docker Desktop with its Linux container engine running. The API uses Docker CLI to create short-lived runner containers, so Docker must be running when a submission is checked.

1. Open PowerShell in the project root and create a local environment file if one does not already exist:

   ```powershell
   if (!(Test-Path .env)) { Copy-Item .env.example .env }
   ```

2. Build the runner image:

   ```powershell
   docker compose --profile build-only build runner-image
   ```

   PostgreSQL is optional. If you want PostgreSQL instead of the default SQLite database, start the Compose database too:

   ```powershell
   docker compose up -d db
   ```

3. In a second PowerShell window, create the Python environment, install backend dependencies, and start the API:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   uvicorn backend.main:app --reload
   ```

   The default database is SQLite at `data/codemind.db`; no database service is required. To use the PostgreSQL service from step 2, set `DATABASE_URL` in `.env` before starting the API:

   ```env
   DATABASE_URL=postgresql+psycopg://codemind:codemind-local@localhost:5432/codemind
   ```

4. In a third terminal, install frontend dependencies and start Vite:

   ```powershell
   npm install
   npm run dev
   ```

Open [http://localhost:5173](http://localhost:5173). The API is at [http://localhost:8000](http://localhost:8000), with interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs). The frontend proxies `/api` requests to the local API.

To stop PostgreSQL, run `docker compose down`. To erase its data too, run `docker compose down -v`. SQLite data is in `data/codemind.db`.

## Architecture

```mermaid
flowchart LR
  Browser[React + TypeScript + Monaco] -->|REST /api| API[FastAPI]
  API --> AST[AST checks + diagnosis rules]
  API --> Runner[Disposable Docker runner]
  Runner --> Evaluation[Test-case evaluator]
  AST --> Diagnosis[Evidence-backed diagnosis]
  Evaluation --> Diagnosis
  Diagnosis --> Hints[Progressive hint selector]
  API --> DB[(PostgreSQL / SQLite)]
  Diagnosis --> DB
  DB --> BKT[BKT-style mastery estimate]
  BKT --> Recommender[Exercise recommender]
  Recommender --> Browser
```

The explanation service uses deterministic, evidence-backed templates. This keeps the prototype useful without an LLM key and avoids delegating correctness decisions to a language model. An LLM can be added later as a phrasing layer grounded in diagnoses and trusted teaching material.

### Submission flow

1. The student opens an exercise and edits the starter code in Monaco.
2. The frontend sends the exercise ID and code to `POST /api/submissions`.
3. The API enforces source limits and parses syntax, then creates a temporary runner script.
4. Docker runs the script with no network, a read-only root filesystem, capped CPU/memory/processes, a temporary directory, and a time limit.
5. The runner invokes the exercise function on the catalog's test inputs and returns per-test outcomes.
6. The tutor combines the test outcome with AST facts and exercise context to produce a likely diagnosis and supporting evidence.
7. The API stores the attempt and updates the learner's concept estimate.
8. The recommendation endpoint chooses a suitable exercise and explains its reason.

### Persistence and learner model

The API creates its tables at startup and seeds catalog exercises that are not already present. The `submissions` table retains the submitted code, execution status, per-test results, diagnosis evidence, duration, and hint level. The `mastery` table stores one estimate and attempt count for each concept. In the browser, unfinished editor code is saved per exercise in `localStorage`.

Mastery uses a small BKT-style update with an initial probability of `0.25`, learning probability `0.12`, guess probability `0.20`, and slip probability `0.10`. Each submission updates the concept estimate using whether all supplied tests passed. These values are prototype assumptions and are not calibrated to a classroom dataset.

The recommender prefers unattempted exercises whose prerequisites have an estimated mastery of at least `0.35`, then favors concepts with lower estimated mastery. If no unattempted exercise meets that prerequisite threshold, it falls back to another unattempted exercise; after all exercises have been attempted, it recommends from the full catalog. The API includes the reason with each recommendation.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/exercises` | Exercise catalog |
| GET | `/api/exercises/{id}` | Exercise details |
| POST | `/api/submissions` | Run, evaluate, diagnose, and save a submission |
| GET | `/api/attempts` | Recent attempt history |
| GET | `/api/attempts/{id}` | One saved attempt, including its code |
| POST | `/api/attempts/{id}/hints` | Get a hint or explicitly reveal the worked solution |
| GET | `/api/mastery` | Concept estimates |
| GET | `/api/concepts` | Prerequisite graph and concept estimates |
| GET | `/api/recommendation` | Next exercise and reason |
| GET | `/api/progress` | Summary and recent activity |

### Request examples

Submit a solution:

```json
{
  "exercise_id": "factorial",
  "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"
}
```

Request the next hint with `POST /api/attempts/{id}/hints`:

```json
{ "reveal_solution": false }
```

Reveal the worked solution only when the learner explicitly asks:

```json
{ "reveal_solution": true }
```

Submission status is one of `completed`, `syntax_error`, `runtime_error`, `timeout`, or `rejected`. If Docker or the runner image is unavailable, the API returns HTTP `503` rather than executing student code in the API process.

## Safety and prototype limits

- The runner fails closed if Docker cannot be invoked. AST parsing is for analysis, not a security boundary.
- The API runs on the host and invokes Docker CLI, so it does not need a persistent Docker socket mount in an API container. The runner containers are disposable and network-isolated.
- This local prototype has no user authentication. Add learner-scoped storage and authentication before deployment to multiple people.
- Tune diagnosis rules and BKT parameters against a documented curriculum and evaluation dataset before drawing conclusions about learner understanding.
- No benchmark, learning-gain, or user-study results are claimed.

## Configuration

Copy `.env.example` to `.env` and adjust these settings as needed:

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | Environment label; currently informational |
| `DATABASE_URL` | `sqlite:///./data/codemind.db` | SQLAlchemy database URL. Use PostgreSQL's URL below to switch databases. |
| `RUNNER_MODE` | `docker` | Must be `docker`; the API fails closed for other values. |
| `RUNNER_IMAGE` | `codemind-python-runner:latest` | Image built from `Dockerfile.runner`. |
| `RUNNER_TIMEOUT_SECONDS` | `4` | Per-submission execution time limit. |
| `MAX_SOURCE_BYTES` | `20000` | Maximum accepted source-code size. |
| `FRONTEND_ORIGINS` | `http://localhost:5173` | Comma-separated allowed browser origins for API CORS. |

For the Compose PostgreSQL service, use:

```env
DATABASE_URL=postgresql+psycopg://codemind:codemind-local@localhost:5432/codemind
```

The Compose database password defaults to `codemind-local` for local development. Change it before using the database outside a local machine.

## Build and checks

Build the production frontend bundle and run its TypeScript check:

```powershell
npm run build
```

Compile the Python files without starting the API:

```powershell
python -m compileall backend
```

There is currently no automated test suite in the repository. A successful frontend build and Python compilation do not establish diagnosis quality, runner security, or educational effectiveness.

## Troubleshooting

| Symptom | What to check |
|---|---|
| Docker Desktop is not running | Start Docker Desktop and confirm its Linux container engine is running. |
| Runner image is missing | Run `docker compose --profile build-only build runner-image` from the project root. |
| API returns HTTP 503 for submissions | Check Docker availability and the image name in `.env`. |
| Frontend cannot reach the API | Start `uvicorn backend.main:app --reload` and open `http://localhost:8000/api/health`. |
| Port 5173, 8000, or 5432 is busy | Stop the conflicting process or change the development port. |
| PostgreSQL connection fails | Confirm `docker compose up -d db`, `DATABASE_URL`, and `POSTGRES_PASSWORD` agree. SQLite works without PostgreSQL. |
| PowerShell blocks virtual-environment activation | Run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload` without activating it. |

For interactive route schemas, open [http://localhost:8000/docs](http://localhost:8000/docs) while the API is running.
