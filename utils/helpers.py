from sqlalchemy.orm import Session
from typing import List, Dict, Tuple
from database.models import Comment, Post


def serialize_comment(comment: Comment) -> Dict:
    return {
        "comment_id": comment.id,
        "post_key": comment.submission_id,
        "body": comment.body,
        "author": comment.author,
        "score": comment.score,
    }


def serialize_post(post: Post, comments: List[Dict]) -> Dict:
    return {
        "post_number": post.id,
        "post_key":post.submission_id,
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


def ensure_data_integrity(session: Session, reddit_data) -> list:
    """
    Returns a list of submission_ids that do NOT exist in the database.
    """
    posts_list = reddit_data.get("posts", [])
    submission_ids_from_posts = []

    for post in posts_list:
        submission_ids_from_posts.append(post["submission_id"])

    if len(submission_ids_from_posts) == 0:
        return []

    query_results = session.query(Post.submission_id).filter(Post.submission_id.in_(submission_ids_from_posts)).all()

    existing_submission_ids = set()
    for record in query_results:
        existing_submission_ids.add(record[0])

    new_submission_ids = []
    for submission_id in submission_ids_from_posts:
        if submission_id not in existing_submission_ids:
            new_submission_ids.append(submission_id)

    return new_submission_ids