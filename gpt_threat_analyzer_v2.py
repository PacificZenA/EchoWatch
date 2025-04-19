import os
import requests
import json
from dotenv import load_dotenv

# Load API key from local env file
load_dotenv(".env.local")
OPENROUTER_API_KEY = os.getenv("VITE_OPENROUTER_API_KEY")
OPENROUTER_MODEL = "openrouter/auto"

def analyze_text_with_gpt(message):
    if not OPENROUTER_API_KEY:
        return {
            "score": 0,
            "intent": "error",
            "explanation": "API key not found. Check .env.local file."
        }

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-butler-site.vercel.app",
        "X-Title": "EchoWatch"
    }

    prompt = f"""
You are an AI threat assessment system. Your job is to analyze the following message and assess how dangerous it is.

Message: "{message}"

Respond ONLY in the following exact JSON format:

{{
  "score": <number from 0 to 100>,
  "intent": "<low/moderate/high>",
  "explanation": "<short reason>"
}}
Do not include any other text or formatting.
"""

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a threat detection assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 401:
            return {"score": 0, "intent": "unauthorized", "explanation": "401 Unauthorized – check API key or headers."}
        if response.status_code != 200:
            return {"score": 0, "intent": "error", "explanation": f"Request failed with code {response.status_code}"}

        raw = response.json()["choices"][0]["message"]["content"]

        # Try to parse as JSON
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"score": 0, "intent": "error", "explanation": "Invalid JSON returned from GPT"}

    except requests.Timeout:
        return {"score": 0, "intent": "timeout", "explanation": "GPT request timed out"}
    except Exception as e:
        return {"score": 0, "intent": "error", "explanation": f"Exception: {e}"}
