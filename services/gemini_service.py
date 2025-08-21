import os
from dotenv import load_dotenv
from utils.logger import logger
from google import genai
from google.genai import types


def initialize_gemini():
    """
    Initialize Gemini client using API key from environment variables.
    Returns a genai.Client instance if successful, otherwise exits.
    """
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment variables.")
        raise SystemExit("Startup failed: Please set your GEMINI_API_KEY to initialize the agent.")

    try:
        client = genai.Client(api_key = api_key)
        logger.info("Gemini client initialized successfully. Agent is ready.")
        return client
    
    except Exception as e:
        logger.exception(f"Failed to initialize Gemini client: {e}")
        raise SystemExit("Gemini initialization failed. Check your API key and SDK setup.") 

    
def provide_agent_tools(tools):
    """
    Provide tools to the agent by creating a GenerateContentConfig.
    Returns the config if successful, otherwise None.
    """
    try:
        config=types.GenerateContentConfig(tools=tools)
        logger.info(f"Agent tools configured successfully with {len(tools)} tool(s).")
        return config
        
    except Exception as e:
        logger.exception(f"Failed to configure agent tools: {e}")
        return None


scout_agent_objective = """
    You are a market scout agent.
    Your objective is to identify Reddit posts where users face real, recurring problems.
    There are multiple posts from each subreddit. Group accordingly and:

    Evaluate each post against the selection criteria:
    1. Frequency (problem affects many users, not just one).
    2. Severity (wastes time, money, or causes frustration).
    3. Clarity (user describes problem in a clear, relatable way).
    4. Feasibility (problem can realistically be solved by a product/service).
    If a post meets at least 80 percent of the criteria:
    Store the qualified post into our database using the `store_reddit_problems` function.

    If no problems where found let me know no problems were identified

    Output:
    - Do not return or reframe the post.
    - Only log which posts were stored.
    - At the end, append: "Total problems stored: <number>"
    """