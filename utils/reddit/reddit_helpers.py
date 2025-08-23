from utils.reddit.fetch_posts import fetch_reddit_posts



def fetch_post_ids()->list[str]:

    """
    Returns all submission ids from the `fetch_reddit_posts()` functions
    """
    submissions = fetch_reddit_posts()

    submission_ids = []

    for submission in submissions:
        submission_id = submission.get("subredditID")
        if submission_id:
            submission_ids.append(submission_id)

    return submission_ids