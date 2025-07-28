from json import load
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

class Quiz(BaseModel):
    questions:str
    options:List[str]
    correct_option:str

agent = Agent(
    name= "Quiz Generator",
    instructions= "Generate quiz for the given text.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
)

query = input("Let's Generate Quiz: ")

result = Runner.run_sync(agent, query)
print(result.final_output)
