

import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
import os
load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
async def main():
    agent = Agent(
    name= "Assistant",
    instructions="You are my AI assistant. You should generate relevant data that should be asked you in query",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),

    )

    query = input("Enter Text: ")

    result = Runner.run_streamed(agent, input=query)
    async for event in result.stream_events():
        if event.type=="raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

asyncio.run(main())




