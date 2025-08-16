from utils.logger import logger
from scrapper.reddit_scrapper import fetch_reddit_posts

def main():
    """
    Main execution function for fetching Reddit posts.
    """
    subreddit_names = ["freelance", "Entrepreneur", "smallbusiness"]

    fetch_reddit_posts(subreddit_names)


if __name__ == "__main__":
    main()