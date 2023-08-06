import os

from vellum.api_resources import Generate
from vellum.api_resources.completion_actuals import SubmitCompletionActuals
from vellum.api_resources.types import CompletionActual, GenerateRequest

api_key = os.environ.get("VELLUM_API_KEY")

__all__ = [
    "Generate",
    "GenerateRequest",
    "SubmitCompletionActuals",
    "CompletionActual",
    "api_key",
]
