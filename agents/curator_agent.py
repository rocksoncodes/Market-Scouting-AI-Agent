from clients.gemini_client import initialize_gemini, provide_agent_tools
from pipelines.curator_pipeline import feeder
from config import settings
from google.genai import errors
from utils.logger import logger

agent = initialize_gemini()

def run_curator_agent():
   """
   Runs the Curator Agent with a given query.
   Uses Gemini to generate content and apply agent tools.
   """
   try:
      response = agent.models.generate_content(
         model = settings.AGENT_MODEL,
         contents = settings.SCOUT_OBJECTIVE,
         config = provide_agent_tools(tools=[feeder])
      )

      logger.info("Curator Agent executed successfully..")
      print(response.text)

   except errors.ServerError as e:
      logger.error(f"Gemini server error: {e}")
      return {"error": "Model temporarily unavailable. Please try again later."}

   except errors.ClientError as e:
    if "RESOURCE_EXHAUSTED" in str(e):
        logger.error("Quota exceeded. Try again after reset or switch models.")
        return {"error": "Quota exceeded"}
    raise

   except Exception as e:
      logger.exception(f"Unexpected error while running Market Scout Agent: {e}")
      raise SystemExit("Agent terminated due to an error.")