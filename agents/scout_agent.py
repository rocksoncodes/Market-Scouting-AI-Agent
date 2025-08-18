from services.ai_service import initialize_gemini


agent = initialize_gemini()


def run_scout_agent(query):
    """
    TODO(rocksoncodes): [High Priority] 
        - Extend this function to use the reddit_scraper function
        - Specifically function -> fetch_reddit_posts()
        - The agent should be able to call this function to fetch posts from reddit
        - And finally return problem statements for storage
    """

    response = agent.models.generate_content(
        model = "gemini-1.5-flash",
        contents = f"{query}"
    )
    print(response.text)