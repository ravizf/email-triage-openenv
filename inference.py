import os

from email_triage_openenv.env import EmailTriageEnv
from email_triage_openenv.models import Action


API_BASE_URL = os.getenv("API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "")
HF_TOKEN = os.getenv("HF_TOKEN")


def run():
    print("[START]")

    env = EmailTriageEnv()
    total_score = 0.0

    for task_id in [0, 1, 2]:
        obs = env.reset(task_id)

        # Simple rule-based agent for reproducible baseline scoring.
        text = (obs.email.subject + " " + obs.email.body).lower()

        if "urgent" in text or "server" in text:
            action_type = "mark_urgent"
        elif "meeting" in text:
            action_type = "reply"
        else:
            action_type = "ignore"

        action = Action(action_type=action_type)

        _, reward, done, _ = env.step(action)

        print(f"[STEP] task={task_id} action={action_type} reward={reward}")

        total_score += reward

        if not done:
            # The current environment supports multi-step episodes, but the
            # baseline evaluates one graded action per task.
            pass

    avg_score = total_score / 3

    print(f"[END] avg_score={avg_score}")


if __name__ == "__main__":
    run()
