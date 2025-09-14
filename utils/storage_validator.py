from sqlalchemy.orm import Session
from database.models import Post

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