from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, WebSearchTool, Runner
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

agent = Agent(
    name="WebSearch Agent",
    instructions="Search on web pages and fetch data according to the provided text",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[WebSearchTool]
)

while True:
    query = input("Enter Text: ")

    if query.lower() == "eixt":
        break
    result = Runner.run_sync(agent, query)
    print(result.final_output)
