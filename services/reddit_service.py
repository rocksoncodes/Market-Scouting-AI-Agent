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

    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    reddit_secrets = {
        "REDDIT_CLIENT_ID":  client_id,
        "REDDIT_CLIENT_SECRET": client_secret, 
        "REDDIT_USER_AGENT": user_agent
    }

    if not validate_reddit_secrets(reddit_secrets):
        logger.error("Connection to the Reddit API failed due to missing environment variable(s)")
        return None
        
    try:
        reddit = praw.Reddit(
        ratelimit_seconds = 2,
        client_id =  client_id,
        client_secret = client_secret,
        user_agent = user_agent
        )
        logger.info("Connection to the Reddit API was successful!")
        return reddit
    except Exception as e:
        logger.exception(f"Failed to initialize Reddit client: {e}")
        return None