import os
from email_triage_openenv.env import EmailTriageEnv
from email_triage_openenv.models import Action
from llm_agent import llm_decide

API_BASE_URL = os.getenv("API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")


def grader(prediction, ground_truth):
    if prediction.lower() == ground_truth.lower():
        return 0.9
    return 0.3


def run():
    print("[START]")

    env = EmailTriageEnv()
    total_score = 0.0

    for task_id in [0, 1, 2]:
        obs = env.reset(task_id)
        result = llm_decide(obs.email)

        action = Action(
            action_type=result.get("action", "ignore"),
            response=result.get("response", ""),
            reason=result.get("reason", ""),
            confidence=result.get("confidence", 0.0),
        )

        _, _, _, _ = env.step(action)
        reward = grader(action.action_type, env.current_task["expected"])

        print(f"[STEP] task={task_id} score={reward}")
        total_score += reward

    avg_score = total_score / 3.0
    print(f"[END] avg_score={avg_score}")


if __name__ == "__main__":
    run()
