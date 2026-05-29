"""Automatic delegation module – always invokes Analyst and Strategist in parallel."""

import asyncio
import time
import config
from agents import query_market_analyst, query_trading_strategist
from request_context import add_log


async def auto_delegate(user_message: str) -> tuple[str, str]:
    """Always invoke Analyst and Strategist agents in parallel.

    Returns a tuple (analyst_json, strategist_json).
    On timeout or error, the failing agent returns an empty string so the
    Interface Agent can still respond with whatever data it has.
    """
    start = time.monotonic()
    add_log("Sistema", "Delegación", "Invocando Analista y Estratega en paralelo…", "pending")

    analyst_action = '{"action":"scan_market_top_opportunities"}'
    strategist_action = f'{{"action":"calculate_max_profit_strategy","context":"{user_message[:120]}"}}'

    async def _safe_analyst() -> str:
        try:
            return await query_market_analyst(analyst_action)
        except Exception as exc:
            add_log("Analista", "Sistema", f"Error: {exc}", "error")
            return ""

    async def _safe_strategist() -> str:
        try:
            return await query_trading_strategist(strategist_action)
        except Exception as exc:
            add_log("Estratega", "Sistema", f"Error: {exc}", "error")
            return ""

    try:
        analyst_output, strategist_output = await asyncio.wait_for(
            asyncio.gather(_safe_analyst(), _safe_strategist()),
            timeout=config.DELEGATION_TIMEOUT,
        )
    except asyncio.TimeoutError:
        add_log("Sistema", "Delegación", f"Timeout ({config.DELEGATION_TIMEOUT}s)", "error")
        analyst_output, strategist_output = "", ""

    elapsed = time.monotonic() - start
    add_log(
        "Sistema", "Delegación",
        f"Delegación paralela completada en {elapsed:.1f}s",
        "success" if (analyst_output or strategist_output) else "warning",
    )
    return analyst_output, strategist_output
