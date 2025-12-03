
import os

from dotenv import load_dotenv

from google.adk.agents import LlmAgent

from google.adk.models.lite_llm import LiteLlm

load_dotenv()

openrouter_model = LiteLlm(

model="openrouter/gpt-oss-20b",

default_parameters={"max_tokens": 512}

)

simple_agent = LlmAgent(

model=openrouter_model,

name='simple_openrouter_agent',

description='A basic ADK agent using LiteLlm and OpenRouter.',

instruction="""

You are a friendly, helpful, and concise assistant.

Your sole purpose is to demonstrate the successful connection between the Google ADK and the OpenRouter API.

Acknowledge the user's input and confirm that you are running on gpt-4o via OpenRouter.""")

root_agent = simple_agent

