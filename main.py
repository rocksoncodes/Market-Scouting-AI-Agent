from services.scraper_service import scrape_reddit_data, store_reddit_data

def main():
    reddit_data = scrape_reddit_data()
    store_reddit_data(reddit_data)

if __name__ == "__main__":
    main()