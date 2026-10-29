# Code Matrix

Code Matrix is a local coding practice workspace for Python, Java, C, HTML, CSS, and JavaScript. It checks submissions against exercise criteria, gives feedback and progressive hints, saves attempts, estimates concept mastery, and recommends what to try next.

This repository is a complete local prototype. The learning model and diagnosis rules are inspectable heuristics, not evidence of educational effectiveness. It currently uses a single local learner profile and does not include account management or classroom administration. The source folder and internal database/runner identifiers may retain the legacy `codemind` name for compatibility; the product name shown to users is Code Matrix.

## Contents

- [Features](#included)
- [Technology stack](#technology-stack)
- [Project layout](#project-layout)
- [Quick start](#start-the-application-on-windows)
- [Architecture and submission flow](#architecture)
- [Configuration](#configuration)
- [API reference](#api)
- [Build and checks](#build-and-checks)
- [Team workflow](#team-workflow)
- [DevOps deployment](#devops-deployment-render)
- [Troubleshooting](#troubleshooting)
- [Security and current limitations](#safety-and-prototype-limits)

## Included

- React + TypeScript dashboard and practice studio with Monaco Editor.
- FastAPI API for exercises, submissions, hints, attempt history, mastery estimates, progress, and recommendations.
- 33 console coding problems, including 21 categorized DSA questions and programming fundamentals. Every console problem can be solved in C, Python, or Java, with separate saved drafts and the same judge cases across languages.
- Problem categories include Arrays & Hashing, Two Pointers, Stack, Binary Search, Sliding Window, Dynamic Programming, Graphs, Strings, Math & Logic, Recursion & DP, Input & Arithmetic, and Loops and Accumulation. Each category has multiple exercises.
- Six multi-file HTML/CSS/JavaScript projects live in a separate UI Studio, with a live preview and browser checks. Code Studio contains only C/Python/Java console exercises.
- Separate Python, Java, and C compiler/runtime images; choose the language from the editor on every console problem. Each studio has its own category-filtered problem list.
- AST-based structural observations and explainable diagnosis rules. Diagnoses are possibilities, not claims about student intent.
- Progressive conceptual and structural hints; a worked solution is returned only on explicit request.
- BKT-style per-concept estimates and concept prerequisite foundations.
- PostgreSQL for Docker Compose and SQLite for simple local API development.
- Disposable Docker execution containers for Python, Java, and C with no network, read-only root filesystems, CPU, memory, process, and time limits, and read-only submission mounts. Student code never runs in the FastAPI process.
- A browser preview inside an iframe sandbox with a restrictive Content Security Policy. Browser checks run in that frame and are useful for local practice feedback.

## Technology stack

| Area | Technology | Role |
|---|---|---|
| Web application | React, TypeScript, Vite | Dashboard, practice flow, progress, and history views |
| Code editor | Monaco Editor | Python, Java, C, HTML, CSS, and JavaScript editing |
| UI icons and styles | Lucide React, CSS | Interface icons and responsive layout |
| API | Python 3.11+, FastAPI, Pydantic | HTTP API, request validation, and orchestration |
| Code inspection | Python `ast` | Structural facts that support diagnosis rules |
| Code execution | Docker runner images | Isolated Python, Java, and C compilation/execution |
| Web preview | Sandboxed browser iframe | Multi-file HTML/CSS/JavaScript preview and client-side checks |
| Persistence | SQLite or PostgreSQL | Exercises, submissions, test results, and mastery estimates |
| Data access | SQLAlchemy | Database models and queries |

Frontend dependency versions are recorded in `package-lock.json`; backend dependency ranges are in `requirements.txt`. Explanations currently use deterministic templates, so no LLM API key is required.

## Project layout

```text
CODEMIND_AI/
├── backend/
│   ├── catalog.py       # Seed exercises and expected test cases
│   ├── dsa_catalog.py   # Shared categorized DSA problems and language starters/solutions
│   ├── extended_dsa.py  # Additional problems across the DSA categories
│   ├── multilang_fundamentals.py # Shared C/Python/Java fundamentals and console exercises
│   ├── ui_catalog.py    # HTML/CSS/JavaScript practice projects and browser checks
│   ├── db.py            # SQLite/PostgreSQL connection setup
│   ├── main.py          # FastAPI routes and startup
│   ├── models.py        # Exercise, submission, and mastery tables
│   ├── runner.py        # Docker invocation for Python, Java, and C
│   ├── stdio_runner.py  # Python/Java/C compiler and stdin/stdout test harness
│   ├── schemas.py       # Validated API request models
│   └── tutor.py         # AST facts, diagnoses, hints, and BKT updates
├── src/
│   ├── App.tsx          # Screens and API interactions
│   ├── styles.css       # Responsive interface styles
│   ├── types.ts         # Frontend data types
│   ├── main.tsx         # React entry point
│   └── vite-env.d.ts    # Vite TypeScript definitions
├── Dockerfile.runner    # Disposable Python execution image
├── Dockerfile.runner-java # Java compiler/runtime image
├── Dockerfile.runner-c  # C compiler/runtime image
├── docker-compose.yml   # Optional PostgreSQL and runner-image build targets
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

2. Build all language runner images (the first build downloads base images and compilers and may take a few minutes):

   ```powershell
   docker compose --profile build-only build runner-image java-runner c-runner
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

![Intelligent Coding Tutor Architecture Flowchart](assets\architecture.png)


The explanation service uses deterministic, evidence-backed templates. This keeps the prototype useful without an LLM key and avoids delegating correctness decisions to a language model. An LLM can be added later as a phrasing layer grounded in diagnoses and trusted teaching material.

### Submission flow

1. The student opens an exercise and edits the relevant source file(s) in Monaco.
2. Code Studio sends the exercise ID, selected C/Python/Java language, and code to `POST /api/submissions`. UI Studio sends its HTML/CSS/JavaScript files and browser-check outcomes.
3. Console submissions include the selected language and run as stdin/stdout programs against the problem's shared test cases. Java and C submissions are compiled inside their language-specific runner images.
4. Docker runs Python, Java, or C work in a disposable network-isolated container with a read-only root filesystem, capped CPU/memory/processes, bounded output, and execution time limits.
5. The runner returns per-test outcomes; the tutor combines them with language-appropriate exercise context and, for Python, AST observations.
6. UI Studio projects render in an iframe with `sandbox="allow-scripts"` and a restrictive CSP. Browser checks inspect DOM text, selectors, computed styles, and interactions. Results are submitted for learning feedback.
7. The API stores the attempt and updates the learner's concept estimate.
8. The recommendation endpoint chooses a suitable exercise and explains its reason.

### Persistence and learner model

The API creates its tables at startup, adds the language/multi-file columns to an existing local database, and synchronizes exercise definitions with the current catalog. Existing submissions and mastery records are retained. The `submissions` table retains the submitted code, chosen language, web files when applicable, execution status, per-test results, diagnosis evidence, duration, and hint level. The `mastery` table stores one estimate and attempt count for each concept. In the browser, unfinished editor code/files are saved per exercise and language in `localStorage`.

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
  "language": "python",
  "code": "n = int(input())\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\nprint(factorial(n))"
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

For any console problem, include the selected language as `c`, `python`, or `java`; it is saved with the attempt. Example:

```json
{
  "exercise_id": "dsa-two-sum",
  "language": "java",
  "code": "import java.util.*;\npublic class Main { public static void main(String[] args) { ... } }"
}
```

Submission status can include `completed`, `syntax_error`, `compile_error`, `runtime_error`, `timeout`, or `rejected`. If Docker or the required runner image is unavailable, the API returns HTTP `503` rather than executing student code in the API process. Web check outcomes are produced in the learner's browser; they are not a trusted grading service and should not be used for high-stakes assessment.

## Safety and prototype limits

- The runner fails closed if Docker cannot be invoked. AST parsing is for analysis, not a security boundary.
- The API runs on the host and invokes Docker CLI, so it does not need a persistent Docker socket mount in an API container. The runner containers are disposable and network-isolated.
- Web preview code is untrusted and runs in a sandboxed iframe with network access blocked by CSP. Browser-based test results are client-reported practice feedback. The current web workspace is a static frontend project; it does not provide a user-controlled backend server or database for each web exercise.
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
| `JAVA_RUNNER_IMAGE` | `codemind-java-runner:latest` | Java image built from `Dockerfile.runner-java`. |
| `C_RUNNER_IMAGE` | `codemind-c-runner:latest` | C image built from `Dockerfile.runner-c`. |
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

## Team workflow

Follow the branch naming, commit, pull-request, review, and merge process in [CONTRIBUTING.md](CONTRIBUTING.md). Work on a short-lived feature/fix/docs branch, target `main` with a pull request, wait for CI and one teammate's approval, and resolve review threads before merging. Configure GitHub branch protection for `main` to require the `frontend`, `backend`, and `containers` checks and one approval; repository settings cannot be managed by a committed file alone.

## DevOps deployment (Render)

The repository includes a GitHub Actions workflow at `.github/workflows/ci.yml`, production container definitions for the API and frontend, and a Render Blueprint at `render.yaml`. Connect the GitHub repository to Render and create a Blueprint deployment from that file. Review the selected plans and current prices in Render before creating managed services. The Blueprint creates a PostgreSQL database, a private FastAPI service, and a public Nginx frontend; the frontend proxies `/api` to the private API using Render's private host-and-port reference. The database URL is injected by Render, and the API listens on Render's `PORT`.

**Execution limitation:** the local judge starts a new Docker container for every student submission and applies network isolation, read-only filesystems, and resource limits. The Render Blueprint deliberately sets `RUNNER_MODE=unavailable`; execution endpoints fail closed with a clear service error rather than running student code inside the API. Thus the web application can be deployed, but code judging is disabled until a separately hosted isolated runner with an authenticated API is implemented and connected. Do not enable direct execution in the API process or expose a Docker socket to the public web service.

### Local container smoke test

```powershell
docker build -f Dockerfile.api -t codematrix-api:local .
docker build -f Dockerfile.web -t codematrix-web:local .
```

### CI and release flow

Every push or pull request to `main` or `master` runs the frontend production build, npm dependency audit, Python compilation/import check, Python dependency audit, and API/frontend container builds. Configure the repository to require these checks before merging. After merging, Render deploys the connected Blueprint services from the repository. Review Render deployment logs and `/api/health` after each release. The current project does not include a staging environment or automated rollback policy.

### Remaining production work

- Implement and threat-model a separate execution service capable of safely running untrusted Python, Java, and C code. Require authenticated service-to-service requests, quotas, strict resource/time limits, no network access for workloads, and cleanup. Then add a `RUNNER_MODE` integration for that service.
- Verify the private service reference and frontend hostname in the deployed Render environment.
- Add a staging environment, end-to-end smoke tests, and a tested rollback procedure.
- Configure branch protection to require CI checks and review; repository settings are managed on GitHub and are not changed by this file.
- Complete the rubric's Coursera certification and retain the certificate separately; it is not a software deployment task.

## Troubleshooting

| Symptom | What to check |
|---|---|
| Docker Desktop is not running | Start Docker Desktop and confirm its Linux container engine is running. |
| Runner image is missing | Run `docker compose --profile build-only build runner-image java-runner c-runner` from the project root. |
| API returns HTTP 503 for submissions | Check Docker availability and the image name in `.env`. |
| Frontend cannot reach the API | Start `uvicorn backend.main:app --reload` and open `http://localhost:8000/api/health`. |
| Port 5173, 8000, or 5432 is busy | Stop the conflicting process or change the development port. |
| PostgreSQL connection fails | Confirm `docker compose up -d db`, `DATABASE_URL`, and `POSTGRES_PASSWORD` agree. SQLite works without PostgreSQL. |
| PowerShell blocks virtual-environment activation | Run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload` without activating it. |

For interactive route schemas, open [http://localhost:8000/docs](http://localhost:8000/docs) while the API is running.
