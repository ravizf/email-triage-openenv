import json
import os

from openai import OpenAI


def _fallback_decide(email):
    text = (email.subject + " " + email.body).lower()

    if any(word in text for word in ["urgent", "server", "crash", "asap", "down", "immediate", "production"]):
        return {
            "action": "mark_urgent",
            "response": "",
            "reason": "Urgent issue detected",
            "confidence": 0.9,
        }

    if any(word in text for word in ["meeting", "schedule", "tomorrow", "request", "available"]):
        return {
            "action": "reply",
            "response": "Yes, I am available.",
            "reason": "Meeting request detected",
            "confidence": 0.85,
        }

    return {
        "action": "ignore",
        "response": "",
        "reason": "Spam or low-priority email detected",
        "confidence": 0.8,
    }


def llm_decide(email):
    api_base_url = os.getenv("API_BASE_URL")
    api_key = os.getenv("API_KEY")
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")

    if not api_base_url or not api_key:
        return _fallback_decide(email)

    client = OpenAI(base_url=api_base_url, api_key=api_key)

    prompt = f"""You are an email triage assistant.
Return valid JSON with keys action, response, reason, confidence.
Allowed actions: ignore, reply, mark_urgent.

Email subject: {email.subject}
Email body: {email.body}
"""

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        content = response.choices[0].message.content or "{}"
        parsed = json.loads(content)
        return {
            "action": parsed.get("action", "ignore"),
            "response": parsed.get("response", ""),
            "reason": parsed.get("reason", ""),
            "confidence": parsed.get("confidence", 0.0),
        }
    except Exception:
        return _fallback_decide(email)
