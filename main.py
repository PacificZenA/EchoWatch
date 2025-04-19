import requests
import time
import hashlib
import csv
from bs4 import BeautifulSoup
from datetime import datetime

# ======= 配置项 =======
SUBREDDIT = "worldnews"
POST_LIMIT = 10
KEYWORDS = ["bomb", "shoot", "kill", "attack", "revenge", "explosive"]
CSV_PATH = "output/threat_log.csv"

# ======= 工具函数 =======

def fetch_reddit_posts(subreddit, limit=10):
    headers = {'User-agent': 'EchoWatch Scanner 1.0'}
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Failed to fetch data: {res.status_code}")
        return []
    data = res.json()
    posts = data["data"]["children"]
    return [{
        "title": post["data"]["title"],
        "author": post["data"]["author"],
        "created_utc": post["data"]["created_utc"],
        "permalink": post["data"]["permalink"]
    } for post in posts]

def analyze_post(post, keywords):
    content = post["title"].lower()
    matched = [kw for kw in keywords if kw in content]
    score = len(matched) * 25  # 简单打分规则
    return matched, min(score, 100)

def hash_content(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def save_to_csv(entries, path):
    with open(path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for e in entries:
            writer.writerow([
                e["timestamp"],
                e["author"],
                e["content_hash"],
                ",".join(e["matched_keywords"]),
                e["threat_score"],
                f"https://reddit.com{e['permalink']}"
            ])

# ======= 主程序入口 =======

def main():
    print(f"[+] Starting EchoWatch v0.1 scanning r/{SUBREDDIT}...")
    posts = fetch_reddit_posts(SUBREDDIT, POST_LIMIT)
    log_entries = []

    for post in posts:
        matched, score = analyze_post(post, KEYWORDS)
        if matched:
            log_entries.append({
                "timestamp": datetime.utcfromtimestamp(post["created_utc"]).isoformat(),
                "author": post["author"],
                "content_hash": hash_content(post["title"]),
                "matched_keywords": matched,
                "threat_score": score,
                "permalink": post["permalink"]
            })
            print(f"[!] Threat detected: score={score}, keywords={matched}")

    if log_entries:
        save_to_csv(log_entries, CSV_PATH)
        print(f"[+] {len(log_entries)} threat logs saved to {CSV_PATH}")
    else:
        print("[-] No threats detected.")

if __name__ == "__main__":
    main()
