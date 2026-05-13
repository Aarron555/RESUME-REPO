from __future__ import annotations

from .base import Validator
from .code_validator import CodeValidator
from .format_validator import FormatValidator
from .math_validator import MathValidator
from .semantic_validator import SemanticValidator


def get_validator(validation_type: str) -> Validator:
    mapping = {
        "math": MathValidator(),
        "code": CodeValidator(),
        "format": FormatValidator(),
        "semantic": SemanticValidator(),
    }
    if validation_type not in mapping:
        raise ValueError(f"Unknown validation type: {validation_type}")
    return mapping[validation_type]


__all__ = [
    "Validator",
    "MathValidator",
    "CodeValidator",
    "FormatValidator",
    "SemanticValidator",
    "get_validator",
]
