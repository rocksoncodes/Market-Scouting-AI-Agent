from typing import Any, Dict
from domain.coordinate import RedditCoordinate
from utils.logger import logger


def scrape_and_store() -> None:
    execute = RedditCoordinate()
    
    reddit_data = execute.run_reddit_scraper()
    execute.run_reddit_storage(reddit_data) 