import os
import json
import hashlib
import csv
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv

# ===== Load API Key =====
load_dotenv(".env.local")
OPENROUTER_API_KEY = os.getenv("VITE_OPENROUTER_API_KEY")
OPENROUTER_MODEL = "openrouter/auto"

# ===== File Config =====
HTML_PATH = "dummy_forum.html"
CSV_PATH = "output/gpt_threat_log.csv"

def extract_posts_from_html(path):
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        divs = soup.select("div.message")
        messages = []
        for div in divs:
            author = div.get("data-author", "unknown")
            text = div.get_text(strip=True)
            messages.append({"author": author, "message": text})
        return messages

def analyze_with_gpt_batch(messages):
    if not OPENROUTER_API_KEY:
        print("❌ API key not found.")
        return []

    prompt = f"""
You are a threat detection assistant. Analyze the following forum messages for public safety risks (e.g. school shootings, terrorism, suicide).

Return a JSON list. For each message, respond with:
- author
- score (0–100)
- intent: "low", "moderate", "high"
- explanation
- message (original text)

Only respond with valid JSON list.

Messages:
{json.dumps(messages, indent=2)}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a public safety AI assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=20)
        if res.status_code != 200:
            print(f"❌ Request failed: {res.status_code}")
            print(res.text)
            return []

        raw = res.json()["choices"][0]["message"]["content"]
        return json.loads(raw)

    except Exception as e:
        print("❌ Error:", e)
        return []

def hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def save_to_csv(results, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for r in results:
            writer.writerow([
                datetime.now(timezone.utc).isoformat(),
                r.get("author", "unknown"),
                hash_text(r.get("message", "")),
                r.get("score", 0),
                r.get("intent", ""),
                r.get("explanation", ""),
                r.get("message", "")
            ])

# ===== MAIN =====
if __name__ == "__main__":
    print("[+] EchoWatch Batch Scanner (GPT) starting...")
    posts = extract_posts_from_html(HTML_PATH)
    print(f"[~] Loaded {len(posts)} messages.")

    results = analyze_with_gpt_batch(posts)
    if results:
        for r in results:
            print(f">> {r['author']}: score={r['score']} | intent={r['intent']} → {r['explanation']}")
        save_to_csv(results, CSV_PATH)
        print(f"\n✅ Saved {len(results)} entries to {CSV_PATH}")
    else:
        print("[-] No threats detected or analysis failed.")
