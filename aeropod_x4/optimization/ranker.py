from __future__ import annotations

from typing import Dict, List


def rank_designs(scored_designs: List[Dict[str, float]], top_n: int = 10) -> List[Dict[str, float]]:
    ordered = sorted(scored_designs, key=lambda x: x["score"], reverse=True)
    return ordered[:top_n]
