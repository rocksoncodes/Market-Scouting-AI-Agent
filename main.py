from config import settings
from agents.scout import run_scout_agent

def main():
    """
    Run the market scout agent with the given objective.
    """
    run_scout_agent(settings.SCOUT_OBJECTIVE)

if __name__ == "__main__":
    main()