import logging
import json
import os
from datetime import datetime, timedelta
from config import SENT_LINKS_FILE

logger = logging.getLogger(__name__)

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
async def send_message_and_save(bot, chat_id, link, unique_key, title, formatted_date, source_name, sent_links, additional_info=None):
    message = (
        f"\U0001F514 *新内容通知* \U0001F514\n"
        f"━━━━━━━━━━━\n"
        f"\U0001F4CC *标题*: [{title}]({link})\n"
        f"\U0001F552 *时间*: `{formatted_date}`\n"
        f"\U0001F4F1 *来源*: {source_name}\n"
    )

    try:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        logger.info(f"成功发送消息: {title}")
    except Exception as e:
        logger.error(f"发送消息失败: {e}")

    # 保存已发送链接
    sent_links.add(unique_key)
    save_sent_links(sent_links)

# 读取已发送链接的记录
def load_sent_links():
    if os.path.exists(SENT_LINKS_FILE):
        with open(SENT_LINKS_FILE, 'r', encoding='utf-8') as file:
            return set(json.load(file))
    return set()

# 保存已发送链接的记录
def save_sent_links(sent_links):
    with open(SENT_LINKS_FILE, 'w', encoding='utf-8') as file:
        json.dump(list(sent_links), file, ensure_ascii=False, indent=4)