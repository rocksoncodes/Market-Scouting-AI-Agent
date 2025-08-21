from utils.logger import logger
from services.reddit_service import connect_to_reddit


reddit = connect_to_reddit()


def fetch_reddit_posts() -> dict:
    """
    Use fetch_reddit_posts when you want to retrieve current Reddit discussions for analyzing small business problems and challenges.

    This function uses predefined settings:
    - No parameters required - call directly when you need current posts

    Returns:
        dict: Contains list of posts with title, body, subreddit, and upvote_ratio
    """
    subreddit_list: str = ["smallbusiness"]
    limit: int = 10
    posts = []

    try:
        for subreddit in subreddit_list:
            for submission in reddit.subreddit(subreddit).hot(limit=limit):
                post = {
                    "subreddit": subreddit,
                    "title":submission.title,
                    "body": submission.selftext,
                    "upvote_ratio": submission.upvote_ratio
                }
                posts.append(post)
        return posts
    
    except Exception as e:
        logger.error(f"Failed to fetch Reddit Posts: {e}")
        return None