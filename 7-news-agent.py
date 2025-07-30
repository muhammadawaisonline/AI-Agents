
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
from dotenv import load_dotenv
import os
import time

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)
@function_tool
def fetch_news(loaction:str) -> str:
    """
    Goal: Provide News for the given location

    Args: 
            Location: loaction to fetch the news for
    expected_ouput:
            It is expected cm will visit to the  provided loaction

    """
    print(f"Fetching news for the {loaction}....")
    time.sleep(4)
    return "breaking News"

agent = Agent(
    name="News Agent",
    instructions="You are a news agent that provides latest news in response to the query",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=client),
    tools=[fetch_news]

)

while True:
    query= input("Enter Text: ")

    if query.lower()=="exit":
        break
    result = Runner.run_sync(agent, query)
    print(result.final_output)