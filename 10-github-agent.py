from json import load
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Replace with your actual Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Function to fetch user data from GitHub API
@function_tool
def fetch_github_user_data(username: str) -> str:
    """
    Goal: Fetch public GitHub user data
    
    Args: 
        username (str): GitHub username whose data is to be fetched
    
    Expected Output: 
        A string containing the user's GitHub profile details.
    """
    try:
        print(f"Fetching GitHub user data for {username}")

        url = f'https://api.github.com/users/{username}'
        response = requests.get(url)
        
        if response.status_code == 200:
            user_data = response.json()
            return f"User: {user_data['login']}\nName: {user_data['name']}\nLocation: {user_data['location']}\nPublic Repos: {user_data['public_repos']}\nFollowers: {user_data['followers']}\nFollowing: {user_data['following']}"
        else:
            return f"Error: {response.status_code}, User not found or API error."

    except Exception as e:
        return f"Error: {str(e)}"

# Create an agent that uses the GitHub API tool
agent = Agent(
    name="GitHub User Data Fetcher",
    instructions="Fetch and display GitHub user data for the provided username",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[fetch_github_user_data],
)

# Get user input for GitHub username
query = input("Enter the GitHub username: ")

# Run the agent to fetch the user data
result = Runner.run_sync(agent, query)

# Output the result
print(result.final_output)

