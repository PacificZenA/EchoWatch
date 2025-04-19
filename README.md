# EchoWatch

🚨 EchoWatch is an open-source, multilingual OSINT-based threat detection tool that scans online forums for early-stage indicators of violent or extreme behavior.

## 🔍 Features (v0.1)
- ✅ Scan real-time Reddit subreddits (e.g., r/canada)
- ✅ Custom keyword matching (English & multi-language ready)
- ✅ Simple threat scoring system (based on keyword hits)
- ✅ Logs anonymized results with content hashing
- ✅ CSV output with timestamp, author, score, and matched keywords

## 💡 Use Case
Originally inspired by the concept of Minority Report and modern threat detection systems. EchoWatch focuses on **ethical monitoring of publicly available content** to surface early signs of dangerous intent or extreme sentiment.

## 🛠️ Tech Stack
- Python 3.10+
- `requests`, `beautifulsoup4`
- OpenAI API (optional, for semantic scoring)
- CSV-based logging

## 📁 Sample Output
```csv
timestamp,author,content_hash,matched_keywords,threat_score,url
2025-04-19T15:42:11,test_user,f5d8e5...,vote,liberal,conservative,100,https://reddit.com/xyz
