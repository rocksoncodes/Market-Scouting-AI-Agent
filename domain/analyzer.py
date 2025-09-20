from sqlalchemy.orm import sessionmaker
from database.models import database_engine, Post
from domain.sentiment import RedditSentiment
from typing import Dict, List
from utils.query import serialize_post, get_comments_for_post
from utils.logger import logger

Session = sessionmaker(bind=database_engine)

class CommentAnalyzer:
    def __init__(self):
        self.session = Session()
        self.analyzer = RedditSentiment()
        self.limit = 1

        self.query_results = []
        self.extracted_comments = []
        self.sentiment_result = []

    def query_posts_with_comments(self) -> List[Dict]:
        """
        Query posts along with their comments.
        Each comment is included only if its submission_id matches the post id.
        """
        session = self.session
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
            self.query_results = post_records
            return post_records

        except Exception as e:
            logger.error(f"Error querying posts with comments: {e}", exc_info=True)
            self.query_results = []
            return []

        finally:
            session.close()


    def extract_comments(self) -> List[List[str]]:
        """
        Extract unprocessed comment bodies from the query results
        """
        if not self.query_results:
            self.query_posts_with_comments()

        new_comments = []

        for data in self.query_results:
            comments = data.get("comments", [])
            for item in comments:
                body_comment = item.get("body", "")
                new_comments.append([body_comment])

        self.extracted_comments = new_comments
        return new_comments


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