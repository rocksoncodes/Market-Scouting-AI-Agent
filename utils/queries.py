from sqlalchemy.orm import sessionmaker
from database.models import database_engine, Post, Comment
from typing import List, Dict
from utils.logger import logger

Session = sessionmaker(bind=database_engine)

def query_posts(limit: int) -> List[Dict]:
    """
    Helper function to query only posts
    """
    session = Session()
    post_records = []

    logger.info("Querying posts from the database...")

    try:
        posts = session.query(Post).limit(limit).all()
        for post in posts:
            post_attribute = {
                "post_number" : post.id,
                "subreddit": post.subreddit,
                "title": post.title,
                "body": post.body
            }
            post_records.append(post_attribute)
        return post_records

    except Exception as e:
        logger.error(f"Error querying posts from the database: {e}", exc_info=True)
        return []

    finally:
        session.close()


def query_comments(sub_id: str, limit: int) -> List[Dict]:
    """
    Helper function to query comments belonging to a specific post
    """
    session = Session()
    comment_records = []

    logger.info("Querying comments from the database...")

    try:
        comments = session.query(Comment).filter(Comment.submission_id == sub_id).limit(limit).all()
        for comment in comments:
            comment_attributes = {
                "author":comment.author,
                "body": comment.body,
            }
            comment_records.append(comment_attributes)
        return comment_records

    except Exception as e:
        logger.error(f"Error querying comments from the database: {e}", exc_info=True)
        return []

    finally:
        session.close()