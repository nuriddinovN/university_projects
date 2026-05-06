# 🤖 Multi-Agent Debate Chatbot

A sophisticated multi-agent system that orchestrates multiple AI models to conduct structured political debates. The system uses Google's Agent Development Kit (ADK) to coordinate two specialized debaters with different perspectives, while a coordinator agent moderates the conversation.

## 📋 What This Project Does

The Multi-Agent Debate Chatbot creates an intelligent debate environment where:

- **Two specialized debate agents** argue opposing viewpoints on political topics
  - **Pessimistic Debater** (OpenRouter/LiteLLM): Hyper-critical, arguments-focused perspective
  - **Supportive Debater** (Gemini): Motivational, constructive perspective

- **A Coordinator Agent** orchestrates the debate by:
  - Managing turn-taking between debaters
  - Formatting debate exchanges
  - Incorporating user input into the discussion
  - Adapting agent responses based on user opinions

- **Real-time interaction**: Users can join the debate, inject opinions, and watch agents respond dynamically

## 🔧 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────┐
│      Coordinator (Root) Agent           │
│     (Google Gemini powered)             │
│  - Manages debate flow                  │
│  - Calls sub-agents via AgentTool       │
│  - Formats debate turns                 │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────────┐  ┌──────────────┐
│ OpenRouter  │  │   Gemini     │
│  Debater    │  │  Debater     │
│(Pessimistic)│  │(Supportive)  │
└─────────────┘  └──────────────┘
```

### Key Components

#### 1. **root_agent** (Coordinator)
- **Model**: Google Gemini
- **Role**: Orchestrates the debate workflow
- **Capabilities**: 
  - Calls `openrouter_debater` and `gemini_debater` via `AgentTool`
  - Invokes `format_debate_turn()` tool to structure responses
  - Manages multi-turn conversations
  - Responds to user interventions

#### 2. **openrouter_debater** (Sub-Agent)
- **Model**: OpenRouter (LiteLLM-backed)
- **Personality**: Pessimistic, hyper-critical
- **Role**: Presents challenging, argument-focused positions
- **Instruction Set**: Defined in `config/personas.py`

#### 3. **gemini_debater** (Sub-Agent)
- **Model**: Google Gemini
- **Personality**: Supportive, motivational, soft-spoken
- **Role**: Presents constructive, empathetic perspectives
- **Instruction Set**: Defined in `config/personas.py`

#### 4. **Tools**
- `AgentTool`: Enables Agent-to-Agent communication (A2A) for coordinator to call debaters
- `format_debate_turn`: Custom tool for structuring debate exchange format

### Multi-Agent Orchestration Pattern

The system uses Google ADK's multi-agent pattern:

```python
root_agent = LlmAgent(
    model=gemini_model_id,
    name="multi_model_debate_coordinator",
    tools=[
        AgentTool(agent=openrouter_debater),  # A2A hook
        AgentTool(agent=gemini_debater),      # A2A hook
        format_debate_turn,                    # Custom tool
    ],
    sub_agents=[openrouter_debater, gemini_debater],  # Hierarchy
)
```

This pattern ensures:
- Coordinator manages the debate flow
- Debaters act autonomously based on their instructions
- Clean parent-child agent relationships
- Structured tool invocations for complex interactions

## 🛠️ Tools & Technologies

### Core Framework
- **[Google Agent Development Kit (ADK)](https://developers.google.com/agents)** - Multi-agent orchestration
  - `LlmAgent`: Base class for all agents
  - `AgentTool`: Agent-to-Agent communication mechanism

### Language Models
- **[Google Gemini](https://ai.google.dev/)** - Powers coordinator and supportive debater
  - Via Google ADK integration
  - Configured through `config/models.py`

- **[OpenRouter](https://openrouter.ai/)** - Powers pessimistic debater
  - Unified API access to multiple models (GPT-4, Claude, etc.)
  - Integrated via LiteLLM

### Libraries
- **[LiteLLM](https://www.litellm.ai/)** - Universal LLM interface
  - Standardized API for OpenRouter, Google, and other providers
  - Configuration via `config/models.py`

- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment configuration
  - Loads `.env` file for API keys
  - Required keys: `GOOGLE_API_KEY`, `OPENROUTER_API_KEY`

### Python
- **Version**: 3.8+
- **Core modules**: `os`, environment handling

## 📁 Project Structure

```
chat_bot/multi_agent/
├── README.md                    # This file
├── __init__.py                  # Package initialization
├── agent.py                     # Main agent definitions & orchestration
├── test_api.py                  # API connectivity tests
├── config/
│   ├── __init__.py
│   ├── models.py               # Model initialization (Gemini, OpenRouter)
│   └── personas.py             # Agent instruction sets (debater personalities)
└── tools/
    ├── __init__.py
    └── debate_tools.py         # Custom tools (format_debate_turn, etc.)
```

## 🚀 Setup & Installation

### Prerequisites

1. **Python 3.8+**
2. **API Keys** (free tiers available):
   - Google AI API Key ([get here](https://aistudio.google.com/app/apikey))
   - OpenRouter API Key ([get here](https://openrouter.ai/keys))

### Step 1: Install Dependencies

```bash
cd chat_bot/multi_agent
pip install google-adk litellm python-dotenv
```

### Step 2: Configure Environment Variables

Create a `.env` file in the `chat_bot/multi_agent/` directory:

```env
# Google (Gemini)
GOOGLE_API_KEY=your_google_api_key_here

