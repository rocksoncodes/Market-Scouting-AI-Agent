from domain.scraper import RedditScraper
from domain.storage import RedditStorage
from typing import Dict, Any
from utils.logger import logger

class RedditCoordinate:
    def __init__(self):
        self.scraper = RedditScraper()
        self.storage = RedditStorage()
        
        
    def run_reddit_scraper(self) -> Dict[str, Any]:
        """
        Orchestrates the Reddit scraping process.
        """

        logger.info("=== Starting Reddit scraping pipeline ===")

        logger.info("[PIPELINE] Step 1/3: Fetching posts")
        posts = self.scraper.fetch_reddit_posts()
        
        if not posts:
            logger.warning("No posts were fetched. Exiting pipeline.")
            return {"posts": [], "submission_ids": [], "comments": []}

        logger.info("[PIPELINE] Step 2/3: Extracting submission IDs")
        submission_ids = self.scraper.fetch_post_ids()
        
        if not submission_ids:
            logger.warning("No submission IDs extracted. Exiting pipeline.")
            return {"posts": posts, "submission_ids": [], "comments": []}
        
        logger.info("[PIPELINE] Step 3/3: Fetching comments")
        comments = self.scraper.fetch_reddit_comments()
        
        if not comments:
            logger.warning("No comments were fetched. Exiting pipeline.")
            return {"posts": posts, "submission_ids": submission_ids, "comments": []}

        logger.info("=== Reddit scraping pipeline completed ===")

        return {
            "posts": posts,
            "submission_ids": submission_ids,
            "comments": comments,
        }
    
    
    def run_reddit_storage(self, reddit_data: Dict):
        """
        Orchestrates the Reddit storage process with error handling.
        """

        logger.info("=== Starting Reddit storage pipeline ===")

        logger.info("[PIPELINE] Step 1/2: Storing posts")
        try:
            self.storage.store_posts(reddit_data)

        except Exception as e:
            logger.error(f"Unexpected error while storing posts: {e}", exc_info=True)
            return

        logger.info("[PIPELINE] Step 2/2: Storing comments")
        try:
            self.storage.store_comments(reddit_data)
            
        except Exception as e:
            logger.error(f"Unexpected error while storing comments: {e}", exc_info=True)

        logger.info("=== Reddit storage pipeline completed ===")
    