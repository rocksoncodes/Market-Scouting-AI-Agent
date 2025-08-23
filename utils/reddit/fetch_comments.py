from utils.logger import logger
from services.reddit_service import connect_to_reddit
from utils.reddit.reddit_helpers import fetch_post_ids


reddit = connect_to_reddit()


def fetch_subreddit_comments():
    """
    Fetch all subreddit comments from a single Reddit submission
    """

    submission_ids = fetch_post_ids()

    comments_collected = []
    logger.info(f"Fetching Post comments")

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

        logger.info(f"Collected {len(comments_collected)} comments")
        return comments_collected
    
    except Exception as e:
       logger.error(f"Failed to fetch Reddit comments: {e}")
       return None