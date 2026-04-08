from .models import Email

TASKS = [
    {
        "id": 0,
        "difficulty": "easy",
        "email": Email(
            subject="Win FREE lottery now!!!",
            body="Click here to claim reward"
        ),
        "expected": "ignore",
        "keywords": ["free", "win", "lottery"]
    },
    {
        "id": 1,
        "difficulty": "medium",
        "email": Email(
            subject="Meeting Request",
            body="Can we meet tomorrow at 11 AM?"
        ),
        "expected": "reply",
        "keywords": ["meeting", "schedule"]
    },
    {
        "id": 2,
        "difficulty": "hard",
        "email": Email(
            subject="URGENT: Database Crash",
            body="Production database is down. Fix ASAP!"
        ),
        "expected": "mark_urgent",
        "keywords": ["urgent", "crash", "asap"]
    }
]