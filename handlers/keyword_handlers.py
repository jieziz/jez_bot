from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils import config_utils

async def add_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        keyword = context.args[0]
        keywords = config_utils.load_keywords()
        keywords.add(keyword)
        config_utils.save_keywords(keywords)
        await update.message.reply_text(f"关键词 '{keyword}' 已添加。")
    else:
        await update.message.reply_text("请提供要添加的关键词。例如: /add_keyword 你的关键词")

async def remove_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        keyword = context.args[0]
        keywords = config_utils.load_keywords()
        if keyword in keywords:
            keywords.remove(keyword)
            config_utils.save_keywords(keywords)
            await update.message.reply_text(f"关键词 '{keyword}' 已删除。")
        else:
            await update.message.reply_text(f"关键词 '{keyword}' 不存在。")
    else:
        await update.message.reply_text("请提供要删除的关键词。例如: /remove_keyword 你的关键词")

async def list_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keywords = config_utils.load_keywords()
    if keywords:
        keyword_list = "\n".join(keywords)
        await update.message.reply_text(f"当前关键词列表:\n{keyword_list}")
    else:
        await update.message.reply_text("当前没有关键词。")

add_keyword_handler = CommandHandler("add_keyword", add_keyword)
remove_keyword_handler = CommandHandler("remove_keyword", remove_keyword)
list_keywords_handler = CommandHandler("list_keywords", list_keywords)