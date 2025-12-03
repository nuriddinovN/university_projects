import os

from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

from .config.models import get_openrouter_litellm, get_gemini_model_id
from .config.personas import (
    OPENROUTER_DEBATER_INSTRUCTION,
    GEMINI_DEBATER_INSTRUCTION,
    COORDINATOR_INSTRUCTION,
)
from .tools.debate_tools import format_debate_turn

# Load .env so:
# - GOOGLE_API_KEY / GOOGLE_GENAI_USE_VERTEXAI are available for Gemini
# - OPENROUTER_API_KEY / OPENROUTER_API_BASE / OPENROUTER_MODEL_ID are available for LiteLLM
load_dotenv()

# ---- Models -----------------------------------------------------------------

openrouter_model = get_openrouter_litellm()
gemini_model_id = get_gemini_model_id()

# ---- Debater Agents ---------------------------------------------------------


openrouter_debater = LlmAgent(
    model=openrouter_model,
    name="openrouter_pessimistic_debater",
    description=(
        "Pessimistic, hyper-critical political debater that argues via an "
        "OpenRouter-backed model."
    ),
    instruction=OPENROUTER_DEBATER_INSTRUCTION,
)

gemini_debater = LlmAgent(
    model=gemini_model_id,
    name="gemini_supportive_debater",
    description=(
        "Supportive, motivational, soft-spoken political debater powered by Gemini."
    ),
    instruction=GEMINI_DEBATER_INSTRUCTION,
)

# ---- Coordinator / Root Agent -----------------------------------------------
# Pattern based on the "multi-agent retail assistant" example:
# - Root LlmAgent orchestrates sub agents using AgentTool and sub_agents[]
#   (see the BigQuery Agent Analytics codelab & Multi-Agent Systems docs).


root_agent = LlmAgent(
    model=gemini_model_id,
    name="multi_model_debate_coordinator",
    description=(
        "Coordinator that runs a structured political debate between a pessimistic "
        "OpenRouter-based debater and a supportive Gemini-based debater. The user "
        "can jump in and the agents adapt to the user's opinion."
    ),
    instruction=COORDINATOR_INSTRUCTION,
    tools=[
        # Explicit A2A (AgentTool) hooks so the coordinator can call each debater
        AgentTool(agent=openrouter_debater),
        AgentTool(agent=gemini_debater),
        # Simple function tool, mirroring the multi-tool quickstart pattern
        format_debate_turn,
    ],
    # Parent-child relationship in the agent hierarchy (multi-agent docs)
    sub_agents=[
        openrouter_debater,
        gemini_debater,
    ],
)

