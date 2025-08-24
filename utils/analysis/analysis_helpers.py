import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import List
from utils.reddit.fetch_comments import fetch_reddit_comments
from utils.logger import logger


def remove_stopwords() -> List[str]:
    """
    Removes stop words from a list of subreddit comments.
    Returns a list of words with stopwords removed.
    Raises ValueError if no comments are available.
    """

    function_name = "remove_stopwords"

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
