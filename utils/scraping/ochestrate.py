from typing import Any, Dict
from utils.scraping.scraper import RedditScraper
from utils.logger import logger


def run_reddit_scraper() -> Dict[str, Any]:
    """
    Orchestrates the Reddit scraping process.
    Steps:
        1. Fetch posts
        2. Extract submission IDs
        3. Fetch comments

    Returns:
        Dictionary containing the results.
    """
    scraper = RedditScraper()

    logger.info("=== Starting Reddit scraping pipeline ===")

    posts = scraper.fetch_reddit_posts()
    if not posts:
        logger.warning("No posts were fetched. Exiting pipeline.")
        return {"posts": [], "submission_ids": [], "comments": []}

    submission_ids = scraper.fetch_post_ids()
    if not submission_ids:
        logger.warning("No submission IDs extracted. Exiting pipeline.")
        return {"posts": posts, "submission_ids": [], "comments": []}

    comments = scraper.fetch_reddit_comments()

    logger.info("=== Reddit scraping pipeline completed ===")

    return {
        "posts": posts,
        "submission_ids": submission_ids,
        "comments": comments,
    }
    
