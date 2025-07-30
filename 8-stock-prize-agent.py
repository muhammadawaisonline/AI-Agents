from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
from  dotenv import load_dotenv
import os
import time

load_dotenv()

gemini_api_key=os.getenv("GEMINI_API_KEY")

client =AsyncOpenAI(
api_key=gemini_api_key,
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

@function_tool
def fetch_stock_prize(location:str) -> str:
    """
    Goal:
        The objective of the agent to fetch stock market prizes of the given loaction.
    Args:
        loaction: fetch stock market prize for the provided loaction 

    expected_outpiut:
        Stock Market Pize: the stock market prize for the location is... 
    """
    print(f"fetching stock market prize for the {location}...")

    time.sleep(4)
    return "$1000.34"

agent = Agent(
    name="Stock Market Agent",
    instructions="Fetch stock market prizes for the given location",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[fetch_stock_prize]
)

while True:
    query = input("Enter Text: ")
    if query.lower()=="exit":
        break
    result= Runner.run_sync(agent, query) 
    print(result.final_output)

