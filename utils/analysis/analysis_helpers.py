import string
from typing import List, Dict

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from utils.reddit.fetch_comments import fetch_reddit_comments
from utils.logger import logger


# Ensure necessary NLTK resources
def ensure_nltk_resources():
    """Download required NLTK resources if missing."""
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        logger.info("Downloading missing NLTK resources...")
        nltk.download('punkt')
        nltk.download('stopwords')


def fetch_and_validate_comments() -> List[Dict[str, str]]:
    """Fetch comments and validate the response."""
    comments = fetch_reddit_comments()
    if not isinstance(comments, list):
        raise TypeError("Expected a list of comment dictionaries.")
    return comments


def tokenize_comments() -> List[List[str]]:
    """Fetch comments and tokenize them into lists of words."""
    try:
        comment_collectible = fetch_and_validate_comments()
        tokens = []
        
        for comment in comment_collectible:
            body = comment.get("body", "")
            if not isinstance(body, str):
                logger.warning(f"Skipping invalid comment body: {body}")
                continue
            
            tokens.append(word_tokenize(body))

        logger.info(f"Tokenized {len(tokens)} comments successfully.")
        return tokens

    except Exception as e:
        logger.error(f"Error during tokenization: {e}", exc_info=True)
        return []


def remove_punctuation() -> str:
    """Tokenize comments and remove punctuation."""
    try:
        tokenized_comments = tokenize_comments()
        if not tokenized_comments:
            logger.warning("No tokenized comments available to process.")
            return ""

        filtered_tokens = []
        for comment_tokens in tokenized_comments:
            for word in comment_tokens:
                if word not in string.punctuation:
                    filtered_tokens.append(word)

        processed_comments = " ".join(filtered_tokens)
        logger.info(f"Processed comments length: {len(processed_comments)} characters.")
        return processed_comments

    except Exception as e:
        logger.error(f"Error during punctuation removal: {e}", exc_info=True)
        return ""


def remove_stopwords() -> List[str]:
    """
    Removes stop words from a list of subreddit comments.
    Returns a list of words with stopwords removed.
    Raises ValueError if no comments are available.
    """
    function_name = "remove_stopwords()"

    try:
        comments_list = fetch_reddit_comments()
        if not comments_list:
            raise ValueError(f"[{function_name}] No comments available for stopword removal.")


        stop_words = set(stopwords.words("english"))
        filtered_data = []

        logger.info("Starting stopword removal process.")
        for submission_item in comments_list:
            comment_body = submission_item.get("body", "")
            if not comment_body.strip():
                continue

            tokenized_data = word_tokenize(comment_body)

            for word in tokenized_data:
                if word.lower() not in stop_words:
                    filtered_data.append(word)

        logger.info(f"Stopword removal completed. Total words after filtering: {len(filtered_data)}")
        return filtered_data
    
    except LookupError as e:
        logger.error(f"Missing NLTK resources: {e}. Suggest running nltk.download('stopwords')")
        return []

    except (NameError, TypeError, AttributeError) as e:
        logger.error(f"Failed to remove stopwords from data: {e}")
        return[]

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return[]


# Initialize NLTK resources
ensure_nltk_resources()