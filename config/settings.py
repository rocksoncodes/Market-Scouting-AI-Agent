import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")

DEFAULT_SUBREDDITS: List[str] = ["smallbusiness"]
DEFAULT_POST_LIMIT: int = 5
DEFAULT_COMMENT_LIMIT: int = 5

SCOUT_OBJECTIVE = """
You are a market scout agent.

Your input includes multiple Reddit posts, each with:
- Title
- Body
- Subreddit
- List of comments

Your objective:
1. Group posts by subreddit.

2. For each post:
    - First, call the `run_reddit_scraper` function to collect subreddit posts.
    - Then, call the `run_sentiment_pipeline` function to analyze the comments.
    - Conclude on the audience sentiment toward the problem.
    - Check if comments indicate frequent, severe, or frustrating issues related to the post.

3. Apply selection criteria:
    a. Frequency: Are multiple users experiencing the same issue?
    b. Severity: Does the tone of comments indicate frustration or significant problems?
    c. Clarity: Is the problem clearly explained in the post?
    d. Feasibility: Can a realistic product or service solve it?

4. For each qualified post, return an XYZ-style problem statement:
   "X people face Y problem so build Z solution for W results."

5. Alongside the XYZ statement, include a sentiment statement from the analysis:
   "Sentiment statement: Sentiment towards [X: Entity/Topic] is predominantly [Y: Sentiment Label], with users [Z: Key themes, opinions, or concerns drawn from the discussion]."

6. If no posts qualify, log "No problems identified."

Output:
- Only log which posts were stored.
- An XYZ problem statement with a sentiment statement for each stored post.
- Append: "Total problems stored: <number>"
"""