from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, function_tool, Runner 
from dotenv import load_dotenv
import os
import time

load_dotenv()

gemini_api_key= os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

@function_tool
async def fetch_weather(location:str) -> str:
        """
         Goal:
            fetch weather for given loaction.

        Args: 
        Location: Fetch weather update for the location

        expected_output:
        out_put: provide us weather report like sunny, cloudy, Rainy or any thing else.
        """
        print(f"fetching weather for {location} location....")
        time.sleep(2)
        return "sunny"

agent = Agent(
    name="Weather Report provider",
    instructions="Use the given tool and provide waether report for the given loaction",
    model= OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[fetch_weather]
)

query= input("Enter the location for Weather Report: ")

result = Runner.run_sync(agent, query)

print(result.final_output)



