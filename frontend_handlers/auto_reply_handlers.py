from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes, ApplicationBuilder
from utils import config_utils
from config import AUTO_DELETE_TIME
import re

# 自动删除消息的函数
async def auto_delete_message(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.delete_message(chat_id=context.job.data['chat_id'], message_id=context.job.data['message_id'])
    except Exception as e:
        print(f"删除消息失败: {e}")

# 监听群组消息的函数
async def monitor_group_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    message_text = update.message.text
    replies = config_utils.load_replies()

    for keywords, reply in replies.items():
        # 使用正则表达式匹配多个关键词
        if re.search(keywords, message_text, re.IGNORECASE):
            # 发送回复消息
            reply_message = await update.message.reply_text(reply)

            # 设置自动删除任务
            context.job_queue.run_once(
                auto_delete_message,
                AUTO_DELETE_TIME,
                data={
                    'chat_id': update.message.chat_id,
                    'message_id': reply_message.message_id
                }
            )
            break

# 创建消息处理器
monitor_group_messages_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, monitor_group_messages)