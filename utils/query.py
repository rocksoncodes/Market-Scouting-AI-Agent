from typing import List, Dict, Tuple
from database.models import Comment, Post

def serialize_comment(comment: Comment) -> Dict:
    return {
        "comment_id": comment.id,
        "body": comment.body,
        "author": comment.author,
        "score": comment.score,
    }


def serialize_post(post: Post, comments: List[Dict]) -> Dict:
    return {
        "post_number": post.id,
        "subreddit": post.subreddit,
        "title": post.title,
        "body": post.body,
        "comments": comments,
    }


def get_comments_for_post(session, post_id: str) -> Tuple[List[Dict], int]:
    comments = (
        session.query(Comment)
        .filter(Comment.submission_id == post_id)
        .all()
    )

    comment_records = []
    count = 0
    for comment in comments:
        comment_records.append(serialize_comment(comment))
        count += 1

    return comment_records, count
