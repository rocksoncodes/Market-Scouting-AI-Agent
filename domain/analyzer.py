from sqlalchemy.orm import sessionmaker
from database.models import database_engine, Post, Comment
from domain.sentiment import RedditSentiment
from typing import Dict, List
from utils.queries import serialize_post, serialize_comment, get_comments_for_post
from utils.logger import logger

Session = sessionmaker(bind=database_engine)

class CommentAnalyzer:
    def __init__(self):
        self.session = Session()
        self.analyzer = RedditSentiment()
        self.limit = 1

        self.query_results = None
        self.extracted_comments = None
        self.sentiment_result = None

    def query_posts_with_comments(self) -> List[Dict]:
        """
        Query posts along with their comments.
        Each comment is included only if its submission_id matches the post id.
        """
        session = Session()
        post_records = []

        logger.info("Querying posts with comments from the database...")

        try:
            posts = session.query(Post).limit(self.limit).all()
            total_comments = 0

            for post in posts:
                comment_records, comment_count = get_comments_for_post(session, post.submission_id)
                total_comments += comment_count

                logger.info(f"Post {post.id} retrieved with {comment_count} comments.")
                post_records.append(serialize_post(post, comment_records))

            logger.info(
                f"Query complete. Retrieved {len(posts)} posts and {total_comments} comments in total."
            )
            return post_records

        except Exception as e:
            logger.error(f"Error querying posts with comments: {e}", exc_info=True)
            return []

        finally:
            session.close()


    def extract_comments(self):
        """
        Extract unprocessed comments from the query results
        """
        if not self.query_results:
            self.query_posts_with_comments()


    def analyze_comments(self):
        """
        Run sentiment analysis on extracted comments
        """
        pass


    def store_sentiment_results(self):
        """
        Insert sentiments results into the database
        """
        pass


    def marked_comments_processed(self):
        """
        Update comments as processed
        """
        pass


    def save_changes(self):
        """
        Commit all changes to the database
        """
        pass