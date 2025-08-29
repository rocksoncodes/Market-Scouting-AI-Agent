from typing import Dict, List
from utils.logger import logger
from services.reddit_service import connect_to_reddit_singleton


reddit = connect_to_reddit_singleton()


def fetch_reddit_posts() -> List[Dict[str:str]]:
    """
    Use fetch_reddit_posts when you want to retrieve current Reddit discussions for analyzing small business problems and challenges.

    This function uses predefined settings:
    - No parameters required - call directly when you need current posts

    Returns:
        dict: Contains list of posts with title, body, subreddit, and upvote_ratio
    """

    subreddit_list: str = ["startups"]
    limit: int = 20
    posts = []

    for subreddit_name in subreddit_list:
        logger.info(f" Fetching posts from '{subreddit_name}' subreddit.")
        subreddit_posts = list(reddit.subreddit(subreddit_name).hot(limit=limit))
        logger.info(f" Retrieved {len(subreddit_posts)} posts from '{subreddit_name}' subreddit.")

    try:
        for submission in subreddit_posts:
            posts.append({
                "subreddit": subreddit_name,
                "subredditID": submission.id,
                "title": submission.title,
                "body": submission.selftext,
                "upvote_ratio": submission.upvote_ratio
            })

        logger.info(f"Completed fetching posts. Total posts collected: {len(posts)}")
        return posts
    
    except Exception as e:
        logger.error(f"Failed to fetch Reddit posts: {e}")
        return []
    