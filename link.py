import sqlite3
from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackContext, Updater
from telegram.ext import Dispatcher, Handler
from telegram.ext import WebhookHandler
import logging
import os

# 配置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化数据库
def init_db():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    points INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS invites (
                    user_id INTEGER,
                    invite_link TEXT)''')
    conn.commit()
    conn.close()

# 获取用户积分
def get_user_points(user_id):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return 0

# 更新用户积分
def update_user_points(user_id, points):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        new_points = result[0] + points
        c.execute('UPDATE users SET points = ? WHERE user_id = ?', (new_points, user_id))
    else:
        c.execute('INSERT INTO users (user_id, points) VALUES (?, ?)', (user_id, points))
    conn.commit()
    conn.close()

# 获取积分排名
def get_leaderboard():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT username, points FROM users ORDER BY points DESC LIMIT 10')
    leaderboard = c.fetchall()
    conn.close()
    return leaderboard

# 生成邀请链接
def generate_invite_link(user_id):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    invite_link = f"https://t.me/yourbot?start={user_id}"
    c.execute('INSERT INTO invites (user_id, invite_link) VALUES (?, ?)', (user_id, invite_link))
    conn.commit()
    conn.close()
    return invite_link

# 启动命令
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    update_user_points(user_id, 0)  # 确保用户有积分记录
    update.message.reply_text(f"Hello {username}! You can generate your personal invite link by typing /invite.")

# 邀请链接命令
def invite(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    invite_link = generate_invite_link(user_id)
    update.message.reply_text(f"Your invite link: {invite_link}")

# 排行榜命令
def leaderboard(update: Update, context: CallbackContext):
    leaderboard_data = get_leaderboard()
    leaderboard_text = "Top 10 Users:\n"
    for i, (username, points) in enumerate(leaderboard_data):
        leaderboard_text += f"{i+1}. {username}: {points} points\n"
    update.message.reply_text(leaderboard_text)

# 处理通过链接加入的用户
def handle_new_member(update: Update, context: CallbackContext):
    if update.message.new_chat_members:
        for new_user in update.message.new_chat_members:
            # 防止 bot 被加入
            if new_user.is_bot:
                return
            # 通过链接加入的用户增加积分
            user_id = new_user.id
            update_user_points(user_id, 1)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{new_user.username} has joined and earned 1 point!")

# Webhook 配置
def set_webhook():
    bot = Bot(token="YOUR_BOT_TOKEN")
    bot.setWebhook('https://yourserver.com/webhook')

# Webhook 处理
def webhook(request):
    if request.method == 'POST':
        updzate = Update.de_json(request.get_json(), bot)
        dispatcher.process_update(update)
    return 'OK'

# 主程序
def main():
    init_db()  # 初始化数据库

    # 设置 Webhook 服务器
    from flask import Flask, request
    app = Flask(__name__)

    # 设置 bot
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    # 添加命令处理器
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('invite', invite))
    dispatcher.add_handler(CommandHandler('leaderboard', leaderboard))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, handle_new_member))

    # 设置 Webhook
    @app.route('/webhook', methods=['POST'])
    def webhook_route():
        return webhook(request)

    # 启动 Webhook
    app.run(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    main()
