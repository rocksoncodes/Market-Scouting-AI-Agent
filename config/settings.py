import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

# =====================================================
# REDDIT CONFIGURATION
# =====================================================
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")


# =====================================================
# NOTION CONFIGURATION
# =====================================================
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")


# =====================================================
# AGENT CONFIGURATION
# =====================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# =====================================================
# DATABASE CONFIGURATION
# =====================================================
DATABASE_URL = os.getenv("DATABASE_URL")


# =====================================================
# REDDIT DATA INGESTION SETTINGS
# =====================================================
DEFAULT_SUBREDDITS: List[str] = [
    "Entrepreneur",
    "smallbusiness",
    "Business_Ideas",
    "ghana"
]
DEFAULT_POST_LIMIT: int = 200
DEFAULT_COMMENT_LIMIT: int = 150


# =====================================================
# REDDIT DATA FILTERING REQUIREMENTS
# =====================================================
MIN_COMMENTS = 50
MIN_SCORE = 75
MIN_UPVOTE_RATIO = 0.8


# =====================================================
# AGENT SETTINGS AND OBJECTIVES
# =====================================================
AGENT_MODEL = "gemini-2.5-flash"
SCOUT_OBJECTIVE = """
You are a market scout agent.

Your input will come directly from the database using the `feeder()` function.

Each record returned by that method includes:
- Post Number
- Title
- Body
- Subreddit
- Sentiment Score (counts, average compound, dominant sentiment)

Your new workflow:

1. Call the `feeder()` function to retrieve all posts and their associated sentiment summaries.

2. Group the retrieved posts by subreddit for contextual analysis.

3. For each post:
   - Interpret the sentiment data to understand audience tone and emotional intensity.
   - Identify whether the discussion highlights a common or critical market problem.

5. For each post, return an XYZ-style problem statement:
   "X people face Y problem so build Z solution for W results."

6. Accompany each with a sentiment statement:
   "Sentiment statement: Sentiment towards [X: Entity/Topic] is predominantly [Y: Sentiment Label], with users [Z: Key themes, opinions, or concerns drawn from the discussion]."

Output:
- Log which posts were analyzed.
- Return the XYZ problem statements and their sentiment statements.
- Conclude: "Total problems stored: <number>"
"""