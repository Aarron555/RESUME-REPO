from __future__ import annotations

from typing import Any, Dict

from .base import Validator


class CodeValidator(Validator):
    def validate(self, output: str, expected: Dict[str, Any]) -> bool:
        tests = expected.get("tests", [])
        for test in tests:
            env = dict(test.get("env", {}))
            expected_value = test.get("expected")
            try:
                if "\n" in output:
                    local_scope = dict(env)
                    exec(output, {"__builtins__": {}}, local_scope)
                    candidate = local_scope.get(test.get("result_var", "result"))
                else:
                    candidate = eval(output, {"__builtins__": {}}, env)
            except Exception:
                return False

            if candidate != expected_value:
                return False

        return True
