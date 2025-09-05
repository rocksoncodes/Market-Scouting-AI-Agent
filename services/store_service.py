from sqlalchemy.orm import sessionmaker
from database.models import database_engine, Post, Comment
from utils.logger import logger


SessionLocal = sessionmaker(bind=database_engine)


def store_reddit_data(reddit_data: dict):
    """
    Stores validated Reddit posts and comments into the database.
    Returns a summary of how many were stored.
    """
    session = SessionLocal()
    stored_posts = 0
    stored_comments = 0

    try:
        for post_data in reddit_data.get("posts", []):
            post = Post(
                submission_id=post_data["submission_id"],
                subreddit=post_data.get("subreddit", ""),
                title=post_data.get("title", ""),
                body=post_data.get("body", ""),
                upvote_ratio=post_data.get("upvote_ratio", 0.0),
                score=post_data.get("score", 0)
            )
            session.add(post)
            stored_posts += 1

        for comment_data in reddit_data.get("comments", []):
            comment = Comment(
                submission_id=comment_data["submission_id"],
                author=comment_data.get("author", ""),
                body=comment_data.get("body", ""),
                score=comment_data.get("score", 0)
            )
            session.add(comment)
            stored_comments += 1

        session.commit()
        logger.info(f"Stored {stored_posts} posts and {stored_comments} comments.")
        return {"posts_stored": stored_posts, "comments_stored": stored_comments}

    except Exception as e:
        session.rollback()
        logger.error(f"Error storing Reddit data: {e}", exc_info=True)
        return {"error": str(e)}

    finally:
        session.close()
