from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils import config_utils

async def add_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) >= 2:
        keyword = context.args[0]
        reply = " ".join(context.args[1:])
        replies = config_utils.load_replies()
        replies[keyword] = reply
        config_utils.save_replies(replies)
        await update.message.reply_text(f"关键词 '{keyword}' 的回复已设置为 '{reply}'。")
    else:
        await update.message.reply_text("请提供关键词和回复。例如: /add_reply 退款 会退款的请耐心等待")

async def remove_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        keyword = context.args[0]
        replies = config_utils.load_replies()
        if keyword in replies:
            del replies[keyword]
            config_utils.save_replies(replies)
            await update.message.reply_text(f"关键词 '{keyword}' 的回复已删除。")
        else:
            await update.message.reply_text(f"关键词 '{keyword}' 的回复不存在。")
    else:
        await update.message.reply_text("请提供要删除回复的关键词。例如: /remove_reply 退款")

async def list_replies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    replies = config_utils.load_replies()
    if replies:
        reply_list = "\n".join([f"{keyword}: {reply}" for keyword, reply in replies.items()])
        await update.message.reply_text(f"当前回复配置:\n{reply_list}")
    else:
        await update.message.reply_text("当前没有回复配置。")

add_reply_handler = CommandHandler("add_reply", add_reply)
remove_reply_handler = CommandHandler("remove_reply", remove_reply)
list_replies_handler = CommandHandler("list_replies", list_replies)