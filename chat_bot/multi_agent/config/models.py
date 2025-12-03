import os

from google.adk.models.lite_llm import LiteLlm

# Default model IDs are taken from the official docs:
# - Gemini: "gemini-2.0-flash" (Models & Authentication page)
# - OpenRouter: "openrouter/openai/gpt-4" (OpenRouter provider examples via LiteLLM)
#
# You can override these using environment variables if you want.
#
# For OpenRouter, LiteLLM expects:
#   OPENROUTER_API_KEY=your_key
#   (optional) OPENROUTER_API_BASE=https://openrouter.ai/api/v1
#
# For Gemini via Google AI Studio, ADK expects:
#   GOOGLE_GENAI_USE_VERTEXAI=FALSE
#   GOOGLE_API_KEY=your_google_api_key

# OpenRouter model (via LiteLLM). This is the "pessimistic" debater.
OPENROUTER_MODEL_ID: str = os.getenv(
    "OPENROUTER_MODEL_ID",
    "openrouter/gpt-oss-20b",  # example from LiteLLM OpenRouter docs
)

# Gemini model (direct string, resolved by ADK / google-genai)
GEMINI_MODEL_ID: str = os.getenv(
    "GEMINI_MODEL_ID",
    "gemini-2.0-flash",  # example from ADK Models & Authentication docs
)


def get_openrouter_litellm() -> LiteLlm:
    """
    Create a LiteLlm model wrapper for OpenRouter, to be used with LlmAgent.

    ADK's LiteLlm integration:
        agent_openai = LlmAgent(
            model=LiteLlm(model="openai/gpt-4o"),
            ...
        )

    Here we adapt it to use OpenRouter instead, relying on LiteLLM's
    OpenRouter provider and environment variables.
    """
    return LiteLlm(model=OPENROUTER_MODEL_ID)


def get_gemini_model_id() -> str:
    """
    Return the Gemini model ID string to use directly with LlmAgent.

    The ADK docs show using a string like "gemini-2.0-flash" with LlmAgent,
    assuming GOOGLE_API_KEY and GOOGLE_GENAI_USE_VERTEXAI are configured.
    """
    return GEMINI_MODEL_ID
