from sqlalchemy.orm import sessionmaker
from database.engine import database_engine
from database.models import Post, Sentiment
from utils.query_helper import get_session
from typing import Dict, List
from utils.logger import logger

Session = sessionmaker(bind=database_engine)


class Curator:
    def __init__(self):
        self.session = get_session()
        self.post_with_sentiments = []


    def query_posts_with_sentiments(self) -> List[Dict]:
        """
        Query posts along with their sentiments.
        Each sentiment is included only if its submission_id matches the post id.
        """
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

        self.post_with_sentiments = post_records
        return post_records