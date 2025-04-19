import requests
import hashlib
import csv
from datetime import datetime, timezone
from reddit_comments import fetch_reddit_comments
from keywords_loader import load_all_keyword_categories
from gpt_threat_analyzer_v2 import analyze_text_with_gpt

# ======= Config =======
TARGET_SUBREDDITS = [
    "TrueOffMyChest", "confession", "conspiracy", "NoNewNormal",
    "AskTeenagers", "teenagers", "4chan", "MorbidReality",
    "TooAfraidToAsk", "DarkHumorAndMemes"
]

POST_LIMIT = 8
COMMENT_LIMIT = 5
CSV_PATH = "output/threat_log.csv"
GPT_TRIGGER_SCORE = 50  # Keyword score ≥ 50 → trigger GPT

# ======= Init =======
keywords_by_category = load_all_keyword_categories()

# ======= Core Functions =======
def fetch_reddit_posts(subreddit, limit=10):
    headers = {'User-agent': 'EchoWatch Scanner 1.0'}
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"[-] Failed to fetch posts from r/{subreddit}: {res.status_code}")
            return []
        data = res.json()
        return [{
            "title": post["data"]["title"],
            "author": post["data"]["author"],
            "created_utc": post["data"]["created_utc"],
            "permalink": post["data"]["permalink"]
        } for post in data["data"]["children"]]
    except Exception as e:
        print(f"[-] Exception while fetching r/{subreddit}: {e}")
        return []

def analyze_text(text, keyword_categories):
    text = text.lower()
    results = []
    for category, keyword_list in keyword_categories.items():
        matched = [kw for kw in keyword_list if kw in text]
        if "intent_phrases" in keyword_categories:
            matched = [kw for kw in keyword_categories["intent_phrases"] if kw in text]
            if matched:
                results.append({
                    "category": "intent_phrase",
                    "matched_keywords": matched,
                    "score": min(len(matched) * 35, 100)
                })
        if matched:
            score = len(matched) * 25
            results.append({
                "category": category,
                "matched_keywords": matched,
                "score": min(score, 100)
            })
    return results

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
                e["source"],
                e["threat_type"],
                f"https://reddit.com{e['permalink']}"
            ])

# ======= Main Scanner =======
def scan_subreddit(subreddit):
    print(f"\n🔍 Scanning r/{subreddit}...")
    posts = fetch_reddit_posts(subreddit, POST_LIMIT)
    log_entries = []

    for post in posts:
        post_results = analyze_text(post["title"], keywords_by_category)
        for r in post_results:
            gpt = {"score": 0, "intent": "skipped", "explanation": "Keyword score below threshold"}
            if r["score"] >= GPT_TRIGGER_SCORE:
                gpt = analyze_text_with_gpt(post["title"])

            log_entries.append({
                "timestamp": datetime.fromtimestamp(post["created_utc"], tz=timezone.utc).isoformat(),
                "author": post["author"],
                "content_hash": hash_content(post["title"]),
                "matched_keywords": r["matched_keywords"],
                "threat_score": max(r["score"], gpt["score"]),
                "source": "POST",
                "threat_type": r["category"],
                "permalink": post["permalink"]
            })
            print(f"[!] [POST] [{r['category'].upper()}] score={r['score']} | GPT: {gpt['score']} | {gpt['intent']} → {gpt['explanation']}")

        comments = fetch_reddit_comments(post["permalink"], COMMENT_LIMIT)
        for c in comments:
            comment_results = analyze_text(c["body"], keywords_by_category)
            for r in comment_results:
                gpt = {"score": 0, "intent": "skipped", "explanation": "Keyword score below threshold"}
                if r["score"] >= GPT_TRIGGER_SCORE:
                    gpt = analyze_text_with_gpt(c["body"])

                log_entries.append({
                    "timestamp": datetime.fromtimestamp(c["created_utc"], tz=timezone.utc).isoformat(),
                    "author": c["author"],
                    "content_hash": hash_content(c["body"]),
                    "matched_keywords": r["matched_keywords"],
                    "threat_score": max(r["score"], gpt["score"]),
                    "source": "COMMENT",
                    "threat_type": r["category"],
                    "permalink": post["permalink"]
                })
                print(f"[!] [COMMENT] [{r['category'].upper()}] score={r['score']} | GPT: {gpt['score']} | {gpt['intent']} → {gpt['explanation']}")

    return log_entries

# ======= Entry Point =======
if __name__ == "__main__":
    total_logs = []
    print("[+] EchoWatch v0.6 - Multi-subreddit scanner")

    for sub in TARGET_SUBREDDITS:
        logs = scan_subreddit(sub)
        total_logs.extend(logs)

    if total_logs:
        save_to_csv(total_logs, CSV_PATH)
        print(f"\n✅ Total {len(total_logs)} threat logs saved to {CSV_PATH}")
    else:
        print("\n[-] No threats detected in this session.")
