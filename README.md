# Telegram Bot Project

[中文](#telegram-bot-项目)

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
# Telegram Bot 项目

[English](#telegram-bot-project)

这是一个 Telegram 机器人项目，能够监听群组消息并根据关键词执行操作，还可以获取 RSS 源并根据配置的关键词发送通知。

## 功能
- 添加、删除和列出关键词。
- 添加、删除和列出关键词对应的回复。
- 监听群组消息，根据配置的关键词自动回复。
- 获取 RSS 源，根据关键词发送通知。

## 安装步骤
1. 克隆仓库。
2. 安装依赖：`pip install -r requirements.txt`。
3. 在 `config.py` 中将 `TELEGRAM_BOT_TOKEN` 替换为您的 Telegram Bot Token。
4. 运行机器人：`python bot.py`。

## 使用方法
- `/add_keyword <keyword>`：添加一个关键词。
- `/remove_keyword <keyword>`：删除一个关键词。
- `/list_keywords`：列出所有关键词。
- `/add_reply <keyword> <reply>`：为某个关键词添加回复。
- `/remove_reply <keyword>`：删除某个关键词的回复。
- `/list_replies`：列出所有关键词对应的回复。

## 配置文件
- `keywords.json`：存储关键词列表。
- `replies.json`：存储关键词对应的回复。
- `sent_links.json`：存储已经发送过的链接。

