# streamlit_mult_agent.py

import asyncio
from typing import List, Dict

import streamlit as st
from dotenv import load_dotenv

from google.adk.runners import InMemoryRunner
from google.genai import types

from multi_agent.agent import root_agent  # <-- your existing multi-agent root


# ======================================================
# 1. Load environment variables (.env for keys)
# ======================================================
load_dotenv()


# ======================================================
# 2. ADK Runner Initialization (agent + app_name)
#    Pattern aligned with official examples:
#    InMemoryRunner(agent=agent, app_name="...") 
# ======================================================

# IMPORTANT:
# ADK keeps complaining:
#   "root agent was loaded from .../google/adk/agents, which implies app name 'agents'"
# So we simply pick app_name="agents" so they match and avoid mismatch noise.
runner = InMemoryRunner(agent=root_agent, app_name="agents")

APP_NAME = runner.app_name  # will be "agents"
session_service = runner.session_service
USER_ID = "streamlit_user"


# ======================================================
# 3. UI helpers: enforce short text + emojis for AGENT messages
# ======================================================

EMOJI_SETS = {
    "openrouter_pessimistic_debater": ["😒", "🙄", "💀", "😡", "🤮", "👺", "💅", "🌚", "❌", "⚠️", "🚩"],
    "gemini_supportive_debater": ["💖", "😊", "🌸", "🤗", "🥺", "✨", "🌈", "🕊️", "🙏", "💕", "🌟", "☀️"],
    "multi_model_debate_coordinator": ["⚖️", "🧭", "🗣️", "🤝", "📝"],
}


def truncate_words(text: str, max_words: int = 30) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words])


def ensure_emoji(author: str, text: str) -> str:
    emojis = EMOJI_SETS.get(author, ["🤖"])
    # if any emoji from this set is already present, keep as-is
    if any(e in text for e in emojis):
        return text
    # otherwise append one
    return text.rstrip() + " " + emojis[0]


def normalize_agent_text(author: str, text: str) -> str:
    """
    UI-level constraints:
    1. Limit agent messages to <= 30 words.
    2. Ensure there is at least one emoji per agent message.
    """
    if author == "user":
        return text

    text = truncate_words(text, max_words=30)
    text = ensure_emoji(author, text)
    return text


# ======================================================
# 4. Session helper + ADK call (run_async)
# ======================================================

async def _ask_adk(prompt: str, session_id: str) -> List[Dict[str, str]]:
    """
    Send a user message to the ADK runner and collect events as
    (author, text) pairs. Uses run_async, which is the recommended
    way to integrate a custom UI. :contentReference[oaicite:3]{index=3}
    """

    # We keep this simple and robust:
    # - Always try to get an existing session.
    # - If it doesn't exist or returns None, create one.
    try:
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )
    except Exception:
        session = None

    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )

    # We don't depend on session.id; we keep using our own session_id string.
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(prompt)],
    )

    events: List[Dict[str, str]] = []

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=user_content,
    ):
        if not event.content or not event.content.parts:
            continue

        text = "".join((p.text or "") for p in event.content.parts).strip()
        if not text:
            continue

        events.append(
            {
                "author": event.author,
                "text": normalize_agent_text(event.author, text),
            }
        )

    return events


def ask_adk_sync(prompt: str, session_id: str) -> List[Dict[str, str]]:
    """Sync wrapper for Streamlit."""
    return asyncio.run(_ask_adk(prompt, session_id))


# ======================================================
# 5. Streamlit UI layout (clean, modern, minimal)
# ======================================================

st.set_page_config(
    page_title="Multi-Agent Debate",
    page_icon="⚖️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f7;
    }
    .chat-container {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚖️ Multi-Agent Political Debate")
st.caption(
    "Pessimistic OpenRouter vs. Supportive Gemini · Built with Google ADK + Streamlit"
)

left, center, right = st.columns([1, 2, 1])

with center:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    st.markdown(
        "> 💡 **Tip:** Try a strong opinion like `I think AI should replace teachers`.\n"
        "> The agents will reply with **short, emoji-rich arguments** in turn."
    )


# ======================================================
# 6. Session state
# ======================================================

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "session_id" not in st.session_state:
    # Any stable ID string is fine; we manage sessions ourselves.
    st.session_state["session_id"] = "streamlit_session_1"


# ======================================================
# 7. Bubbles and styling per author
# ======================================================

AGENT_STYLES = {
    "user": {
        "label": "You",
        "avatar": "🧑",
    },
    "openrouter_pessimistic_debater": {
        "label": "OpenRouter • Critical",
        "avatar": "🔥",
    },
    "gemini_supportive_debater": {
        "label": "Gemini • Supportive",
        "avatar": "✨",
    },
    "multi_model_debate_coordinator": {
        "label": "Coordinator",
        "avatar": "🎛️",
    },
}


def render_message(author: str, text: str):
    """Render a single chat bubble."""
    style = AGENT_STYLES.get(
        author,
        AGENT_STYLES["multi_model_debate_coordinator"],
    )
    role = "assistant" if author != "user" else "user"

    with st.chat_message(role, avatar=style["avatar"]):
        st.markdown(f"**{style['label']}**\n\n{text}")


# ======================================================
# 8. Render history with spacing between different agents
# ======================================================

with center:
    prev_author = None
    for msg in st.session_state["messages"]:
        if prev_author is not None and msg["author"] != prev_author:
            # blank line between different authors for readability
            st.markdown("")
        render_message(msg["author"], msg["text"])
        prev_author = msg["author"]


# ======================================================
# 9. Input + new round
# ======================================================

with center:
    user_input = st.chat_input(
        "Enter your topic or opinion (e.g. “I think Donald Trump's politics are good”)"
    )

    if user_input:
        # 1) Add user message
        st.session_state["messages"].append({"author": "user", "text": user_input})
        render_message("user", user_input)

        # 2) Ask ADK and get streaming events
        events = ask_adk_sync(user_input, st.session_state["session_id"])

        # 3) Each Event becomes its own bubble, in order
        for ev in events:
            st.session_state["messages"].append(ev)
            render_message(ev["author"], ev["text"])

    st.markdown("</div>", unsafe_allow_html=True)
