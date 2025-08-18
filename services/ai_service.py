import os
from dotenv import load_dotenv
from utils.logger import logger
from google import genai
from google.genai import types


def initialize_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("Failed to intialize agent due to missing api key")
        raise SystemExit("Please set your api key to initialize the agent...")
    
    client = genai.Client(api_key = api_key)
   
    return client


def provide_agent_tools(tools):
    config=types.GenerateContentConfig(tools=tools)
    return config


agent_objective = """
    You are a market scout agent.
    Your objective is to identify Reddit posts where users face real, recurring problems.
    Evaluate each post against the selection criteria:
    1. Frequency (problem affects many users, not just one).
    2. Severity (wastes time, money, or causes frustration).
    3. Clarity (user describes problem in a clear, relatable way).
    4. Feasibility (problem can realistically be solved by a product/service).
    If a post meets at least 80 percent of the criteria, reframe it into a structured problem brief:
    [X user faces Y problem, so build Z solution to achieve W result].
    For each post received return the structured brief only.
    At the very end, write: "Total problems identified: <number>
    """