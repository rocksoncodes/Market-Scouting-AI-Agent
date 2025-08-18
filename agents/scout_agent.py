from services.ai_service import initialize_gemini, provide_agent_tools
from utils.reddit_functions import fetch_reddit_posts


agent = initialize_gemini()


def run_scout_agent(query):
    response = agent.models.generate_content(
        model = "gemini-1.5-flash",
        contents = query,
        config=provide_agent_tools(tools=[fetch_reddit_posts])
    )
    print(response.text)