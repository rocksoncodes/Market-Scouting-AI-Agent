from typing import Dict, List, Any
from config import settings
from utils.logger import logger
from services.reddit_service import connect_to_reddit_singleton


class RedditScraper:
    def __init__(self):
        self.reddit = connect_to_reddit_singleton()
        
        self.subreddits: List[str] = settings.DEFAULT_SUBREDDITS
        self.post_limit: int = settings.DEFAULT_POST_LIMIT
        self.comment_limit: int = settings.DEFAULT_COMMENT_LIMIT
        
        self.posts: List[Dict[str, Any]] = []
        self.submission_ids: List[str] = []
        self.comments: List[Dict[str, Any]] = []
         

    def fetch_reddit_posts(self) -> List[Dict[str, Any]]:
        """
        Fetch Reddit posts from default subreddits.
        Returns:
            List of post dictionaries.
        """
        if not self.reddit:
            logger.warning("Reddit client not found. Reconnecting...")
            self.reddit = connect_to_reddit_singleton()

        posts: List[Dict[str, Any]] = []

        for subreddit_name in self.subreddits:
            logger.info(f"Fetching posts from r/{subreddit_name} (limit={self.post_limit})...")
            try:
                subreddit_posts = list(self.reddit.subreddit(subreddit_name).hot(limit=self.post_limit))
                logger.info(f"Retrieved {len(subreddit_posts)} posts from r/{subreddit_name}.")

                for submission in subreddit_posts:
                    post_data: Dict[str, Any] = {
                        "subreddit": subreddit_name,
                        "submission_id": submission.id,
                        "title": submission.title,
                        "body": submission.selftext,
                        "upvote_ratio": submission.upvote_ratio,
                        "score": submission.score
                    }
                    posts.append(post_data)

            except Exception as e:
                logger.error(f"Error fetching posts from r/{subreddit_name}: {e}", exc_info=True)

        self.posts = posts
        logger.info(f"Completed fetching posts. Total collected: {len(posts)}")
        return posts
    

    def fetch_post_ids(self) -> List[str]:
        """
        Extracts submission IDs from stored posts.
        Returns:
            List of submission IDs.
        """
        if not self.posts:
            logger.warning("No posts available. Run fetch_reddit_posts() first.")
            return []

        submission_ids: List[str] = []

        for post in self.posts:
            if "submission_id" in post:
                submission_id = post["submission_id"]
                submission_ids.append(submission_id)

        self.submission_ids = submission_ids
        logger.info(f"Extracted {len(submission_ids)} submission IDs.")
        return submission_ids
    

    def fetch_reddit_comments(self) -> List[Dict[str, Any]]:
        """
        Fetch comments for stored submission IDs using default comment limit.
        Returns:
            List of comment dictionaries.
        """
        if not self.submission_ids:
            logger.warning("No submission IDs available. Run fetch_post_ids() first.")
            return []

        comments_collected: List[Dict[str, Any]] = []
        logger.info(f"Fetching comments from {len(self.submission_ids)} submissions...")

        for submission_id in self.submission_ids:
            try:
                submission = self.reddit.submission(id=submission_id)
                submission.comments.replace_more(limit=0)

                comments = submission.comments.list()
                if self.comment_limit:
                    comments = comments[:self.comment_limit]

                count = 0
                for comment in comments:
                    if not comment.body or comment.body in ("[deleted]", "[removed]"):
                        continue

                    comment_data: Dict[str, Any] = {
                        "submission_id": submission.id,
                        "title": submission.title,
                        "author": str(comment.author) if comment.author else "Unknown",
                        "body": comment.body,
                        "score": comment.score
                    }
                    comments_collected.append(comment_data)
                    count += 1

                logger.info(f"Collected {count} comments from post '{submission.title[:30]}...'")

            except Exception as e:
                logger.error(f"Error fetching comments for submission {submission_id}: {e}", exc_info=True)

        self.comments = comments_collected
        logger.info(f"Completed. Total comments collected: {len(comments_collected)}")
        return comments_collected
