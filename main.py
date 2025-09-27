from database.init_db import init_db
from handlers.reddit_handler import scrape_reddit_data, store_reddit_data

def run_program():
    init_db()
    reddit_data = scrape_reddit_data()
    store_reddit_data(reddit_data)

if __name__ == "__main__":
    run_program()