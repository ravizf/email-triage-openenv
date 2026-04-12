from .models import Email
from .grader import grade, grade_task_0, grade_task_1, grade_task_2

TASKS = [
    {
        "id": "email_triage_task_0",
        "task_id": "spam_filter",
        "name": "spam-filter",
        "difficulty": "easy",
        "email": Email(
            subject="Win FREE iPhone!!!",
            body="Click this link to claim your prize now."
        ),
        "expected": "ignore",
        "ground_truth": "ignore",
        "expected_output": "ignore",
        "reward_range": [0.01, 0.99],
        "score_range": [0.01, 0.99],
        "reset_params": {"task_id": 0},
        "grader": grade_task_0,
        "grader_fn": grade_task_0,
        "grader_name": "grade_task_0",
    },
    {
        "id": "email_triage_task_1",
        "task_id": "meeting_reply",
        "name": "meeting-reply",
        "difficulty": "medium",
        "email": Email(
            subject="Meeting Request",
            body="Can we schedule a meeting tomorrow at 10 AM?"
        ),
        "expected": "reply",
        "ground_truth": "reply",
        "expected_output": "reply",
        "reward_range": [0.01, 0.99],
        "score_range": [0.01, 0.99],
        "reset_params": {"task_id": 1},
        "grader": grade_task_1,
        "grader_fn": grade_task_1,
        "grader_name": "grade_task_1",
    },
    {
        "id": "email_triage_task_2",
        "task_id": "urgent_incident",
        "name": "urgent-incident",
        "difficulty": "hard",
        "email": Email(
            subject="URGENT: Server Down",
            body="Production server is down. Immediate action needed!"
        ),
        "expected": "mark_urgent",
        "ground_truth": "mark_urgent",
        "expected_output": "mark_urgent",
        "reward_range": [0.01, 0.99],
        "score_range": [0.01, 0.99],
        "reset_params": {"task_id": 2},
        "grader": grade_task_2,
        "grader_fn": grade_task_2,
        "grader_name": "grade_task_2",
    }
]

TASK_ID_TO_INDEX = {
    "spam_filter": 0,
    "meeting_reply": 1,
    "urgent_incident": 2,
}

GRADERS = {
    "email_triage_task_0": grade_task_0,
    "email_triage_task_1": grade_task_1,
    "email_triage_task_2": grade_task_2,
}

TASK_GRADER_PAIRS = [
    ("email_triage_task_0", grade_task_0),
    ("email_triage_task_1", grade_task_1),
    ("email_triage_task_2", grade_task_2),
]

DEFAULT_GRADER = grade
