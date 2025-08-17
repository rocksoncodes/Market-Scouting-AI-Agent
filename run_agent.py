from scrapper.reddit_scrapper import fetch_reddit_posts

def main():
    """
    Main execution function for fetching Reddit posts.
    """
    subreddit_list = [
        "startups", 
        "Entrepreneur", 
        "smallbusiness",
        "freelance",
        "Productivity",
        "sidehustle"
    ]

    fetch_reddit_posts(subreddit_list)


if __name__ == "__main__":
    main()