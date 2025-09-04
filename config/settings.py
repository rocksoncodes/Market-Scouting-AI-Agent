import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

DEFAULT_SUBREDDITS: List[str] = ["smallbusiness"]
DEFAULT_POST_LIMIT: int = 5
DEFAULT_COMMENT_LIMIT: int = 5