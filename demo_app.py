import gradio as gr

from email_triage_openenv.env import EmailTriageEnv
from email_triage_openenv.models import Action
from analytics import generate_chart
from llm_agent import llm_decide
from logger import log_result
from report import generate_report


env = EmailTriageEnv()
SEPARATOR = "-" * 31


def run_agent(task_id):
    try:
        task_id = int(task_id)
    except (TypeError, ValueError):
        return "Please enter 0, 1, or 2."

    if task_id not in [0, 1, 2]:
        return "Please enter 0, 1, or 2."

    try:
        obs = env.reset(task_id)
        result = llm_decide(obs.email)

        action = Action(
            action_type=result.get("action"),
            response=result.get("response", ""),
            reason=result.get("reason", ""),
            confidence=result.get("confidence", 0.0),
        )

        _, reward, _, _ = env.step(action)

        log_result(task_id, obs.email, action, reward)
        generate_chart()
        generate_report()
    except Exception:
        return "Something went wrong while running the task. Please check the terminal and try again."

    return f"""
{SEPARATOR}
Email
{SEPARATOR}
Subject: {obs.email.subject}
Body: {obs.email.body}

{SEPARATOR}
Decision
{SEPARATOR}
Action: {action.action_type}
Response: {action.response or "No reply needed"}

{SEPARATOR}
Notes
{SEPARATOR}
Reason: {action.reason}
Confidence: {round(action.confidence, 2)}

{SEPARATOR}
Score
{SEPARATOR}
Reward: {round(reward, 2)}

Files saved: logs.json, performance.png, report.pdf
{SEPARATOR}
"""


gr.Interface(
    fn=run_agent,
    inputs=gr.Number(label="Task ID (0-2)"),
    outputs="text",
    title="Email Triage Demo",
    description="Run one of the sample tasks and review the result.",
    flagging_mode="never",
).launch(server_name="0.0.0.0")
