from agents.scout_agent import run_scout_agent
from services.ai_service import agent_objective

def main():
    """Run the market scout agent with the given objective."""

    run_scout_agent(agent_objective)

if __name__ == "__main__":
    main()