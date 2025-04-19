from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import hashlib
from datetime import datetime, timezone
import os
import csv

# === CONFIG ===
KEYWORD_FILE = "keywords/threat_phrases.txt"
OUTPUT_PATH = "output/4plebs_threat_log_selenium.csv"
TARGET_URL = "https://archive.4plebs.org/pol/"

# === HELPERS ===
def load_threat_phrases(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def analyze_text(text, threat_phrases):
    text = text.lower()
    matched = [phrase for phrase in threat_phrases if phrase in text]
    score = min(len(matched) * 35, 100)
    return matched, score

def save_to_csv(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow([
                row["timestamp"],
                row["content_hash"],
                ",".join(row["matched_keywords"]),
                row["threat_score"],
                row["preview"],
                row["url"]
            ])

# === MAIN ===
def scan_4plebs_selenium(threat_phrases):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    logs = []
    try:
        driver.get(TARGET_URL)
        posts = driver.find_elements(By.CSS_SELECTOR, "div.post_container")[:20]

        for post in posts:
            try:
                content = post.find_element(By.CSS_SELECTOR, "div.post_body").text
                link = post.find_element(By.CSS_SELECTOR, "a.post_number").get_attribute("href")
                matched, score = analyze_text(content, threat_phrases)
                if matched:
                    logs.append({
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "content_hash": hash_text(content),
                        "matched_keywords": matched,
                        "threat_score": score,
                        "preview": content[:100],
                        "url": link
                    })
            except Exception:
                continue

    finally:
        driver.quit()

    if logs:
        save_to_csv(logs, OUTPUT_PATH)
        print(f"[+] {len(logs)} threats saved to {OUTPUT_PATH}")
    else:
        print("[-] No threats detected.")

if __name__ == "__main__":
    phrases = load_threat_phrases(KEYWORD_FILE)
    scan_4plebs_selenium(phrases)
