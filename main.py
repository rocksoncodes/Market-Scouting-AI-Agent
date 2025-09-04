from agents.scout_agent import run_scout_agent
from config import settings
from services.gemini_service import scout_agent_objective

def main():
    """
    Run the market scout agent with the given objective.
    """
    run_scout_agent(settings.SCOUT_OBJECTIVE)

if __name__ == "__main__":
    main()