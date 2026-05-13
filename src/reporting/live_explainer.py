"""Live interpretability output formatter for AXE-LAB v4."""

from __future__ import annotations

from typing import Any, Dict, List


def _interpret(success_rate: float, avg_attempts: float, failure_rate: float, cost_per_success: float) -> str:
    if success_rate >= 0.9 and avg_attempts <= 1.3:
        return "High correctness with minimal retry loops; behavior is stable and production-ready."
    if failure_rate > 0.4:
        return "Frequent failures persist across retries, indicating brittle behavior under this prompt/model pairing."
    if cost_per_success > 0.001:
        return "Correctness may be acceptable, but economic efficiency is weak due to token-heavy recovery cycles."
    return "Mixed reliability: retries partially recover failures but stability is not consistent."


def _translation(success_rate: float, cost_per_success: float, avg_attempts: float) -> str:
    return (
        f"At current performance, this setup delivers {success_rate:.2%} successful runs, "
        f"requires ~{avg_attempts:.2f} attempts per success, and costs ${cost_per_success:.6f} per success. "
        "Use this to estimate deployment cost and latency trade-offs."
    )


def render_live_readout_v4(
    *,
    model: str,
    system: str,
    task: str,
    success_rate: float,
    avg_attempts: float,
    cost_per_success: float,
    failure_rate: float,
    failure_tags: List[str],
) -> str:
    return "\n".join(
        [
            "==============================",
            "AXE-LAB LIVE READOUT (v4)",
            "==============================",
            f"MODEL: {model}",
            f"SYSTEM: {system}",
            f"TASK: {task}",
            "",
            f"SUCCESS RATE: {success_rate:.4f}",
            f"AVG ATTEMPTS: {avg_attempts:.4f}",
            f"COST/SUCCESS: ${cost_per_success:.8f}",
            f"FAILURE RATE: {failure_rate:.4f}",
            "",
            "FAILURE TAGS:",
            f"{failure_tags if failure_tags else '[]'}",
            "",
            "INTERPRETATION:",
            _interpret(success_rate, avg_attempts, failure_rate, cost_per_success),
            "",
            "TRANSLATION:",
            _translation(success_rate, cost_per_success, avg_attempts),
        ]
    )
