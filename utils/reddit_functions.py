from utils.logger import logger
from services.reddit_service import connect_to_reddit


reddit = connect_to_reddit()


def fetch_reddit_posts() -> dict:
    subreddit_list = ["smallbusiness"]
    limit = 10
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
        logger.error(f"Cannot fetch because Reddit connection failed: {e}")
        return None