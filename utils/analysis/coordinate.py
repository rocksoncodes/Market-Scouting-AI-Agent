
from utils.analysis.sentiment import RedditCommentSentiment
from utils.logger import logger

def run_sentiment_pipeline() -> dict:
    """
    Perform sentiment analysis on Reddit post comments.

    This function coordinates the RedditCommentSentiment class methods to:
    1. Fetch post comments internally.
    2. Analyze sentiment for each comment.
    3. Summarize the overall sentiment for the post.

    Returns:
        dict: {
            "summary": { ... },   # Aggregated sentiment summary for the post
            "comments": [ ... ]   # List of per-comment sentiment results
        }

    Notes for AI use:
    - Call this function to get the sentiment data for a post.
    - The function automatically fetches the comments; no separate comment input is needed.
    - Use the returned summary to conclude audience sentiment.
    """
    try:
        logger.info("Starting sentiment pipeline...")
        
        processor = RedditCommentSentiment()
        processor.fetch_and_validate_comments()
        per_comment = processor.analyze_sentiment()
        summary = processor.summarize_post_sentiment()

        payload = {
            "summary": summary,
            "comments": per_comment
        }
        
        logger.info("Sentiment pipeline completed successfully.")
        return payload

    except Exception as e:
        logger.error(f"Error in sentiment pipeline: {e}", exc_info=True)
        return {"error": str(e)}
