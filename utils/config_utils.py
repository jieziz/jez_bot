import os
import json
from config import KEYWORDS_FILE, REPLIES_FILE, SENT_LINKS_FILE


def load_keywords() -> set:
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as file:
            return set(json.load(file))
    return set()

def save_keywords(keywords: set) -> None:
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as file:
        json.dump(list(keywords), file, ensure_ascii=False, indent=4)

def load_sent_links() -> set:
    if os.path.exists(SENT_LINKS_FILE):
        try:
            with open(SENT_LINKS_FILE, "r", encoding="utf-8") as file:
                return set(json.load(file))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {SENT_LINKS_FILE}: {e}")
            return set()
    return set()

def save_sent_links(sent_links: set) -> None:
    with open(SENT_LINKS_FILE, "w", encoding="utf-8") as file:
        json.dump(list(sent_links), file, ensure_ascii=False, indent=4)

def load_replies() -> dict:
    if os.path.exists(REPLIES_FILE):
        try:
            with open(REPLIES_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    print(f"Warning: {REPLIES_FILE} contains a list, converting to an empty dictionary.")
                    return {}
                return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {REPLIES_FILE}: {e}")
            return {}
    return {}


def load_replies() -> dict:
    if os.path.exists(REPLIES_FILE):
        with open(REPLIES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_replies(replies: dict) -> None:
    with open(REPLIES_FILE, "w", encoding="utf-8") as file:
        json.dump(replies, file, ensure_ascii=False, indent=4)