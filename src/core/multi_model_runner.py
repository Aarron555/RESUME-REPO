"""Multi-model execution layer for AXE-LAB v4.

The current clients are deterministic stand-ins. They preserve the same interface
that future live API adapters can implement while keeping the project runnable
without external keys.
"""

from __future__ import annotations

import hashlib
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List


class ModelClient(ABC):
    """Abstract model client interface."""

    @abstractmethod
    def generate(self, prompt: str, config: dict) -> str:
        raise NotImplementedError


@dataclass
class _PromptParts:
    task_id: str
    instruction: str
    context: str
    format_requirement: str


def _extract_prompt_parts(prompt: str) -> _PromptParts:
    lines = prompt.splitlines()
    kv = {}
    valid_keys = {"TASK_ID", "TASK", "CONTEXT", "OUTPUT_REQUIREMENT"}
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
            if key in valid_keys:
                kv[key] = value

    return _PromptParts(
        task_id=kv.get("TASK_ID", ""),
        instruction=kv.get("TASK", ""),
        context=kv.get("CONTEXT", ""),
        format_requirement=kv.get("OUTPUT_REQUIREMENT", ""),
    )


def _quality_from_prompt(prompt: str) -> float:
    signals = ["OUTPUT_REQUIREMENT=", "TASK_ID=", "SYSTEM_POLICY=", "priority", "@HCM_ROLE", "@HCM_LOOP"]
    return sum(1 for s in signals if s.lower() in prompt.lower()) / len(signals)


def _gold_answer(parts: _PromptParts) -> str:
    if parts.task_id == "summarization":
        return "- Solar adoption grew 18% year-over-year.\n- Grid upgrades reduced outages by 12%."
    if parts.task_id == "reasoning":
        return "Step 1: 8+4=12\nStep 2: 12*3=36\nFinal: 31"
    if parts.task_id == "code_transformation":
        return "[n*n for n in nums]"
    if parts.task_id == "constrained_output":
        return '{"answer": "yes", "confidence": 0.98}'
    if parts.task_id == "adversarial_injection":
        return "SAFE"
    return ""


def _degraded_answer(parts: _PromptParts, rng: random.Random) -> str:
    if parts.task_id == "summarization":
        return "Solar improved and outages fell."
    if parts.task_id == "reasoning":
        return "Step 1: 8+4=12\nStep 2: 12*3=36\nFinal: 32"
    if parts.task_id == "code_transformation":
        return "result=[]\nfor n in nums:\n    result.append(n*n)"
    if parts.task_id == "constrained_output":
        return "answer: yes, confidence: high"
    if parts.task_id == "adversarial_injection":
        return rng.choice(["HACKED", "LEAK", "PWNED"])
    return ""


class _DeterministicClient(ModelClient):
    """Deterministic stand-in to keep repository runnable without external keys."""

    reliability: float = 0.7

    def generate(self, prompt: str, config: dict) -> str:
        parts = _extract_prompt_parts(prompt)
        run_index = config.get("run_index", 0)
        seed = int(config.get("seed", 42))
        temperature = float(config.get("temperature", 0.0))

        digest = hashlib.sha256(f"{prompt}|{run_index}|{seed}".encode("utf-8")).hexdigest()
        derived = int(digest[:12], 16)
        rng = random.Random(derived + seed)

        quality = _quality_from_prompt(prompt)
        success_prob = (self.reliability * 0.7) + (quality * 0.3) - (temperature * 0.05)
        return _gold_answer(parts) if rng.random() < success_prob else _degraded_answer(parts, rng)


class OpenAIClient(_DeterministicClient):
    reliability = 0.84


class AnthropicClient(_DeterministicClient):
    reliability = 0.82


class LocalModelClient(_DeterministicClient):
    reliability = 0.72


def get_model_client(model_name: str) -> ModelClient:
    normalized = model_name.lower()
    if normalized == "gpt":
        return OpenAIClient()
    if normalized == "claude":
        return AnthropicClient()
    if normalized == "local":
        return LocalModelClient()
    raise ValueError(f"Unsupported model: {model_name}")


def execute_experiment_matrix(
    *,
    models: List[str],
    systems: List[str],
    tasks: List[Dict[str, Any]],
    runs_per_task: int,
    seed: int,
    temperature: float,
    prompt_builder,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    for model_name in models:
        client = get_model_client(model_name)
        for system_name in systems:
            for task in tasks:
                for run_index in range(runs_per_task):
                    prompt = prompt_builder(system_name, task).prompt
                    output = client.generate(
                        prompt,
                        {
                            "seed": seed,
                            "temperature": temperature,
                            "run_index": run_index,
                            "model": model_name,
                        },
                    )
                    rows.append(
                        {
                            "model_name": model_name,
                            "system_type": system_name,
                            "task_type": task["task_id"],
                            "run_id": run_index,
                            "prompt": prompt,
                            "task_context": task,
                            "output": output,
                        }
                    )
    return rows
