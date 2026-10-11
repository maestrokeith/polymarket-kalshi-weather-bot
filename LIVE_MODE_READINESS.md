# Safe paper-to-live mode switching

## Current behavior

- The dashboard reports the backend's effective mode via `GET /api/trading-mode`.
- The UI labels the paper mode explicitly and keeps the Live control locked.
- `SIMULATION_MODE=true` remains the required deployment setting.
- `LIVE_TRADING_ENABLED=false` is a second, fail-closed feature flag.
- Setting either environment variable incorrectly does not create a live executor. The scheduler intentionally refuses live trading while no verified executor exists.

## Requirements before unlocking Live

1. Implement supported official order submission for each enabled venue; do not reuse paper-trade database inserts as exchange execution.
2. Persist client order IDs and venue order IDs; make retries idempotent.
3. Reconcile accepted, partially filled, filled, cancelled, rejected, and unknown orders against venue state after every reconnect and restart.
4. Add per-order, per-market, daily-loss, total-exposure, and available-balance limits enforced server-side.
5. Validate minimum order sizes, tick sizes, fees, slippage, market status, and settlement rules per venue.
6. Keep live credentials in Render secret environment variables; never expose them to the frontend or logs.
7. Add operator authentication for every state-changing endpoint, CSRF/origin protections where relevant, and audit logs for mode changes.
8. Test with mocked venues and official sandbox/test environments where available; require explicit operator confirmation for the first live activation.
9. Start in read-only mode after every deployment/restart. A mode switch must stop new orders, reconcile open orders, verify account state, then change mode atomically.
10. Only then permit a live mode transition. If health checks, reconciliation, or risk checks fail, stay in paper mode and fail closed.

## Important

This repository does not yet contain a verified live order executor or complete real-fill reconciliation. The Live UI control is intentionally disabled. Do not set `SIMULATION_MODE=false` in production as a workaround.
