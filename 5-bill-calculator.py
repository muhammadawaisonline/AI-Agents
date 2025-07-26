from json import load
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
from dotenv import load_dotenv
import os


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

@function_tool
def bill_calculator(unit: float, rate: float) -> str:
    """
    goal: calculate the bill for given units and rate

    args: The number of units consumed and the rate per unit

    expected_output: The total bill for the given units and rate


    """
    try:
        print(f"calculating bill for {unit} units at {rate} per unit")
        
        bill_amount = unit * rate

        return bill_amount

    except Exception as e:
        raise print(f"Error calculating bill: {e}")

agent = Agent(
            name= "Bill Calculator",
            instructions= "calculate the bill for given units and rate",
            model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
            tools=[bill_calculator],
            
        )
query = input("Enter the number of units consumend and rate per unit: ")
result = Runner.run_sync(agent, query)
print (result.final_output)











