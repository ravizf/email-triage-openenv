import os

from email_triage_openenv.env import EmailTriageEnv
from email_triage_openenv.models import Action
from llm_agent import llm_decide


API_BASE_URL = os.getenv("API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
API_KEY = os.getenv("API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME", "")


def run():
    print("[START]")

    env = EmailTriageEnv()
    total = 0.0

    for task_id in [0, 1, 2]:
        obs = env.reset(task_id)
        result = llm_decide(obs.email)

        action = Action(
            action_type=result.get("action", "ignore"),
            response=result.get("response", ""),
            reason=result.get("reason", ""),
            confidence=result.get("confidence", 0.0),
        )

        _, score, _, _ = env.step(action)
        total += score

        print(f"[STEP] task={task_id} score={score}")

    avg = total / 3.0
    print(f"[END] avg_score={avg}")


if __name__ == "__main__":
    run()
