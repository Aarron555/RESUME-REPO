from __future__ import annotations

import re
from typing import Any, Dict, Optional

from .base import Validator


class MathValidator(Validator):
    def _extract_number(self, output: str) -> Optional[float]:
        nums = re.findall(r"-?\d+(?:\.\d+)?", output)
        if not nums:
            return None
        return float(nums[-1])

    def validate(self, output: str, expected: Dict[str, Any]) -> bool:
        target = expected.get("value")
        if target is None:
            return False
        pred = self._extract_number(output)
        return pred is not None and float(target) == pred
