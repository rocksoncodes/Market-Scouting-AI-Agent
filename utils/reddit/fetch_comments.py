from utils.logger import logger
from services.reddit_service import connect_to_reddit


reddit = connect_to_reddit()


def fetch_subreddit_comments(submission, comment_limit):
    """
    Fetch all subreddit comments from a single Reddit submission
    """

    comments_collected = []
    logger.info(f"Fetching post comments for; {submission.title}")

    try:
        submission.comments.replace_more(comment_limit)

        count = 0
        for comment in submission.comments.list():
            if comment.body and comment.body != "[deleted]":
                comments_collected.append({
                    "author": str(comment.author),
                    "body": comment.body,
                    "score": comment.score
                })

                count += 1
                if comment_limit and count >= comment_limit:
                    break


        logger.info(f"Collected {len(comments_collected)} comments")
        return comments_collected
    
    except Exception as e:
       logger.error(f"Failed to fetch Reddit comments: {e}")
       return None