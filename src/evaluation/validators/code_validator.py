from __future__ import annotations

from typing import Any, Dict

from .base import Validator


class CodeValidator(Validator):
    """Validate small Python transformation outputs against expected fixtures.

    The validator intentionally runs with disabled builtins and controlled inputs.
    It supports expression-style answers such as list comprehensions and small
    statement-style answers that assign to a result variable.
    """

    def validate(self, output: str, expected: Dict[str, Any]) -> bool:
        tests = expected.get("tests", [])
        for test in tests:
            env = dict(test.get("env", {}))
            expected_value = test.get("expected")
            result_var = test.get("result_var", "result")
            safe_globals = {"__builtins__": {}, **env}
            local_scope = dict(env)

            try:
                if "\n" in output:
                    exec(output, safe_globals, local_scope)
                    candidate = local_scope.get(result_var)
                else:
                    candidate = eval(output, safe_globals, local_scope)
            except Exception:
                return False

            if candidate != expected_value:
                return False

        return True
