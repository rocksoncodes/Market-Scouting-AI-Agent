from services.gemini_service import initialize_gemini, provide_agent_tools
from services.sentiment_service import execute_sentiment_pipeline
from google.genai import errors
from utils.logger import logger


agent = initialize_gemini()


def run_scout_agent(query):
   """
   Runs the Market Scout Agent with a given query.
   Uses Gemini to generate content and apply agent tools.
   """
   try:
      response = agent.models.generate_content(
         model = "gemini-1.5-flash",
         contents = query,
         config = provide_agent_tools(tools=[execute_sentiment_pipeline])
      )

      logger.info("Market Scout Agent executed successfully..")
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