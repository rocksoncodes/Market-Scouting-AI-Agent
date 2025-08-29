from utils.logger import logger
from services.reddit_service import connect_to_reddit_singleton
from utils.reddit.reddit_helpers import fetch_post_ids


reddit = connect_to_reddit_singleton()


def fetch_reddit_comments()->list[dict]:
    """
    Fetch all subreddit comments from a list of Reddit submissions.
    Returns a list of dictionaries with comment data.
    """

    function_name = "fetch_reddit_comments()"

    submission_ids = fetch_post_ids()
    if not submission_ids:
        logger.warning(f"[{function_name}] No submission IDs found. Returning empty list.")
        return []

    comments_collected = []
    logger.info(f"Fetching post comments from {len(submission_ids)} submissions.")

    try:
        for submission_id in submission_ids:
            submission = reddit.submission(id=submission_id)
            submission.comments.replace_more(limit=None)

            count = 0
            for comment in submission.comments.list():
                if comment.body and comment.body != "[deleted]":
                    comments_collected.append({
                        "title":submission.title,
                        "author": str(comment.author),
                        "body": comment.body,
                        "score": comment.score
                    })
                    count += 1

        logger.info(f"Completed. Total comments collected: {len(comments_collected)}")
        return comments_collected
    
    except Exception as e:
       logger.error(f"Failed to fetch Reddit comments: {e}")
       return []
   
   
   