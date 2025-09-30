from services.sentiment_service import SentimentService
from utils.logger import logger


def execute_sentiment_pipeline() -> dict:
    """
    Perform sentiment analysis on Reddit post comments.
    Returns a summary of sentiment analysis results.
    """
    try:
        logger.info("Starting sentiment pipeline...")
        
        processor = SentimentService()
        processor.query_posts_with_comments()
        processor.extract_comments()
        processor.analyze_sentiment()
        summary = processor.summarize_post_sentiment()

        sentiment_results = {
            "post_sentiment": summary,
        }
        
        logger.info("Sentiment pipeline completed successfully.")
        return sentiment_results

    except Exception as e:
        logger.error(f"Error in sentiment pipeline: {e}", exc_info=True)
        return {"error": str(e)}
