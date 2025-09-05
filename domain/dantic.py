from pydantic import BaseModel
from google.genai import types

class PostInfo(BaseModel):
    submission_id: str
    subreddit: str
    title: str
    body: str
    upvote_ratio: str
    score: str