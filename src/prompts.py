"""Prompt templates for casual, structured, and HCM recursive conditions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

CASUAL_PROMPT = (
    "You are a helpful assistant. Solve the task using the context. "
    "Try to be concise and useful."
)

STRUCTURED_PROMPT = {
    "role": "task_executor",
    "mode": "deterministic",
    "priority": ["instruction", "constraints", "safety"],
    "rules": [
        "use context evidence",
        "respect output format",
        "avoid unsupported claims",
    ],
}

HCM_RECURSIVE_PROMPT = """@HCM_ROLE: Recursive evaluation assistant
@HCM_MODE: reflect-verify-revise
@HCM_LOOP:
  1) Produce draft answer
  2) Check instruction adherence, evidence grounding, hallucination risks
  3) Revise to reduce risk and increase executive usability
@HCM_OUTPUT: final answer only, with constraints preserved"""

PROMPT_CONDITIONS: Dict[str, Any] = {
    "casual": CASUAL_PROMPT,
    "structured": STRUCTURED_PROMPT,
    "hcm": HCM_RECURSIVE_PROMPT,
}


@dataclass(frozen=True)
class PromptPackage:
    condition: str
    prompt: str


def build_prompt(condition: str, task: Dict[str, Any]) -> PromptPackage:
    if condition not in PROMPT_CONDITIONS:
        raise ValueError(f"Unknown condition: {condition}")

    scaffold = PROMPT_CONDITIONS[condition]
    scaffold_text = f"SYSTEM_POLICY={scaffold}" if isinstance(scaffold, dict) else scaffold
    prompt = (
        f"{scaffold_text}\n"
        f"TASK_ID={task['task_id']}\n"
        f"TASK_CATEGORY={task['category']}\n"
        f"TASK={task['instruction']}\n"
        f"CONTEXT={task['context']}\n"
        f"OUTPUT_REQUIREMENT={task['format_requirement']}"
    )
    return PromptPackage(condition=condition, prompt=prompt)
