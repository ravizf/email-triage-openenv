from email_triage_openenv.env import EmailTriageEnv
from email_triage_openenv.models import Action


def grader(pred, gt):
    if pred == gt:
        return 0.9
    return 0.4


def decide(email):
    text = (email.subject + " " + email.body).lower()

    if "free" in text or "win" in text:
        return {
            "action": "ignore",
            "response": "",
            "reason": "Spam detected",
            "confidence": 0.8,
        }

    elif "meeting" in text:
        return {
            "action": "reply",
            "response": "Yes, I am available.",
            "reason": "Meeting request detected",
            "confidence": 0.85,
        }

    elif "urgent" in text or "server" in text:
        return {
            "action": "mark_urgent",
            "response": "Escalating issue immediately.",
            "reason": "Urgent issue detected",
            "confidence": 0.9,
        }

    return {
        "action": "ignore",
        "response": "",
        "reason": "Default",
        "confidence": 0.5,
    }


def run():
    print("[START]")

    env = EmailTriageEnv()
    total = 0

    for task_id in [0, 1, 2]:
        obs = env.reset(task_id)
        result = decide(obs.email)

        action = Action(
            action_type=result["action"],
            response=result["response"],
            reason=result["reason"],
            confidence=result["confidence"],
        )

        expected = env.current_task["expected"]
        score = grader(action.action_type, expected)

        total += score

        print(f"[STEP] task={task_id} score={score}")

    avg = total / 3
    print(f"[END] avg_score={avg}")


if __name__ == "__main__":
    run()
