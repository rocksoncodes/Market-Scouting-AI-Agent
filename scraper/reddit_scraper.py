from utils.logger import logger
from services.reddit_service import connect_to_reddit


reddit = connect_to_reddit()


def fetch_reddit_posts(subreddit_list: list[str], limit: int) -> dict:
    """
    Fetch the top posts from a list of subreddits and return their data.
        
    Returns:
        dict: Dictionary containing post data with keys:
              - subreddit: name of the subreddit
              - title: post title
              - body: post content (selftext)
              - upvote_ratio: ratio of upvotes to total votes
              Returns None if Reddit connection fails.
    """

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