from agents.scout_agent import run_scout_agent
from services.ai_service import agent_objective

def main():
    """
    Main execution function for running the agent.
    """

    run_scout_agent(agent_objective)

if __name__ == "__main__":
    main()