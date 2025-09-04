from typing import List, Dict
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter

from services.scraper_service import run_reddit_scraper
from utils.logger import logger


class RedditSentiment:
    def __init__(self):
        """
        Initialize sentiment analyzer and ensure required NLTK resources.
        """
        self.ensure_nltk_resources()
        self.comments: List[Dict[str, str]] = []
        self.sia = SentimentIntensityAnalyzer()
        

    def ensure_nltk_resources(self) -> None:
        """
        Download required NLTK resources if missing.
        """
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            logger.info("Downloading VADER lexicon...")
            nltk.download("vader_lexicon")
            

    def fetch_and_validate_comments(self) -> List[Dict[str, str]]:
        """
        Use RedditScraper to fetch posts and comments.
        """
        scraper = run_reddit_scraper()
        comments = scraper.get("comments")

        if not isinstance(comments, list):
            raise TypeError("Expected a list of comment dictionaries.")

        self.comments = comments
        return comments
    

    def analyze_sentiment(self) -> List[Dict[str, str]]:
        """
        Run sentiment analysis on comments and return results with labels.
        """
        if not self.comments:
            self.fetch_and_validate_comments()

        sentiment_results: List[Dict[str, str]] = []

        for comment in self.comments:
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
                    "author": comment.get("author"),
                    "text": text,
                    "sentiment": {"compound": score["compound"], "label": label}
                })

            except Exception as e:
                logger.error(f"Error analyzing comment {comment}: {e}")

        return sentiment_results
    

    def summarize_post_sentiment(self) -> Dict:
        """
        Aggregate sentiment results for all loaded comments.
        """
        sentiment_results = self.analyze_sentiment()

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

        return {"summary": summary}
