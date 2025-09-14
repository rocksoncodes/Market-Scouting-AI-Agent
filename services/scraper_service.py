from typing import Any, Dict
from domain.coordinate import RedditCoordinate
from utils.logger import logger

execute = RedditCoordinate()

def scrape_reddit_data() -> Dict[str, Any]:
    reddit_data = execute.run_reddit_scraper()
    return reddit_data


def store_reddit_data(reddit_data: Dict[str, Any]) -> None:
    execute.run_reddit_storage(reddit_data)