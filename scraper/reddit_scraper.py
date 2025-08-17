from utils.logger import logger
from utils.reddit_connection import connect_to_reddit

reddit = connect_to_reddit()

subreddit_list = [
        "startups", 
        "Entrepreneur", 
        "smallbusiness",
        "freelance",
        "Productivity",
        "sidehustle"
]
        
        
# TODO: Extend this function to return posts from reddit:
def fetch_reddit_posts(subreddit_list):
    """
     Fetch the top posts from a list of subreddits and print their titles.
    """

    try:
        for subreddit in subreddit_list:
            print(f"{subreddit.title()} Subreddit:")
            for submission in reddit.subreddit(subreddit).hot(limit=5):
                print(f"{submission.title}")
            print(f"\n")
    except Exception:
        logger.error("Cannot fetch posts because Reddit connection failed.")
        return None
    