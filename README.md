# Market Scouting AI Agent
#### For `Entrepreneurs & Developers` </br>
Automatically discovers market problems so you can focus on building solutions instead of hunting for ideas.


## 1. How Market Scout Works (Overview)

Entrepreneurs and developers spend hours manually searching forums and communities, trying to find problems worth solving.
Because this process takes so much time, I'm building Market Scout to automatically discover, filter and structure these market problems into actionable project briefs.

This way, users can focus on building solutions instead of hunting for ideas, saving time and increasing productivity.
This repository contains the initial project setup; more updates and implementations will be added throughout development.

## 2. Current Features

- Reddit Integration: OAuth-based Reddit API connection
- AI-Powered Analysis: Gemini API integration for problem validation
- Structured Logging: Comprehensive logging system
- Modular Architecture: 
  - agents/: AI agent logic and coordination
  - services/: Core business logic and API integrations
  - utils/: Shared utilities and helper functions

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

4. Configure your .env file with:
```bash
REDDIT_CLIENT_ID       # Your Reddit API client ID
REDDIT_CLIENT_SECRET   # Your Reddit API secret key
REDDIT_USER_AGENT     # Your Reddit API user agent
GEMINI_API_KEY        # Your Google Gemini API key
```

5. Run the scout agent
```bash
python main.py
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

## 5. Current Capabilities

- Reddit Data Collection: Fetches relevant posts from configured subreddits
- Problem Validation: Uses Gemini AI to evaluate problem validity

## 6. Development Status

Current branch: `MSAA-001-Reddit-Scrapper-Implementation`
- ✅ Basic project structure
- ✅ Reddit API integration
- ✅ Gemini AI integration
- ✅ Reddit data collection
- ✅ Problem validation system
- 🔄 Market sentiment analysis
- 📝 Reddit data storage 

## 7. Contributing

Pull requests are welcome! You can help by:

- Implementing features from the planned roadmap

- Improving project structure and readability

- Adding documentation or examples

## 8. License

MIT License – free to use, adapt and share.