# OpenRouter (requires OPENROUTER_API_BASE & model ID)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_BASE=https://openrouter.ai/api/v1
OPENROUTER_MODEL_ID=gpt-4  # or any OpenRouter-supported model
```

### Step 3: Verify Installation

```bash
python test_api.py
```

Expected output:
```
--- Starting API Connection Test ---
1. Testing Google (Gemini)...
✅ Google Success: Gemini Online

2. Testing OpenRouter (GPT)...
✅ OpenRouter Success: OpenRouter Online

--- Test Complete ---
```

## 💡 Usage Examples

### Basic Debate Session

```python
from chat_bot.multi_agent.agent import root_agent

# Initialize a debate on a political topic
response = root_agent.generate_content(
    "Let's debate whether universal basic income is economically viable."
)
print(response)
```

### Accessing Individual Debaters

```python
from chat_bot.multi_agent.agent import openrouter_debater, gemini_debater

# Pessimistic perspective
openrouter_response = openrouter_debater.generate_content(
    "Why would universal basic income fail?"
)

# Supportive perspective
gemini_response = gemini_debater.generate_content(
    "What are the benefits of universal basic income?"
)
```

### Structured Debate Format

```python
from chat_bot.multi_agent.tools.debate_tools import format_debate_turn

# Format a debate exchange
formatted = format_debate_turn(
    topic="Economic policy",
    openrouter_argument="Argument against...",
    gemini_argument="Argument for..."
)
print(formatted)
```

## 🔄 How Agent Communication Works

### Agent-to-Agent (A2A) Flow

1. **User Input** → Root Agent receives query
2. **Coordinator Decision** → Determines which agent(s) to call
3. **AgentTool Invocation** → Root agent calls sub-agents:
   - `AgentTool(agent=openrouter_debater)` → Pessimistic response
   - `AgentTool(agent=gemini_debater)` → Supportive response
4. **Response Formatting** → Uses `format_debate_turn` tool
5. **Output** → Structured debate response to user

### Key Implementation in `agent.py`

```python
root_agent = LlmAgent(
    model=gemini_model_id,
    tools=[
        AgentTool(agent=openrouter_debater),  # Enables A2A calls
        AgentTool(agent=gemini_debater),
        format_debate_turn,
    ],
    sub_agents=[openrouter_debater, gemini_debater],  # Hierarchy
)
```

## ⚙️ Configuration Files

### `config/models.py`
Initializes and returns model instances:
- `get_openrouter_litellm()` - Returns LiteLLM-configured OpenRouter model
- `get_gemini_model_id()` - Returns Gemini model ID for ADK

### `config/personas.py`
Defines agent instructions:
- `OPENROUTER_DEBATER_INSTRUCTION` - Pessimistic debater prompt
- `GEMINI_DEBATER_INSTRUCTION` - Supportive debater prompt
- `COORDINATOR_INSTRUCTION` - Coordinator/orchestrator prompt

### `tools/debate_tools.py`
Custom tools:
- `format_debate_turn()` - Structures debate exchanges for readability

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'google.adk'"

**Solution**: Ensure Google ADK is installed
```bash
pip install google-adk --upgrade
```

### Issue: "OPENROUTER_API_KEY not found"

**Solution**: 
1. Verify `.env` file exists in `chat_bot/multi_agent/`
2. Check that `OPENROUTER_API_KEY` is set correctly
3. Reload environment: `load_dotenv(override=True)`

### Issue: API timeouts or rate limits

**Solution**:
- Add retry logic in API calls
- Check OpenRouter/Google quotas
- Consider caching responses for testing

### Issue: Agents not calling each other

**Solution**:
- Verify `AgentTool` is properly instantiated with agent instances
- Check coordinator instruction for sub-agent invocation language
- Review ADK multi-agent documentation

## 📊 Performance & Scaling

### Current Capabilities
- Handles 2 sub-agents with 1 coordinator
- Supports real-time user interaction
- Structures debates in 2-3 agent turns

### Future Enhancements
- **More debaters**: Add agents with moderate/neutral perspectives
- **Memory**: Track debate history across sessions
- **Persistence**: Store debate transcripts to database
- **Evaluation**: Score argument quality automatically
- **Dynamic personas**: Adjust debater personalities based on topic
- **Web UI**: Streamlit/FastAPI interface for interactive debates

## 📚 Learning Resources

- [Google Agent Development Kit Docs](https://developers.google.com/agents)
- [Multi-Agent Systems Patterns](https://cloud.google.com/docs/agents)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [OpenRouter API Reference](https://openrouter.ai/docs)

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Multi-agent orchestration patterns
- ✅ Agent-to-Agent (A2A) communication
- ✅ Tool-based agent capabilities
- ✅ Model selection & configuration
- ✅ Environment-based secrets management
- ✅ Structured prompt engineering for agent personas
- ✅ Integration of multiple LLM providers

## 📝 Notes

- This project uses **generative AI** - responses are non-deterministic
- API costs apply; monitor usage on Google AI and OpenRouter dashboards
- Agent instructions (personas) can be modified in `config/personas.py`
- The multi-agent pattern follows Google ADK best practices

---

**Last Updated**: May 2026  
**Status**: Active Development
