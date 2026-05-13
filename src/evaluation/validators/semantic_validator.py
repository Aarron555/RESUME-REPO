from __future__ import annotations

from typing import Any, Dict, List

from .base import Validator


class SemanticValidator(Validator):
    def validate(self, output: str, expected: Dict[str, Any]) -> bool:
        text = output.lower()

        exact = expected.get("exact_match")
        if exact is not None:
            return output.strip() == str(exact)

        keywords: List[str] = [k.lower() for k in expected.get("keywords", [])]
        if not keywords:
            return False

        hits = sum(1 for k in keywords if k in text)
        threshold = float(expected.get("min_overlap", 0.5))
        return (hits / len(keywords)) >= threshold
