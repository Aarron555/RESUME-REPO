from __future__ import annotations

import json
from typing import Any, Dict

from .base import Validator


TYPE_MAP = {
    "str": str,
    "float": (int, float),
    "int": int,
    "bool": bool,
    "list": list,
    "dict": dict,
}


class FormatValidator(Validator):
    def validate(self, output: str, expected: Dict[str, Any]) -> bool:
        schema = expected.get("schema", {})
        try:
            payload = json.loads(output)
        except json.JSONDecodeError:
            return False

        for key, type_name in schema.items():
            if key not in payload:
                return False
            py_type = TYPE_MAP.get(type_name)
            if py_type is None:
                return False
            if not isinstance(payload[key], py_type):
                return False
        return True
