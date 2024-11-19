TELEGRAM_BOT_TOKEN = "7579255040:AAFYREPl_G0tAoFT3Jeq5ARbymBkxADGVxY"
CHAT_ID = "907118371"
KEYWORDS_FILE = "data/keywords.json"
REPLIES_FILE = "data/replies.json"
SENT_LINKS_FILE = "data/sent_links.json"

RSS_SOURCES = [                         
    {
        "url": "https://rss.nodeseek.com/",
        "name": "NodeSeek",
        "fields": ["title", "link", "published"], 
        "date_format": "%a, %d %b %Y %H:%M:%S %Z",
        "unique_key": "link" 
    },
    {
        "url": "https://www.v2ex.com/index.xml",
        "name": "v2ex",
        "fields": ["title", "link", "published", "id"],
        "date_format": "%Y-%m-%dT%H:%M:%S%z",
        "unique_key": "id"  
    },
    {
        "url": "https://hostloc.com/forum.php?mod=rss",
        "name": "hostloc",
        "fields": ["title", "link", "pubDate"],  
        "date_format": "%Y-%m-%dT%H:%M:%S%z",
        "unique_key": "link"  
    },
    {
        "url": "https://www.nodeloc.com/atom/discussions",
        "name": "NodeLoc",
        "fields": ["title", "link", "updated"], 
        "date_format": "%Y-%m-%dT%H:%M:%S%z",
        "unique_key": "link"  
    },
    {
        "url": "https://linux.do/latest.rss",
        "name": "linux.do",
        "fields": ["title", "link", "published"], 
        "date_format": "%a, %d %b %Y %H:%M:%S %z",
        "unique_key": "link"  
    },
    {
        "url": "https://lowendbox.com/feed/",
        "name": "lowendbox",
        "fields": ["title", "link", "published"], 
        "date_format": "%a, %d %b %Y %H:%M:%S %z",
        "unique_key": "link"  
    },
    {
        "url": "https://lowendtalk.com/discussions/feed.rss",
        "name": "lowendtalk",
        "fields": ["title", "link", "published"], 
        "date_format": "%a, %d %b %Y %H:%M:%S %z",
        "unique_key": "link"  
    }
    # 可添加更多源
]