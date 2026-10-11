"""Trading mode readiness and release gates.

Live mode must remain disabled until an exchange executor, durable order/fill
reconciliation, idempotency, and end-to-end sandbox tests have been implemented.
A dashboard control must never bypass these server-side gates.
"""

from fastapi import APIRouter
from backend.config import settings

router = APIRouter()


@router.get("/api/trading-mode")
async def get_trading_mode():
    """Report the effective mode and whether live trading is eligible."""
    live_enabled = bool(getattr(settings, "LIVE_TRADING_ENABLED", False))
    executor_verified = False  # Deliberately false until a verified executor exists.
    live_available = live_enabled and executor_verified and not settings.SIMULATION_MODE
    return {
        "mode": "paper" if settings.SIMULATION_MODE else "live_blocked",
        "simulation_mode": settings.SIMULATION_MODE,
        "live_available": live_available,
        "live_enabled_by_operator": live_enabled,
        "executor_verified": executor_verified,
        "message": (
            "Paper trading is active."
            if settings.SIMULATION_MODE
            else "Live mode is blocked: no verified live order executor is installed."
        ),
    }
