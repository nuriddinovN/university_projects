# streamlit_mult_agent.py

import asyncio
from typing import List, Dict

import streamlit as st
from dotenv import load_dotenv

from google.adk.apps import App
from google.adk.runners import InMemoryRunner
from google.genai import types

from multi_agent.agent import root_agent   # <-- your existing multi-agent system


# ======================================================
# 1. Load environment variables
# ======================================================
load_dotenv()


# ======================================================
# 2. Correct ADK Initialization (FROM OFFICIAL DOCS)
#    https://google.github.io/adk-docs
# ======================================================
APP_NAME = "multi_agent_streamlit_app"

adk_app = App(
    name=APP_NAME,
    root_agent=root_agent,
)

runner = InMemoryRunner(app=adk_app)
session_service = runner.session_service

USER_ID = "streamlit_user"


# ======================================================
# 3. ADK Session Management (official pattern)
# ======================================================
async def ensure_session(session_id: str):
    """Ensure a valid ADK session or create one."""
    try:
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )
    except Exception:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )
    return session


# ======================================================
# 4. Ask ADK (async) using run_async()
#    This is the correct way to build a custom UI.
# ======================================================
async def _ask_adk(prompt: str, session_id: str) -> List[Dict[str, str]]:
    session = await ensure_session(session_id)
    session_id = session.id  # canonical ID returned by ADK

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

        events.append({"author": event.author, "text": text})

    return events


def ask_adk_sync(prompt: str, session_id: str):
    """Sync wrapper for Streamlit."""
    return asyncio.run(_ask_adk(prompt, session_id))


# ======================================================
# 5. Streamlit Page Setup
# ======================================================
st.set_page_config(
    page_title="Multi-Agent Debate",
    page_icon="⚖️",
    layout="centered",
)

st.markdown("""
# ⚖️ Multi-Agent Debate System  
### Powered by Google ADK (Gemini + OpenRouter)

Start by typing a political opinion or topic.  
The pessimistic OpenRouter agent and the supportive Gemini agent will debate your topic.

_Type **exit** to stop the debate._
""")

# ======================================================
# 6. Session State Chat History
# ======================================================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "session_id" not in st.session_state:
    st.session_state["session_id"] = "streamlit_session_1"


# ======================================================
# 7. Chat Bubble Styling
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
    """Render one chat bubble."""
    style = AGENT_STYLES.get(
        author,
        AGENT_STYLES["multi_model_debate_coordinator"]
    )

    role = "assistant" if author != "user" else "user"

    with st.chat_message(role, avatar=style["avatar"]):
        st.markdown(f"**{style['label']}**\n\n{text}")


# ======================================================
# 8. Render Chat History
# ======================================================
for msg in st.session_state["messages"]:
    render_message(msg["author"], msg["text"])


# ======================================================
# 9. Prompt Input Box
# ======================================================
user_input = st.chat_input("Enter your topic or opinion...")

if user_input:
    # Show user bubble
    st.session_state["messages"].append({"author": "user", "text": user_input})
    render_message("user", user_input)

    # Send to ADK (call your root multi-agent)
    events = ask_adk_sync(user_input, st.session_state["session_id"])

    # Display each agent event as its own bubble
    for ev in events:
        st.session_state["messages"].append(ev)
        render_message(ev["author"], ev["text"])
