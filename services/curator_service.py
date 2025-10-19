from typing import Dict, List
from sqlalchemy.orm import sessionmaker
from google.genai import errors
from config import settings
from database.engine import database_engine
from database.models import Post, Sentiment, ProcessedBriefs
from database.session import get_session
from utils.logger import logger
from clients.gemini_client import initialize_gemini, provide_agent_tools


Session = sessionmaker(bind=database_engine)


class CuratorService:
    def __init__(self):
        self.session = get_session()
        self.agent = initialize_gemini()
        self.post_with_sentiments = []
        self.curator_agent_response = None

    def query_posts_with_sentiments(self) -> List[Dict]:

        session = self.session
        post_records = []

        logger.info("Querying posts with sentiments from the database...")

        posts_with_sentiments = (
            session.query(Post, Sentiment)
            .join(Sentiment, Sentiment.post_id == Post.submission_id)
            .all()
        )

        for post, sentiment in posts_with_sentiments:
            post_with_sentiments = {
                "post_number": post.id,
                "subreddit": post.subreddit,
                "title": post.title,
                "body": post.body,
                "sentiment_score": sentiment.sentiment_results
            }
            post_records.append(post_with_sentiments)

        logger.info("Successfully queried posts with sentiments.")

        self.post_with_sentiments = post_records
        return post_records


    def feeder(self) -> List[Dict]:
        """
        Call the Feeder function to obtain posts and their sentiment analysis results.
        Each record in the returned list contains a post and its sentiment score.
        Use this information to guide your next actions, generate summaries, or perform analysis as required.
        """
        return self.query_posts_with_sentiments()


    def execute_curator_agent(self):

        if not self.post_with_sentiments:
            logger.info("No posts with sentiments found. Querying database...")
            self.query_posts_with_sentiments()

        try:
            logger.info("Executing Curator Agent...")
            response = self.agent.models.generate_content(
                model=settings.AGENT_MODEL,
                contents=settings.SCOUT_OBJECTIVE,
                config=provide_agent_tools(tools=[self.feeder])
            )

            logger.info("Curator Agent executed successfully..")
            curator_response = response.text
            print(response.text)

            self.curator_agent_response = curator_response
            return curator_response

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


    def store_curator_response(self):

        session = self.session

        if not self.curator_agent_response:
            logger.info("No curator agent response found. Running agent...")
            try:
                self.execute_curator_agent()
            except Exception as e:
                logger.error(f"Failed to run curator agent: {e}", exc_info=True)

        try:
            curated_brief = ProcessedBriefs(
                curated_content = self.curator_agent_response
            )
            session.add(curated_brief)
            session.commit()
            logger.info("Curator response stored successfully in the database.")

        except Exception as e:
            session.rollback()
            logger.error(f"Failed to store curator response: {e}", exc_info=True)

        finally:
            session.close()