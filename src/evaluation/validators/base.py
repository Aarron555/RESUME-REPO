from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class Validator(ABC):
    @abstractmethod
    def validate(self, output: str, expected: Dict[str, Any]) -> bool:
        raise NotImplementedError
