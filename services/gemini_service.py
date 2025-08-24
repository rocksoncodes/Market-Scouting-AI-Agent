import os
from dotenv import load_dotenv
from utils.logger import logger
from google import genai
from google.genai import types


def initialize_gemini() -> genai.Client:
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

    
def provide_agent_tools(tools) -> types.GenerateContentConfig | None:
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

    Your input includes multiple Reddit posts, each with:
    - Title
    - Body
    - Subreddit
    - List of comments

    Your objective:
    1. Group posts by subreddit.

    2. For each post:
        - Analyze the title, body, and comments.
        - Perform sentiment analysis on comments (internally).
        - Check if comments indicate frequent, severe, or frustrating issues related to the post.

    3. Apply selection criteria:
        a. Frequency: Are multiple users experiencing the same issue?
        b. Severity: Does the tone of comments indicate frustration or significant problems?
        c. Clarity: Is the problem clearly explained in the post?
        d. Feasibility: Can a realistic product or service solve it?
        
    4. If no posts qualify, log "No problems identified."

    Output:
    - Only log which posts were stored.
    - Sentiment summary on each post
    - Append: "Total problems stored: <number>"
    """