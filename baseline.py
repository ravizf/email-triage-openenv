from email_triage_openenv.env import EmailTriageEnv
from email_triage_openenv.models import Action

def smart_policy(email):
    text = (email.subject + " " + email.body).lower()

    if "urgent" in text or "crash" in text:
        return Action(action_type="mark_urgent")
    elif "meeting" in text:
        return Action(
            action_type="reply",
            response="Sure, I am available for the meeting."
        )
    else:
        return Action(action_type="ignore")


def run():
    env = EmailTriageEnv()
    total = 0

    for i in range(3):
        obs = env.reset(i)
        action = smart_policy(obs.email)

        _, reward, _, _ = env.step(action)

        print(f"Task {i}: {reward}")
        total += reward

    print("Final Score:", total / 3)


if __name__ == "__main__":
    run()