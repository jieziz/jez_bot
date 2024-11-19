# Telegram Bot Project

This is a Telegram bot project that listens to group messages and performs actions based on keywords. It also fetches RSS feeds and sends notifications based on configured keywords.

## Features
- Add, remove, and list keywords.
- Add, remove, and list keyword-based replies.
- Monitor group messages and automatically reply based on configured keywords.
- Fetch RSS feeds and send notifications based on keywords.

## Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Replace `TELEGRAM_BOT_TOKEN` in `config.py` with your Telegram Bot Token.
4. Run the bot: `python bot.py`.

## Usage
- `/add_keyword <keyword>`: Add a keyword.
- `/remove_keyword <keyword>`: Remove a keyword.
- `/list_keywords`: List all keywords.
- `/add_reply <keyword> <reply>`: Add a reply for a keyword.
- `/remove_reply <keyword>`: Remove a reply for a keyword.
- `/list_replies`: List all keyword-based replies.

## Configuration
- `keywords.json`: Stores the list of keywords.
- `replies.json`: Stores the keyword-based replies.
- `sent_links.json`: Stores the links that have already been sent.