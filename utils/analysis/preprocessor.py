import string
from typing import List, Dict

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from utils.reddit.fetch_comments import fetch_reddit_comments
from utils.logger import logger


class RedditCommentPreprocessor:
    def __init__(self):
        """Initialize and ensure necessary NLTK resources are available."""
        self.ensure_nltk_resources()
        self.comments: List[Dict[str, str]] = []
        self.processed_data: List[List[str]] = []
        

    def ensure_nltk_resources(self) -> None:
        """Download required NLTK resources if missing."""
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            logger.info("Downloading missing NLTK resources...")
            nltk.download('punkt')
            nltk.download('stopwords')
            
            
    def fetch_and_validate_comments(self) -> List[Dict[str, str]]:
        """Fetch comments and validate the response."""
        comments = fetch_reddit_comments()
        if not isinstance(comments, list):
            raise TypeError("Expected a list of comment dictionaries.")
        self.comments = comments
        return comments
    
    
    def tokenize_comments(self) -> List[List[str]]:
        """Fetch comments (if not already fetched) and tokenize them into lists of words."""
        try:
            if not self.comments:
                self.fetch_and_validate_comments()

            tokens = []
            for comment in self.comments:
                body = comment.get("body", "")
                if not isinstance(body, str):
                    logger.warning(f"Skipping invalid comment body: {body}")
                    continue
                tokens.append(word_tokenize(body))

            self.processed_data = tokens
            logger.info(f"Tokenized {len(tokens)} comments successfully.")
            return tokens

        except Exception as e:
            logger.error(f"Error during tokenization: {e}", exc_info=True)
            return []
        
    
    def remove_punctuation(self) -> list[list[str]]:
        """Remove punctuation from previously tokenized comments."""
        try:
            if not self.processed_data:
                self.tokenize_comments()

            cleaned_comments = []
            for comment_tokens in self.processed_data:
                cleaned_comment = []
                for token in comment_tokens:
                    if token not in string.punctuation:
                        cleaned_comment.append(token)
                cleaned_comments.append(cleaned_comment)

            self.processed_data = cleaned_comments
            logger.info(f"Removed punctuation from comments. Total comments: {len(cleaned_comments)}")
            return cleaned_comments

        except Exception as e:
            logger.error(f"Error during punctuation removal: {e}", exc_info=True)
            return []
        
        
    def remove_stopwords(self) -> List[List[str]]:
        """Removes stopwords from a list of tokens"""
        try:
            stop_words = set(stopwords.words("english"))
            filtered_lists = []
            
            if not self.processed_data:
                self.remove_punctuation()
                
            for sublist in self.processed_data:
                filtered_list = []
                for token in sublist:
                    if token.lower() not in stop_words:
                        filtered_list.append(token)
                filtered_lists.append(filtered_list)
                        
            logger.info(f"Stopword removal completed. Total words after filtering: {len(filtered_lists)}")
            return filtered_lists
        
        except Exception as e:
            logger.error(f"Error during stopwrord removal: {e}", exc_info=True)
            return []