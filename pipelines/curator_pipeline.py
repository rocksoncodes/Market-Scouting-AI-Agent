from services.curator_service import Curator

execute = Curator()

def feeder():
    """
    Call the Feeder function to obtain posts and their sentiment analysis results.
    Each record in the returned list contains a post and its sentiment score.
    Use this information to guide your next actions, generate summaries, or perform analysis as required.
    """
    return execute.query_posts_with_sentiments()