import logging
import feedparser
from datetime import datetime, timedelta
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, CHAT_ID, RSS_SOURCES, SENT_LINKS_FILE, KEYWORDS_FILE
from utils import config_utils, rss_utils

# 初始化 Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# 设置日志配置
logger = logging.getLogger(__name__)

# 获取 RSS 数据并根据配置进行解析
async def fetch_rss_and_filter(context):
    sent_links = config_utils.load_sent_links()  # 加载已发送的链接
    keywords = config_utils.load_keywords()  # 加载关键词
    
    for rss_source in RSS_SOURCES:
        logger.info(f"开始解析 RSS 源: {rss_source['name']} - {rss_source['url']}")
        feed = feedparser.parse(rss_source['url'])
        
        if feed.bozo:
            logger.error(f"解析 RSS 源失败: {rss_source['name']} - {rss_source['url']} - {feed.bozo_exception}")
            continue
        
        logger.info(f"成功解析到 {len(feed.entries)} 条 RSS 项")
        
        for entry in feed.entries:
            # 根据配置获取需要的字段
            fields = rss_source['fields']
            date_format = rss_source['date_format']
            unique_key_field = rss_source['unique_key']
            
            # 提取字段
            data = rss_utils.extract_fields(entry, fields, date_format)
            
            title = data.get("title", "没有标题")
            link = data.get("link", "没有链接")
            unique_key = data.get(unique_key_field, "没有唯一性标识")
            formatted_date = data.get(fields[-1], "没有日期")  # 获取日期字段
       
            # 检查标题是否包含关键词
            if any(keyword.lower() in title.lower() for keyword in keywords):
                logger.info(f"发现符合条件的条目: {title}")
                
                # 如果唯一性标识没有发送过，则发送消息
                if unique_key not in sent_links:
                    source_name = rss_source['name']  # 获取 RSS 源的名称作为来源标识
                    additional_info = {key: data.get(key, "无") for key in fields if key != fields[-1]}  # 提取非日期字段
                    await rss_utils.send_message_and_save(bot, CHAT_ID, link, unique_key, title, formatted_date, source_name, sent_links, additional_info)
                else:
                    logger.info(f"该条目已发送过: {title}")
            else:
                logger.debug(f"该条目标题不包含任何关键词: {title}")