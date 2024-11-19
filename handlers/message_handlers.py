from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes
from utils import config_utils

async def monitor_group_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    message_text = update.message.text
    replies = config_utils.load_replies()
    for keyword, reply in replies.items():
        if keyword in message_text:
            await update.message.reply_text(reply)
            break

monitor_group_messages_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, monitor_group_messages)