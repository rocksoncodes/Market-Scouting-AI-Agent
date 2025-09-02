from typing import Dict, List, Any
from utils.logger import logger
from services.reddit_service import connect_to_reddit_singleton


reddit = connect_to_reddit_singleton()

"""
TODO: Make sure the code iterates through
the subreddit list returns their posts
"""

      
def fetch_reddit_posts() -> List[Dict[str, Any]]:
    """
    Fetch current Reddit discussions from multiple subreddits.
    """
    subreddit_list: List[str] = ["smallbusiness", "freelance","recruitinghell"]
    limit: int = 5
    posts: List[Dict[str, Any]] = []

    for subreddit_name in subreddit_list:
        logger.info(f"Fetching posts from '{subreddit_name}' subreddit.")
        try:
            subreddit_posts = list(reddit.subreddit(subreddit_name).hot(limit=limit))
            logger.info(f"Retrieved {len(subreddit_posts)} posts from '{subreddit_name}' subreddit.")

            for submission in subreddit_posts:
                posts.append({
                    "subreddit": subreddit_name,
                    "subredditID": submission.id,
                    "title": submission.title,
                    "body": submission.selftext,
                    "upvote_ratio": submission.upvote_ratio
                })

        except Exception as e:
            logger.error(f"Failed to fetch posts from '{subreddit_name}': {e}")

    logger.info(f"Completed fetching posts. Total posts collected: {len(posts)}")
    return posts

    