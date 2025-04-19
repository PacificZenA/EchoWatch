# 🛰️ EchoWatch - Open Threat Signal Scanner

**EchoWatch** is an open-source intelligence (OSINT) tool for detecting early signs of online threats by scanning public platforms like Reddit, Pastebin, and 4plebs.org.

It matches messages against an evolving set of **intent-oriented phrases**, aiming to flag content related to:
- 🏫 school threats
- 🧨 terrorism
- 🧒 child exploitation
- 🧠 mental health breakdowns with risk signals

---

## 🚀 Features

- 🔍 Multi-platform scanning (Reddit, Pastebin, 4plebs)
- 🧠 Contextual keyword analysis (`threat_phrases.txt`)
- 🧾 CSV logs of all flagged content
- ⚙️ Headless browser support (Selenium for bypassing web protection)
- ☁️ No API keys required for Reddit or Pastebin

---

## 📁 Project Structure

```bash
ECHO_WATCH/
├── keywords/
│   ├── threat_phrases.txt        # Intent-oriented sentence fragments
│   ├── threat_school.txt
│   ├── threat_terror.txt
│   └── threat_csex.txt
├── output/
│   └── *.csv                     # Logs from all platforms
├── main.py                      # Central runner (Reddit-based)
├── external_pastebin_scanner.py
├── external_4plebs_selenium.py
├── gpt_threat_analyzer_v2.py    # Optional GPT-based scoring
├── keywords_loader.py
├── reddit_comments.py
└── README.md


⚙️ Setup
Clone this repo

Install dependencies:
pip install -r requirements.txt

For 4plebs scanner, also install:
pip install selenium webdriver-manager
Ensure keywords/ contains your threat phrase lists


🧪 Run Scanners
# Reddit
python main.py

# Pastebin
python external_pastebin_scanner.py

# 4plebs (headless Chrome)
python external_4plebs_selenium.py


📦 Outputs
All logs saved under /output/*.csv with fields:

🧠 Author
Created by Alex Tang for ethical AI research and digital public safety.
"I’d rather prevent one tragedy than debug a thousand after the fact."


📜 Changelog
[v0.6.2] - 2025-04-21
✅ Added Pastebin and 4plebs (Selenium-based) scanners
🧠 Upgraded threat_phrases.txt with 30+ intent phrases
🧹 Removed deprecated direct 4chan scanner due to ongoing breach
🛡️ Scanned live platforms, no threats detected (空军一日)
