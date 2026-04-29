"""Iteration simulation engine for retry-loop evaluation."""

from __future__ import annotations

from typing import Any, Dict

from src.evaluation.validators import Validator


def _token_count(text: str) -> int:
    return len(text.split())


def refine_prompt(prompt: str, previous_output: str) -> str:
    return (
        f"{prompt}\n"
        "\nRETRY_INSTRUCTION: Previous output was invalid. "
        "Fix format/content and return only valid output.\n"
        f"PREVIOUS_OUTPUT={previous_output}"
    )


def run_iteration_loop(
    *,
    model_client,
    prompt: str,
    validator: Validator,
    expected: Dict[str, Any],
    generation_config: Dict[str, Any],
    max_attempts: int = 3,
) -> Dict[str, Any]:
    attempts = []
    current_prompt = prompt

    for attempt_idx in range(1, max_attempts + 1):
        output = model_client.generate(current_prompt, {**generation_config, "attempt": attempt_idx})
        is_correct = validator.validate(output, expected)

        attempts.append(
            {
                "attempt": attempt_idx,
                "prompt": current_prompt,
                "output": output,
                "is_correct": is_correct,
                "input_tokens": _token_count(current_prompt),
                "output_tokens": _token_count(output),
            }
        )

        if is_correct:
            break
        current_prompt = refine_prompt(current_prompt, output)

    success = any(a["is_correct"] for a in attempts)
    attempts_to_success = next((a["attempt"] for a in attempts if a["is_correct"]), max_attempts)

    return {
        "success": success,
        "attempts_to_success": attempts_to_success,
        "failed_attempts": sum(1 for a in attempts if not a["is_correct"]),
        "final_output": attempts[-1]["output"],
        "attempt_logs": attempts,
        "total_input_tokens": sum(a["input_tokens"] for a in attempts),
        "total_output_tokens": sum(a["output_tokens"] for a in attempts),
        "is_correct": success,
    }
