import os
import praw
from dotenv import load_dotenv
from utils.logger import logger


def validate_reddit_secrets(reddit_secrets: dict) -> bool:
    """
    Validate presence of Reddit API environment variables.
    Returns True if all secrets are found, otherwise False.
    """
    missing_keys = []
    found_keys = []

    for reddit_key, reddit_value in reddit_secrets.items():
        if reddit_value:
            found_keys.append(reddit_key)
        else:
            missing_keys.append(reddit_key)
            
    if missing_keys:
        logger.error(f"Failed to load {len(missing_keys)} Reddit environment variable(s)")
        for key in missing_keys:
            logger.info(f"Missing Reddit environment variable: {key}")
        return False
    
    if found_keys:
        logger.info(f" {len(found_keys)} Reddit environment variables were loaded successfully")
    
    return True


def connect_to_reddit():
    """
    Connect to Reddit API using PRAW and environment variables.
    Returns a Reddit instance if successful, otherwise None.
    """
    load_dotenv()

    reddit_secrets = {
        "REDDIT_CLIENT_ID": os.getenv("REDDIT_CLIENT_ID"),
        "REDDIT_CLIENT_SECRET": os.getenv("REDDIT_CLIENT_SECRET"), 
        "REDDIT_USER_AGENT": os.getenv("REDDIT_USER_AGENT")
    }

    if not validate_reddit_secrets(reddit_secrets):
        logger.error("Connection to the Reddit API failed due to missing environment variable(s)")
        return None
        
    try:
        reddit = praw.Reddit(
        client_id = reddit["REDDIT_CLIENT_ID"],
        client_secret = reddit["REDDIT_CLIENT_SECRET"],
        user_agent = reddit["REDDIT_USER_AGENT"]
        )
        logger.info("Connection to the Reddit API was successful!")
        return reddit
    except Exception as e:
        logger.exception(f"Failed to initialize Reddit client: {e}")
        return None