from utils.agent import start_agent, agent_objective
from scraper.reddit_scraper import fetch_reddit_posts

def main():
    """
    Main execution function for running the agent.
    """

    start_agent(agent_objective)

if __name__ == "__main__":
    main()