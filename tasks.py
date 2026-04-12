from graders import grade, grade_task_0, grade_task_1, grade_task_2


TASKS = [
    {
        "id": "email_triage_task_0",
        "task_id": "spam_filter",
        "name": "spam-filter",
        "difficulty": "easy",
        "description": "Classify a promotional spam email and ignore it.",
        "input": "Subject: Win FREE iPhone!!! Body: Click this link to claim your prize now.",
        "expected": "ignore",
        "expected_output": "ignore",
        "ground_truth": "ignore",
        "max_steps": 1,
        "reset_params": {"task_id": 0},
        "reward_range": [0.01, 0.99],
        "score_range": [0.01, 0.99],
        "grader": "env.graders:grade_task_0",
        "grader_fn": "env.graders:grade_task_0",
        "grader_name": "env.graders:grade_task_0",
        "graders": ["env.graders:grade_task_0"],
    },
    {
        "id": "email_triage_task_1",
        "task_id": "meeting_reply",
        "name": "meeting-reply",
        "difficulty": "medium",
        "description": "Classify a meeting request and reply appropriately.",
        "input": "Subject: Meeting Request Body: Can we schedule a meeting tomorrow at 10 AM?",
        "expected": "reply",
        "expected_output": "reply",
        "ground_truth": "reply",
        "max_steps": 1,
        "reset_params": {"task_id": 1},
        "reward_range": [0.01, 0.99],
        "score_range": [0.01, 0.99],
        "grader": "env.graders:grade_task_1",
        "grader_fn": "env.graders:grade_task_1",
        "grader_name": "env.graders:grade_task_1",
        "graders": ["env.graders:grade_task_1"],
    },
    {
        "id": "email_triage_task_2",
        "task_id": "urgent_incident",
        "name": "urgent-incident",
        "difficulty": "hard",
        "description": "Classify an urgent production incident and mark it urgent.",
        "input": "Subject: URGENT: Server Down Body: Production server is down. Immediate action needed!",
        "expected": "mark_urgent",
        "expected_output": "mark_urgent",
        "ground_truth": "mark_urgent",
        "max_steps": 1,
        "reset_params": {"task_id": 2},
        "reward_range": [0.01, 0.99],
        "score_range": [0.01, 0.99],
        "grader": "env.graders:grade_task_2",
        "grader_fn": "env.graders:grade_task_2",
        "grader_name": "env.graders:grade_task_2",
        "graders": ["env.graders:grade_task_2"],
    },
]

TASK_ID_TO_INDEX = {
    "spam_filter": 0,
    "meeting_reply": 1,
    "urgent_incident": 2,
}

TASK_GRADER_PAIRS = [
    ("email_triage_task_0", grade_task_0),
    ("email_triage_task_1", grade_task_1),
    ("email_triage_task_2", grade_task_2),
]

GRADERS = {
    "email_triage_task_0": grade_task_0,
    "email_triage_task_1": grade_task_1,
    "email_triage_task_2": grade_task_2,
}

DEFAULT_GRADER = grade

__all__ = [
    "TASKS",
    "TASK_ID_TO_INDEX",
    "TASK_GRADER_PAIRS",
    "GRADERS",
    "DEFAULT_GRADER",
]
