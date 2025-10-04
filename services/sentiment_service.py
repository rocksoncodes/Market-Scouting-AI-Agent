import nltk
from sqlalchemy.orm import sessionmaker
from database.engine import database_engine
from database.models import Post, Sentiment
from typing import Dict, List, Any
from utils.query_helper import serialize_post, get_comments_for_post
from nltk.sentiment import SentimentIntensityAnalyzer
from utils.query_helper import get_session
from collections import Counter
from utils.logger import logger

Session = sessionmaker(bind=database_engine)

class SentimentService:
    def __init__(self):
        """
        Initialize sentiment analyzer and ensure required NLTK resources.
        """
        self.ensure_nltk_resources()
        self.session = get_session()
        self.sia = SentimentIntensityAnalyzer()
        self.limit = 1 # Limit number of posts to process

        self.query_results: List[Dict] = []
        self.extracted_comments: List[Dict] = []
        self.sentiment_result: List[Dict] = []
        
    @staticmethod
    def ensure_nltk_resources() -> None:
        """
        Download required NLTK resources if missing.
        """
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            logger.info("Downloading VADER lexicon...")
            nltk.download("vader_lexicon")


    def query_posts_with_comments(self) -> List[Dict]:
        """
        Query posts along with their comments.
        Each comment is included only if its submission_id matches the post id.
        """
        session = self.session
        post_records = []

        logger.info("Querying posts with comments from the database...")

        try:
            posts = session.query(Post).limit(self.limit).all()
            total_comments = 0

            for post in posts:
                comment_records, comment_count = get_comments_for_post(session, post.submission_id)
                total_comments += comment_count

                logger.info(f"Post {post.id} retrieved with {comment_count} comments.")
                post_records.append(serialize_post(post, comment_records))

            logger.info(
                f"Query complete. Retrieved {len(posts)} posts and {total_comments} comments in total."
            )

            self.query_results = post_records
            return post_records

        except Exception as e:
            logger.error(f"Error querying posts with comments: {e}", exc_info=True)
            self.query_results = []
            return []

        finally:
            session.close()

    def extract_comments(self) -> List[Dict[str, Any]]:
        """
        Extract raw comment data from the query results
        """

        logger.info("Extracting all comments from query results...")

        if not self.query_results:
            logger.info("No query results found, calling query_posts_with_comments()...")
            self.query_posts_with_comments()

        new_comments = []

        try:
            for data in self.query_results:
                comments = data.get("comments", [])
                for item in comments:
                    body_comment = item.get("body", "")
                    if body_comment:
                        new_comments.append({
                            "body": body_comment,
                            "submission_id": item.get("submission_id"),
                            "author": item.get("author")
                        })

            logger.info(f"Extracted {len(new_comments)} valid comment(s)")
            self.extracted_comments = new_comments
            return new_comments

        except Exception as e:
            logger.error(f"Error extracting comments from query results: {e}", exc_info=True)
            self.extracted_comments = []
            return []
    

    def analyze_sentiment(self) -> List[Dict[str, Any]]:
        """
        Run sentiment analysis on comments and return results with labels.
        """

        if not self.extracted_comments:
            logger.info("No extracted comments found, calling extract_comments()...")
            self.extract_comments()

        sentiment_results: List[Dict[str, Any]] = []
        logger.info(f"Starting sentiment analysis on {len(self.extracted_comments)} comment(s).")

        for comment in self.extracted_comments:
            try:
                text = comment.get("body", "")
                if not isinstance(text, str) or not text.strip():
                    logger.warning(f"Skipping invalid or empty comment: {comment}")
                    continue

                score = self.sia.polarity_scores(text)

                if score["compound"] > 0.05:
                    label = "Positive"
                elif score["compound"] < -0.05:
                    label = "Negative"
                else:
                    label = "Neutral"

                sentiment_results.append({
                    "submission_id": comment.get("submission_id"),
                    "sentiment": {"compound": score["compound"], "label": label}
                })

            except Exception as e:
                logger.error(f"Error analyzing comment {comment}: {e}", exc_info=True)

        self.sentiment_result = sentiment_results
        logger.info("Completed sentiment analysis. Valid result(s): %d", len(sentiment_results))
        return sentiment_results
    

    def summarize_post_sentiment(self) -> Dict:
        """
        Aggregate sentiment results for all loaded comments.
        """
        logger.info("Starting sentiment summarization...")

        if not self.sentiment_result:
            logger.info("No sentiment results found, calling analyze_sentiment()...")
            sentiment_results = self.analyze_sentiment()
        else:
            sentiment_results = self.sentiment_result

        sentiment_labels = []
        compound_scores = []

        try:
            for result in sentiment_results:
                sentiment = result.get("sentiment", {})
                if "label" in sentiment and "compound" in sentiment:
                    sentiment_labels.append(sentiment["label"])
                    compound_scores.append(sentiment["compound"])

            label_counts = Counter()
            for label in sentiment_labels:
                label_counts[label] += 1

            if compound_scores:
                average_compound = sum(compound_scores) / len(compound_scores)
            else:
                average_compound = 0.0

            if label_counts:
                dominant_sentiment = label_counts.most_common(1)[0][0]
            else:
                dominant_sentiment = "Neutral"

            summary = {
                "dominant_sentiment": dominant_sentiment,
                "avg_compound": average_compound,
                "counts": dict(label_counts),
                "total_comments": len(sentiment_results),
            }

            logger.info("Post sentiment summary: %s", summary)

        except Exception as e:
            logger.error(f"Error summarizing post sentiment: {e}")
            summary = {}

        return summary


    def store_sentiment_results(self):
        """
        Insert sentiments results into the database
        """
        session = self.session
        posts = self.query_results
        post_summary = self.summarize_post_sentiment()

        if not posts:
            self.query_posts_with_comments()
            posts = self.query_results

        if not posts:
            logger.warning("No posts available to store sentiments.")
            return

        post_key = posts[0].get("post_id")

        try:
            results = Sentiment(
                post_id = post_key,
                sentiment_results = post_summary
            )
            session.add(results)
            session.commit()

        except Exception as e:
            logger.error(f"Error storing post sentiment(s) {e}", exc_info=True)
            session.rollback()



    def marked_comments_processed(self):
        """
        Update comments as processed
        """
        pass


    def save_changes(self):
        """
        Commit all changes to the database
        """
        pass
