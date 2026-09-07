# Navora Backend

Intelligent maritime freight decision-support platform for dry bulk (coal,
coking coal, iron ore) shipments from Australia / US / Mozambique / Russia /
Indonesia into Indian East Coast ports.

A single `POST /api/decision` call runs feasibility, forecasting, landed
cost, recommendation, market timing, risk, split-cargo, idle-vessel,
simulation, explainability, and audit — and returns one unified response the
frontend can render without doing any of its own calculations.

## Architecture

```
Frontend -> FastAPI -> Pydantic Schemas -> Application Service -> Input Guardrail
  -> DecisionOrchestrator -> [Feasibility, Forecast, LandedCost, Recommendation,
     MarketEntry, Risk, SplitCargo, IdleVessel, Simulation, Explainability]
  -> Output Guardrail -> DecisionResponse
```

Engines never call each other directly — the `DecisionOrchestrator` runs them
in order and passes a shared `ExecutionContext`. Feasibility, Forecast,
LandedCost, and Recommendation are **critical**: their failure aborts the
decision. The rest are non-critical — a failure there degrades the response
(`PARTIALLY_COMPLETED`) instead of breaking it.

It's a **modular monolith** — one FastAPI app, no Kafka/Redis/Celery/
microservices. See `backend/main.py` for the app, `core/orchestrator/` for
the workflow engine, and `core/engines/*` for the 10 intelligence engines.

## Prerequisites

- Python 3.11+
- MySQL 8.x (or any SQLAlchemy-compatible DB via `DATABASE_URL` — the test
  suite and dev verification in this repo use SQLite for convenience)
- `uv` (recommended) or `pip`

## Setup

```bash
cd backend
uv sync                      # or: pip install -r requirements.txt
cp .env.example .env         # edit DATABASE_URL / MYSQL_* / LLM_* as needed
```

### MySQL setup

```sql
CREATE DATABASE navora CHARACTER SET utf8mb4;
CREATE USER 'navora'@'%' IDENTIFIED BY 'navora';
GRANT ALL PRIVILEGES ON navora.* TO 'navora'@'%';
```

Set `DATABASE_URL=mysql+pymysql://navora:navora@localhost:3306/navora` in `.env`.

### Database migration

```bash
alembic upgrade head
```

### Data seeding

CSV fixtures live in `data/raw/` (ports, vessels, routes, commodities,
bunker prices, congestion, weather, market signals, Baltic indices).

```bash
python -m db.seed
```

### ML training (optional)

The forecast/risk/idle-vessel engines run on deterministic fallback logic by
default (`model_type: "fallback"` in responses) so the API works with zero
trained artifacts. To train real models, populate `ml/training/*.py` against
your historical data and drop the resulting joblib artifacts under
`ml/artifacts/<model>/` — `ml/registry.py` will then report them as
available and the engines' predictors are the seam to plug inference in.

### Running the backend

```bash
uvicorn main:app --reload
```

Docs at `http://localhost:8000/docs` and `/redoc`.

### Running tests

```bash
pytest
```

11 tests across unit (engines), integration (orchestrator), and API
(end-to-end `POST /api/decision`) layers — all pass against SQLite; the
same suite runs unchanged against MySQL by setting `DATABASE_URL`.

## Example DecisionRequest

```json
{
  "commodity": "Coking Coal",
  "cargo_quantity": 80000,
  "origin": "Australia",
  "destination": "Vizag",
  "earliest_loading_date": "2026-10-01",
  "latest_delivery_date": "2026-10-30",
  "contract_preference": "AUTO",
  "currency": "USD"
}
```

## Example DecisionResponse (abridged)

