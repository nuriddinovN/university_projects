from typing import Dict


def format_debate_turn(topic: str, speaker: str, text: str) -> Dict[str, str]:
    """
    Utility function tool used by the coordinator to wrap one debate turn
    into a structured record.

    This is a simple Function Tool following the ADK Function Tool pattern
    shown in the multi-tool quickstart: the function is regular Python with
    type hints and a descriptive docstring. ADK will introspect the signature
    and docstring automatically.

    Args:
        topic: The current debate topic or question.
        speaker: Who is speaking in this turn, e.g. "OpenRouter" or "Gemini" or "User".
        text: The actual argument or opinion expressed by that speaker.

    Returns:
        A small dictionary that can be used for logging, summarization, or
        further reasoning by the LLM.
    """
    return {
        "topic": topic,
        "speaker": speaker,
        "text": text,
    }
