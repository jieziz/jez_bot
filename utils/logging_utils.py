import logging

def setup_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),  # 输出到控制台
            logging.FileHandler('rss_bot.log', encoding='utf-8')  # 保存到文件
        ]
    )
    logger = logging.getLogger(__name__)
    return logger