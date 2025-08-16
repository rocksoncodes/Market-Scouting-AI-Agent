# Market Scout – Problem Finder for Entrepreneurs & Developers
Automatically discovers market problems so you can focus on building solutions instead of hunting for ideas

## 1. How Market Scout Works (Story)

Entrepreneurs and developers spend hours manually searching forums and communities, trying to find problems worth solving.
Because this process takes so much time, I'm building Market Scout to automatically discover, filter, and structure market problems into actionable project briefs.

This way, users can focus on building solutions instead of hunting for ideas, saving time and increasing productivity.
This repository contains the initial project setup; more updates and implementations will be added throughout development.

## 2. Features (Planned)

- Reddit Scraper: Saves time on research

- Problem Processor: Converts raw data into structured briefs

- Notion Reporter: Organizes results in Notion

- Feedback Loop: Allows future improvement based on input
```bash
Note: (Features will be implemented incrementally through sprints.)
```

## 3. Quick Start
1. Clone the repository
```bash
git clone https://github.com/[your-username]/market-scout.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set environment variables
```bash
cp .env.example .env
```

4. Run the application
```bash
python run_agent.py  # currently placeholder script
```

## 4. Configuration

Edit the .env file with your:
```bash
REDDIT_CLIENT_ID – Reddit API client ID
REDDIT_CLIENT_SECRET – Reddit API secret
NOTION_API_KEY – Notion integration key
NOTION_DB_ID – Notion database ID
GEMINI_API_KEY – Gemini LLM API key

(These will be used as features are implemented.)
```

## 5. Tech Stack

**Language/Framework:** Python

**Database:** SQLite

**Other Tools:** PRAW (Reddit API), Gemini SDK, Notion API, GitHub Actions

## 6. Example Usage
Run the agent
```bash
python run_agent.py  # currently placeholder
```



Future updates will fetch problems, process them, and report to Notion.

## 7. Contributing

Pull requests are welcome! You can help by:

- Implementing features from the planned roadmap

- Improving project structure and readability

- Adding documentation or examples

## 8. License

MIT License – free to use, adapt, and share.