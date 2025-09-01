import string
from typing import List, Dict

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

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
        nltk_resources = {
            'tokenizers/punkt': 'punkt',
            'corpora/stopwords': 'stopwords',
            'corpora/wordnet': 'wordnet',
            'taggers/averaged_perceptron_tagger': 'averaged_perceptron_tagger'
        }
        
        for path, name in nltk_resources.items():
            try:
                nltk.data.find(path)
            except LookupError:
                logger.info(f"Downloading missing NLTK resource: {name}...")
                nltk.download(name)
            
            
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
        
    
    def remove_punctuation(self) -> List[List[str]]:
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
            if not self.processed_data:
                self.remove_punctuation()
                
            filtered_lists = []
            for sublist in self.processed_data:
                filtered_list = []
                for token in sublist:
                    if token.lower() not in stop_words:
                        filtered_list.append(token)
                filtered_lists.append(filtered_list)
            
            self.processed_data = filtered_lists    
            logger.info(f"Stopword removal completed. Total words after filtering: {len(filtered_lists)}")
            return filtered_lists
        
        except Exception as e:
            logger.error(f"Error during stopword removal: {e}", exc_info=True)
            return []
        
    
    @staticmethod
    def get_wordnet_pos(treebank_tag: str) -> str:
        """Map NLTK POS tags (Treebank) to WordNet POS tags."""
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
        
        
    def lemmatize_tokens(self) -> List[List[str]]:
        """Lemmatizes all tokens in processed_data using WordNet POS tags and returns them as a list of lists."""
        try:
            lemmatizer = WordNetLemmatizer()
            lemmatized_results: List[List[str]] = []

            if not self.processed_data:
                self.remove_stopwords()

            total_words = 0
            for sublist in self.processed_data:
                sublist_token_tags = nltk.pos_tag(sublist)

                lemmatized_tokens = []
                for word, speech_tag in sublist_token_tags:
                    wordnet_speech_tag = self.get_wordnet_pos(speech_tag) 
                    lemma = lemmatizer.lemmatize(word, wordnet_speech_tag)
                    lemmatized_tokens.append(lemma)

                total_words += len(lemmatized_tokens)
                lemmatized_results.append(lemmatized_tokens)

            self.processed_data = lemmatized_results
            logger.info(f"Lemmatization completed. Total words lemmatized after processing: {total_words}")
            return lemmatized_results
        
        except Exception as e:
            logger.error(f"Error during lemmatization: {e}", exc_info=True)
            return []