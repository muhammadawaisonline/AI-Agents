from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv
import os
load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

agent = Agent(
    name="Assistent",
    instructions="You are a helpful assistent",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client) 
)

while True:
    query = input("Enter Text: ")
    if query.lower() == "exit":
        break

    result= Runner.run_sync(agent, query)
    print(result.final_output)