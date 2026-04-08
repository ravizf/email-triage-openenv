import json
import os

from openai import OpenAI

from email_triage_openenv.env import EmailTriageEnv
from email_triage_openenv.models import Action


API_BASE_URL = os.getenv("API_BASE_URL", "<your-active-openai-compatible-base-url>")
MODEL_NAME = os.getenv("MODEL_NAME", "<your-active-model-name>")
HF_TOKEN = os.getenv("HF_TOKEN")

# Optional - if you use from_docker_image():
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

ALLOWED_ACTIONS = {"reply", "ignore", "mark_urgent"}
SYSTEM_PROMPT = """You are an email triage assistant.
Read the email and return exactly one JSON object.
The object must contain:
- action_type: one of reply, ignore, mark_urgent
- response: a short response string, or empty string when no reply is needed
- reason: a brief explanation
- confidence: a number from 0.0 to 1.0
Return JSON only with no markdown or extra text."""


def build_client():
    return OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN or "placeholder-token",
    )


def heuristic_fallback(email):
    text = (email.subject + " " + email.body).lower()

    if any(word in text for word in ["urgent", "server", "crash", "asap", "down", "database"]):
        return {
            "action_type": "mark_urgent",
            "response": "",
            "reason": "Urgent incident keywords detected.",
            "confidence": 0.93,
        }

    if any(word in text for word in ["meeting", "schedule", "tomorrow", "request"]):
        return {
            "action_type": "reply",
            "response": "Thanks for the note. I am available and can meet at the proposed time.",
            "reason": "Scheduling request detected.",
            "confidence": 0.88,
        }

    return {
        "action_type": "ignore",
        "response": "",
        "reason": "Promotional or low-priority content detected.",
        "confidence": 0.72,
    }


def extract_json_object(text):
    if not text:
        raise ValueError("Empty model response")

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(text[start : end + 1])


def normalize_action(payload):
    if not isinstance(payload, dict):
        payload = {}

    action_type = str(payload.get("action_type", "ignore")).strip().lower()
    if action_type not in ALLOWED_ACTIONS:
        action_type = "ignore"

    response = payload.get("response", "")
    if response is None:
        response = ""
    response = str(response).strip()
    if action_type != "reply":
        response = ""

    reason = payload.get("reason", "")
    if reason is None:
        reason = ""
    reason = str(reason).strip() or "No reason provided."

    confidence = payload.get("confidence", 0.0)
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0
    confidence = max(0.0, min(confidence, 1.0))

    return {
        "action_type": action_type,
        "response": response,
        "reason": reason,
        "confidence": confidence,
    }


def call_model(client, email):
    user_prompt = (
        "Classify this email and return JSON only.\n"
        f"Subject: {email.subject}\n"
        f"Body: {email.body}"
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    content = response.choices[0].message.content
    return extract_json_object(content)


def decide_action(client, email):
    try:
        payload = call_model(client, email)
    except Exception:
        payload = heuristic_fallback(email)
    return normalize_action(payload)


def run():
    print("[START]")

    env = EmailTriageEnv()
    client = build_client()
    total_score = 0.0

    for task_id in [0, 1, 2]:
        obs = env.reset(task_id)
        payload = decide_action(client, obs.email)
        action = Action(**payload)
        _, reward, _, _ = env.step(action)
        total_score += reward
        print(f"[STEP] task={task_id} action={action.action_type} reward={reward}")

    avg_score = total_score / 3
    print(f"[END] avg_score={avg_score}")


if __name__ == "__main__":
    run()
