import requests
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime, timezone
import os
import csv

def load_threat_phrases(filepath="keywords/threat_phrases.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def analyze_paste(text, threat_phrases):
    text = text.lower()
    matched = [phrase for phrase in threat_phrases if phrase in text]
    score = min(len(matched) * 35, 100)
    return matched, score

def save_to_csv(rows, path="output/pastebin_threat_log.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow([
                row["timestamp"],
                row["content_hash"],
                ",".join(row["matched_keywords"]),
                row["threat_score"],
                row["source"],
                row["url"]
            ])

def scan_pastebin(threat_phrases, limit=10):
    base_url = "https://pastebin.com"
    archive_url = f"{base_url}/archive"
    headers = {"User-Agent": "EchoWatch-Pastebin-Scanner"}
    res = requests.get(archive_url, headers=headers, timeout=10)

    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select("table.maintable a[href^='/']")

    threat_logs = []
    for link in links[:limit]:
        paste_url = base_url + link["href"]
        paste_id = link["href"].strip("/")
        raw_url = f"https://pastebin.com/raw/{paste_id}"

        try:
            raw_res = requests.get(raw_url, headers=headers, timeout=10)
            if raw_res.status_code != 200:
                continue
            content = raw_res.text
            matched, score = analyze_paste(content, threat_phrases)
            if matched:
                threat_logs.append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "content_hash": hash_text(content),
                    "matched_keywords": matched,
                    "threat_score": score,
                    "source": "Pastebin",
                    "url": paste_url
                })
        except Exception:
            continue

    if threat_logs:
        save_to_csv(threat_logs)
        print(f"[+] {len(threat_logs)} threats saved to CSV.")
    else:
        print("[-] No threats detected.")

if __name__ == "__main__":
    phrases = load_threat_phrases()
    scan_pastebin(phrases)
