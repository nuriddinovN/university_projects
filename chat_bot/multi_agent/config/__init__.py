# Convenience re-exports (optional, but keeps imports tidy in agent.py)
from .models import get_openrouter_litellm, get_gemini_model_id
from .personas import (
    OPENROUTER_DEBATER_INSTRUCTION,
    GEMINI_DEBATER_INSTRUCTION,
    COORDINATOR_INSTRUCTION,
)
