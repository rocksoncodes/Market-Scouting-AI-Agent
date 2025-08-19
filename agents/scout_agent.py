from services.ai_service import initialize_gemini, provide_agent_tools
from utils.reddit_functions import fetch_reddit_posts
from utils.logger import logger


agent = initialize_gemini()


def run_scout_agent(query):
   """
   Run the Market Scout Agent with a given query.
   Uses Gemini to generate content and apply agent tools.
   """
   try:
      response = agent.models.generate_content(
         model = "gemini-1.5-flash",
         contents = query,
         config=provide_agent_tools(tools=[fetch_reddit_posts])
      )

      logger.info("Market Scout Agent executed successfully.")
      print(response.text)

   except Exception:
      logger.exception("Unexpected error while running Market Scout Agent.")
      raise SystemExit("Agent terminated due to an error.")