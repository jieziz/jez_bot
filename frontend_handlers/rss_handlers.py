import logging
import json
import os
from datetime import datetime, timedelta
import feedparser
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, CHAT_ID, RSS_SOURCES, SENT_LINKS_FILE, KEYWORDS_FILE
from utils import config_utils
import re


# 初始化 Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# 设置日志配置
logger = logging.getLogger(__name__)

def escape_markdown(text):
    # 转义 Markdown 特殊字符
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

# 提取所需字段的内容
def extract_fields(entry, fields, date_format):
    data = {}
    for field in fields:
        if field in entry:
            data[field] = entry[field]
        else:
            data[field] = "无"  # 如果字段不存在，返回默认值

    # 处理日期字段，假设所有日期字段都需要转换
    # 设定最后一个字段是日期字段
    date_field = fields[-1]
    if date_field in data:
        pub_date = data[date_field]
        try:
            parsed_date = datetime.strptime(pub_date, date_format)
            cst_date = parsed_date + timedelta(hours=8)
            formatted_date = cst_date.strftime('%Y-%m-%d %H:%M:%S')
            data[date_field] = formatted_date  # 更新日期字段
        except ValueError:
            logger.warning(f"日期格式解析错误: {pub_date}")
            data[date_field] = pub_date  # 如果解析失败，保留原始格式

    return data

# 发送消息并保存已发送链接
async def send_message_and_save(bot, chat_id, link, unique_key, title, formatted_date, source_name, sent_links, additional_info=None, context=None):
    title = escape_markdown(title)
    # 转换为 datetime 对象
    date_obj = datetime.strptime(formatted_date, "%Y-%m-%d %H:%M:%S")
    # 格式化为 mm-dd hh:mm
    formatted_date = date_obj.strftime("%m-%d %H:%M")

    # 判断标题是否包含 "引流"
    if "引流" in title:
        logger.info(f"标题包含 '引流'，跳过发送消息: {title}")
        return  # 不发送消息，直接返回

    # 判断标题是否包含 "出" 或 "收"
    if "出" in title or "收" in title:
        notification_title = "交易来啦"
        notification_emoji = "\U0001F4B0"  # 金钱图标 💰
    else:
        notification_title = "新帖子来啦"
        notification_emoji = "\U0001F514"  # 铃铛图标 🔔

    message = (
        f"{notification_emoji} *{notification_title}* {notification_emoji}\n"
        f"━━━━━━━━━━━\n"
        f"\U0001F4E2  [{title}]({link})\n"
        f"\U0001F3F7  {source_name}  `{formatted_date}`"
    )

    try:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown', disable_web_page_preview=True)
        logger.info(f"成功发送消息: {title}")
    except Exception as e:
        logger.error(f"发送消息失败: {e}")

    # 保存已发送链接
    sent_links.add(unique_key)
    config_utils.save_sent_links(sent_links)



# 获取 RSS 数据并根据配置进行解析
async def fetch_rss_and_filter(context):
    sent_links = config_utils.load_sent_links()  # 加载已发送的链接
    keywords = config_utils.load_keywords()  # 加载关键词
    logger.info(f"加载关键词: {keywords}")
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
            data = extract_fields(entry, fields, date_format)
            
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
                    await send_message_and_save(bot, CHAT_ID, link, unique_key, title, formatted_date, source_name, sent_links, additional_info)
                else:
                    logger.info(f"该条目已发送过: {title}")
            else:
                logger.debug(f"该条目标题不包含任何关键词: {title}")

