# Market Scouting AI Agent
#### `For Entrepreneurs & Developers` </br>
Automatically discovers market problems so you can focus on building solutions instead of hunting for ideas.


## 1. How Market Scout Works (Overview)

Entrepreneurs and developers spend hours manually searching forums and communities, trying to find problems worth solving.
Because this process takes so much time, I'm building Market Scout to automatically discover, filter, and structure market problems into actionable project briefs.

This way, users can focus on building solutions instead of hunting for ideas, saving time and increasing productivity.
This repository contains the initial project setup; more updates and implementations will be added throughout development.

## 2. Planned Features

- Reddit Scraper: Collects relevant data efficiently

- Problem Processor: Converts raw posts into structured problem briefs

- Notion Reporter: Organizes findings in Notion databases

- Feedback Loop: Allows iterative improvements based on user input
```bash
Note: (Features will be implemented incrementally through development sprints.)
```

## 3. Quick Start
1. Clone the repository
```bash
git clone https://github.com/[your-username]/Market-Scouting-AI-Agent.git
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
REDDIT_CLIENT_ID       # Reddit API client ID
REDDIT_CLIENT_SECRET   # Reddit API secret
USER_AGENT             # Reddit API user agent
NOTION_API_KEY         # Notion integration key
NOTION_DB_ID           # Notion database ID
GEMINI_API_KEY         # Gemini LLM API key

(These will be used as features are implemented.)
```

## 5. Tech Stack

- Language/Framework: Python
- Database: SQLite
- APIs & Tools: PRAW (Reddit API), Gemini SDK, Notion API
- CI/CD: GitHub Actions

## 6. Example Usage
Run the agent
```bash
python run_agent.py  # currently placeholder
```



Future updates will fetch problems, process them, and report to Notion automatically.

## 7. Contributing

Pull requests are welcome! You can help by:

- Implementing features from the planned roadmap

- Improving project structure and readability

- Adding documentation or examples

## 8. License

MIT License – free to use, adapt, and share.
