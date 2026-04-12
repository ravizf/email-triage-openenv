def _clamp_score(score):
    return min(max(float(score), 0.01), 0.99)


def _extract_prediction_ground_truth(*args, **kwargs):
    if "prediction" in kwargs and "ground_truth" in kwargs:
        return kwargs["prediction"], kwargs["ground_truth"]

    if "task" in kwargs and "action" in kwargs:
        task = kwargs["task"]
        action = kwargs["action"]
        prediction = getattr(action, "action_type", action)
        ground_truth = task.get("expected") if isinstance(task, dict) else None
        return prediction, ground_truth

    if "state" in kwargs and "reward" in kwargs:
        return None, kwargs["reward"]

    if len(args) == 2:
        first, second = args

        if isinstance(first, dict):
            prediction = getattr(second, "action_type", second)
            return prediction, first.get("expected")

        return first, second

    return None, None


def grade(*args, **kwargs):
    prediction, ground_truth = _extract_prediction_ground_truth(*args, **kwargs)

    if prediction is None and ground_truth is not None:
        return _clamp_score(ground_truth)

    if prediction is None or ground_truth is None:
        return 0.01

    prediction = str(prediction).strip().lower()
    ground_truth = str(ground_truth).strip().lower()

    if prediction == ground_truth:
        return 0.90

    if ground_truth == "mark_urgent":
        if prediction == "reply":
            return 0.60
        if prediction == "ignore":
            return 0.20
        return 0.10

    if ground_truth == "reply":
        if prediction == "mark_urgent":
            return 0.50
        if prediction == "ignore":
            return 0.20
        return 0.10

    if ground_truth == "ignore":
        if prediction == "reply":
            return 0.40
        if prediction == "mark_urgent":
            return 0.30
        return 0.10

    return 0.10


def grade_task_0(*args, **kwargs):
    prediction, _ = _extract_prediction_ground_truth(*args, **kwargs)
    if prediction is None and "reward" in kwargs:
        return _clamp_score(kwargs["reward"])
    return grade(prediction, "ignore")


def grade_task_1(*args, **kwargs):
    prediction, _ = _extract_prediction_ground_truth(*args, **kwargs)
    if prediction is None and "reward" in kwargs:
        return _clamp_score(kwargs["reward"])
    return grade(prediction, "reply")


def grade_task_2(*args, **kwargs):
    prediction, _ = _extract_prediction_ground_truth(*args, **kwargs)
    if prediction is None and "reward" in kwargs:
        return _clamp_score(kwargs["reward"])
    return grade(prediction, "mark_urgent")


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

__all__ = [
    "grade",
    "grade_task_0",
    "grade_task_1",
    "grade_task_2",
    "GRADERS",
    "TASK_GRADER_PAIRS",
]
