from telegram.ext import Application
from frontend_handlers import auto_reply_handlers, rss_handlers,chat_member_handlers
from management_handlers import reply_handlers, rss_keyword_handlers
from config import TELEGRAM_BOT_TOKEN
from utils import logging_utils

def main() -> None:
    # 创建应用
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 添加命令处理器
    application.add_handler(rss_keyword_handlers.add_keyword_handler)
    application.add_handler(rss_keyword_handlers.remove_keyword_handler)
    application.add_handler(rss_keyword_handlers.list_keywords_handler)

    application.add_handler(reply_handlers.add_reply_handler)
    application.add_handler(reply_handlers.remove_reply_handler)
    application.add_handler(reply_handlers.list_replies_handler)

    # 添加监听群组消息的处理器
    application.add_handler(auto_reply_handlers.monitor_group_messages_handler)

    # 添加监听新人入群的处理器
    # application.add_handler(chat_member_handlers.handle_new_member_handler)

    # 启动 RSS 抓取任务
    application.job_queue.run_repeating(rss_handlers.fetch_rss_and_filter, interval=60, first=0)

    # 启动轮询
    application.run_polling()

if __name__ == "__main__":
    logging_utils.setup_logging()
    main()