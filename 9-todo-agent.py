
from sys import exception
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
from dotenv import load_dotenv
from typing import Dict, Any
from datetime import datetime
import os
import time
import json

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelaunage.googleapis.com/v1beta/openai/"
)
@function_tool
def list_todos():
    """ List all todos form todos.json file."""
    try:
        print("listing todos...")
        time.sleep(4)
        with open("Agent/todos.json", "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error {e}")
        raise FileNotFoundError("The file todos.json not found.")

@function_tool
def add_todo(title: str, description:str="", due_date:str="" ) -> Dict[str, Any]:
    """ Goal: 
            Add new todo to the todo.json file
        Args:
            title: The title of the todo
            description: Description of the newly add todo
            due_date: the expiry date of the todo
        expected_output:
            A new todo added with title, descrption, due_date todos.json file """
    try:

        try:
            with open("Agent/todos.json") as file:
                todo= json.load(file)
        except FileNotFoundError:
                todos = [] #if file doesn't exist start with empty file
        except json.JSONDecodeError:
            raise ValueError("Error decoding todos.json. Ensure it contains valid JSON")
    #create new todo
        new_todo = {
        "id" :len(todos) + 1,
        "title": title,
        "description":description,
        "completed":False,
        "dueDate": due_date if due_date else datetime().now().strftime("%Y-%m-%d")
    }
        #append and save
        todos.append(new_todo)
        with open("Agent/todos.json", "w") as file:
            json.dump(todos, file, intent= 2)

            return new_todo
    except Exception as e:
        raise Exception(f"Failed to add todo {str(e)}")



agent =Agent(
    name= "Todo Agent",
    instructions= "You are expert in todos. You can add, update, delete to do in the todo list",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[list_todos, add_todo] 
)

query = input("Enter the query: ")
result = Runner.run_sync(agent, query)

print(result.final_output)