```json
{
  "request_id": "...",
  "status": "COMPLETED",
  "feasibility": {
    "feasible_vessels": ["Handysize", "Supramax", "Panamax"],
    "infeasible_vessels": [
      {"vessel_class": "Capesize", "reason": "Capesize rejected: destination draft limit (17.0m) is lower than vessel operating draft (18.2m)."}
    ],
    "port_compatible": true,
    "route_compatible": true
  },
  "recommendation": [
    {"vessel_class": "Panamax", "rank": 1, "score": 0.82, "is_feasible": true, "charter_strategy": "SPOT"}
  ],
  "market_entry": {"recommended_action": "MONITOR", "confidence": 0.55},
  "risks": [{"risk_type": "DELIVERY_WINDOW", "risk_level": "MEDIUM", "score": 0.386}],
  "split_cargo": {"recommended_option": "Option A - Single Vessel"},
  "engine_statuses": [{"engine": "FeasibilityEngine", "state": "COMPLETED", "duration_ms": 0.04}]
}
```

## API endpoints

```
GET  /health
GET  /health/db
POST /api/decision
GET  /api/decision/{id}
GET  /api/forecast/{decision_id}
GET  /api/recommendation/{decision_id}
GET  /api/risk/{decision_id}
GET  /api/market-entry/{decision_id}
GET  /api/split-cargo/{decision_id}
GET  /api/idle-vessel/{decision_id}
POST /api/simulation
POST /api/assistant/chat
GET  /api/market/brief
GET  /api/market/signals
```

## Ops Assistant

`POST /api/assistant/chat` answers questions like "why was Capesize
rejected?", "what is the best vessel?", "why should I book now?", "what
happens if freight rises 15%?" by calling the same backend tools the API
exposes (`core/agents/ops_assistant/tools.py`) — never inventing numbers.
When `LLM_API_KEY` is unset (`LLM_PROVIDER=none`), a deterministic keyword
router picks the right tool; the seam for swapping in a real LangGraph
tool-calling loop is `core/agents/ops_assistant/graph.py`.

## Guardrails

`core/guardrails/input_guard.py` validates commodity/origin/destination/
dates/quantity/contract preference before any engine runs.
`core/guardrails/output_guard.py` checks for negative costs, invalid
confidence/risk values, and infeasible-but-ranked recommendations before the
response is returned. NeMo Guardrails config files are stubbed under
`core/guardrails/config/` (`config.yml`, `rails.co`, `prompts.yml`) — wire in
the `nemoguardrails` package there if you need LLM-facing rail enforcement;
the deterministic guardrails above already enforce business rules regardless.

## Design notes / simplifications made for this MVP

- **Financial single source of truth**: `Recommendation` stores only
  `landed_cost_id`, never duplicated cost fields — see `models/recommendation.py`.
- **Fallback-first**: every ML-ish engine (`forecast`, `risk`, `idle_vessel`)
  has a deterministic, clearly-labeled fallback (`model_type: "fallback"`)
  so the app runs with zero trained artifacts, zero LLM key, and zero
  external market API.
- **Agents**: LangChain/LangGraph are declared as dependencies and the
  agent modules are structured as graphs (`core/agents/*/graph.py`), but the
  actual graph execution in this MVP is a plain deterministic pipeline so
  behavior is identical with or without an LLM key configured. This is the
  intended extension point, not a placeholder to be embarrassed about —
  wire an LLM call into `run_market_research_graph` /
  `route_and_answer` when you have a provider configured.
- `xgboost`/`lightgbm`/`langchain`/`langgraph` are declared in
  `pyproject.toml`/`requirements.txt` per the frozen stack, but the verified
  end-to-end run in this environment used only the deterministic fallback
  paths (no GPU/heavy deps needed to prove the pipeline). Install them before
  running `ml/training/*.py`.

## Troubleshooting

- **`alembic upgrade head` fails to connect**: check `DATABASE_URL` in `.env`
  and that MySQL is reachable; the migration itself is DB-agnostic and was
  verified against SQLite in this repo's test run.
- **All vessel classes infeasible**: check `config/constants.py` `PORT_SPECS`
  / `VESSEL_SPECS` against your seeded `Port`/`Vessel` rows — the feasibility
  engine currently reads from these constants, not from the DB rows, as an
  MVP simplification; swapping in live DB lookups is a small change in
  `core/engines/feasibility/engine.py`.
- **`GuardrailViolation` on a request that looks fine**: check
  `config/constants.py` `COMMODITIES`/`ORIGINS`/`DESTINATIONS` — the input
  guardrail only accepts the enumerated values from the spec.
