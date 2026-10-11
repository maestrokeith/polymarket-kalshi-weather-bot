# Security and Trading Audit — 2026-10-12

Repository reviewed: `maestrokeith/polymarket-kalshi-weather-bot`
Scope: source-level review of configuration, FastAPI startup, scheduler trade path, database models, Kalshi client, and deployment settings. This was not a full local build, dependency scan, or live exchange test.

## Executive summary

**Status: NOT READY for real-money trading or an internet-exposed deployment.** The current code path appears to create local database trade records rather than submit and reconcile exchange orders. Treat displayed trades and P&L as simulated/internal bookkeeping, not evidence of live fills or profitability.

## Findings

### Critical — no live order execution in the inspected BTC scheduler path
**Evidence:** `backend/core/scheduler.py` constructs a `Trade` ORM row and commits it; the inspected path contains no Polymarket order submission, exchange acknowledgement, fill polling, or order-ID persistence. It logs “Executed” after recording the row. Do not interpret this as a live execution.

**Fix:** implement a dedicated execution adapter using the official venue SDKs, with explicit simulation/live separation, order IDs, idempotency, fill reconciliation, partial-fill handling, cancel/replace logic, and startup reconciliation before enabling live mode.

### High — unauthenticated operational API risk
**Evidence:** `backend/api/main.py` exposes a FastAPI control/dashboard API. The inspected application config has permissive CORS (`allow_origins=["*"]`). The repository documents control endpoints including bot start/stop/reset. No authentication or authorization layer was visible in the inspected routes.

**Impact:** if control endpoints are reachable on a public deployment, an arbitrary caller may be able to inspect data or manipulate bot state. CORS is not authentication.

**Fix:** require authenticated access for every non-public endpoint; restrict origins to the actual dashboard origin; protect WebSocket access; rate-limit and audit control actions; do not expose administrative APIs publicly until secured.

### High — startup automatically marks the bot as running
**Evidence:** startup in `backend/api/main.py` sets an existing `BotState.is_running = True` and creates a new state with `is_running=True`.

**Impact:** an operator's pause may not survive a restart. This is especially unsafe if future live execution is added.

**Fix:** default to paused on startup; persist a deliberate operator-approved state; require a separate explicit live-mode arming step after risk checks.

### High — documented risk settings are not proof of enforced live risk controls
The configuration includes `SIMULATION_MODE`, a daily loss limit, and trade caps, but the inspected scheduler path only writes local trade records and does not demonstrate venue-side enforcement. Risk limits must be enforced at the execution boundary and account for open orders, partial fills, fees, slippage, and positions held outside this process.

**Fix:** centralize pre-trade risk checks; fail closed on missing/stale balances or market data; enforce daily loss, per-market and aggregate exposure, max order size, price collars, stale-signal limits, and a kill switch before every order.

### Medium — deployment persistence and process lifecycle need verification
The deployment configuration uses `python run.py` and an application health endpoint. The database defaults to local SQLite. On ephemeral hosting, local SQLite data may be lost across restarts or instances unless persistent storage is configured. Multiple replicas can also run duplicate schedulers unless leadership/locking is implemented.

**Fix:** use managed PostgreSQL for production, run one scheduler/worker or add a distributed lock, configure persistent storage where appropriate, and test restart recovery.

### Medium — weather probabilities and market semantics need validation
The weather model estimates threshold probabilities from ensemble members and Kalshi market parsing maps ticker suffixes to above/below directions. That is a useful signal prototype, but it does not itself validate each venue's exact settlement rules, inclusivity of threshold boundaries, station, local date/time, or the currently active contract schema.

**Fix:** add fixture-based tests from official contract rules for every supported city/market type; test boundary temperatures, timezone/date transitions, missing members, stale forecasts, and market-price units.

### Medium — no test/build evidence in this review
This was a source inspection via repository files; tests, dependency vulnerability scans, and full backend/frontend builds were not run in an isolated checkout.

**Fix:** add automated unit/integration tests and CI for linting, type checking, API authorization, settlement, risk limits, and simulated end-to-end scans. Pin and regularly audit dependencies.

## Before deployment checklist

- [ ] Keep `SIMULATION_MODE=true`; do not add real funds or production trading credentials yet.
- [ ] Add authentication/authorization and restrictive CORS.
- [ ] Ensure startup is paused by default and a kill switch is tested.
- [ ] Prove paper-trade settlement and P&L against known fixtures.
- [ ] Add venue order execution only after order/fill reconciliation tests pass.
- [ ] Add idempotency, duplicate-order prevention, restart recovery, and persistent storage.
- [ ] Add unit tests for fees, slippage, position sizing, daily loss, and aggregate exposure.
- [ ] Run dependency and secret scans; ensure `.env`, private keys, and credentials never enter Git.
- [ ] Run in paper mode for an extended period and evaluate out-of-sample performance. No strategy profitability is established by this audit.

## Files inspected

- `README.md`
- `requirements.txt`
- `.env.example`
- `.gitignore`
- `backend/config.py`
- `backend/api/main.py`
- `backend/core/scheduler.py`
- `backend/data/kalshi_client.py`
- `backend/data/kalshi_markets.py`
- `backend/data/weather.py`
- `backend/models/database.py`
- `railway.json`
