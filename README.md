# Market Scout: The AI Agent That Finds Market Problems for You

A lightweight AI agent that automates early-stage market research by scanning Reddit for real user pain points, validating them with a large language model, and preparing findings for downstream storage (Notion, database, etc.). Intended for entrepreneurs and developers who want to discover validated problems worth building solutions for.

---

## Key ideas

- Automatically collect posts and comments from configured subreddits.
- Use an LLM (Gemini) to validate whether a discovered issue represents a meaningful market problem.
- Produce structured outputs that can be saved to Notion or a database for later review.

---

## Current Features (implemented)

- OAuth-based Reddit integration for data ingestion
- Basic Gemini AI integration (validation prompts)
- Modular code structure with agents, services and pipelines
- Sentiment analysis and text processing helpers
- Structured logging

Planned features are tracked in the roadmap and will be added over time.

---

## Quick start

Prerequisites
- Python 3.11+ (tested with 3.13)
- A Reddit app (client ID & secret)
- Gemini API key (Google LLM)

1. Clone the repository

    git clone https://github.com/[your-username]/Market-Scouting-AI-Agent.git
    cd Market-Scouting-AI-Agent

2. Create a virtual environment and install dependencies

    python -m venv .venv
    .\.venv\Scripts\activate    # Windows
    pip install -r requirements.txt

3. Copy and edit environment variables

    cp .env.example .env

Open `.env` and set the required keys (see Configuration below).

4. Run the ingest agent (example)

    python engines\reddit_ingest.py

Depending on the agent/engine you want to run, use the corresponding script under `engines/`.

---

## Configuration (.env)

The following environment variables are used by the project (add any others required by your integrations):

- REDDIT_CLIENT_ID       # Reddit API client ID
- REDDIT_CLIENT_SECRET   # Reddit API secret
- REDDIT_USER_AGENT      # Reddit API user agent string
- GEMINI_API_KEY         # Gemini / Google LLM API key
- NOTION_API_KEY         # (optional) Notion integration key
- NOTION_DB_ID           # (optional) Notion database id

Notes:
- Keep secrets out of version control. Use a secrets manager for production.

---

## Project structure (overview)

- agents/         — orchestration logic for AI agents
- clients/        — thin API clients (Reddit, Gemini)
- engines/        — runnable scripts / entrypoints (reddit_ingest, curator)
- services/       — business logic and integrations (scrapers, storage)
- pipelines/      — data processing pipelines (sentiment, curator)
- database/       — SQLAlchemy models and DB initialization
- utils/          — shared helpers

---

## Development status

Branch: MSAA-05-Curator-Agent-Development

- ✅ Project skeleton and core modules
- ✅ Reddit ingestion and basic data collection
- ✅ Gemini integration for evaluation
- 🔄 Ongoing: Problem processing and storage
- 📝 Planned: Notion sync, richer problem-ranking, Email notifications

---

## Contributing

Contributions and PRs are welcome. Suggested ways to help:
- Implement planned features from the roadmap
- Improve data processing and validation prompts
- Add tests and CI
- Improve documentation and examples

When opening a PR, include tests or a short demo showing the change.

