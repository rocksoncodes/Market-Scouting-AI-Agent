import os
import praw
from dotenv import load_dotenv
from ..utils.logger import logger


def validate_reddit_secrets(reddit_secrets):
    """
    Helper Function:
    Validate that all required Reddit environment variables are loaded.

    Logs
    ----
    - Info messages for successfully loaded variables.
    - Error messages for missing variables.
    """
    missing_keys = []
    found_keys = []

    for reddit_key, reddit_value in reddit_secrets.items():

        if reddit_value:
            found_keys.append(reddit_key)
        else:
            missing_keys.append(reddit_key)
            

    if missing_keys:
        logger.error(f"Failed to load {len(missing_keys)} environment variable(s)")
        for key in missing_keys:
            logger.info(f"Missing environment variable: {key}")
        return False
    
    if found_keys:
        logger.info(f" {len(found_keys)} reddit environment variables were loaded successfully")
    
    return True


def connect_to_reddit():
    """
    Load environment variables, validate them and establish a Reddit connection.

    Logs
    ----
    - Info messages when the connection is successful.
    - Error messages when environment variables are missing or validation fails.
    """
    
    load_dotenv()
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    reddit_secrets = {
        "REDDIT_CLIENT_ID": client_id, 
        "REDDIT_CLIENT_SECRET": client_secret, 
        "REDDIT_USER_AGENT": user_agent
    }

    if not validate_reddit_secrets(reddit_secrets):
        logger.error("Connection to Reddit failed due to missing environment variable(s)")
        return None
        
    reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    user_agent = user_agent
    )

    logger.info("Connection to Reddit successful!")
    return reddit