import os
from dotenv import load_dotenv
from utils.logger import logger
from google import genai


def initialize_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("Failed to intialize agent due to missing api key")
        raise SystemExit("Please set your api key to initialize the agent...")
    
    client = genai.Client(api_key = api_key)
   
    return client


agent = initialize_gemini()


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
    Return the structured brief only.
    """


# TODO: Extend this function to use the reddit_scraper function -> fetch_reddit_posts()
def start_agent(query):

    response = agent.models.generate_content(
        model = "gemini-1.5-flash",
        contents = f"{query}"
    )
    print(response.text)