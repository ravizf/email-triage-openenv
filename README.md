# Email Triage Demo

## Overview

This project is a small email triage environment with three sample tasks. It classifies each email, explains the decision, and saves simple evaluation artifacts.

## Features

- OpenEnv-style interface (`step`, `reset`, `state`)
- Three sample tasks with increasing difficulty
- Partial reward grading
- Offline rule-based agent
- Interactive Gradio UI
- Decision reason and confidence output
- Logging for every evaluation run
- Performance chart generation
- PDF report generation

## Project Structure

```text
email-triage-openenv/
├── email_triage_openenv/
│   ├── env.py
│   ├── models.py
│   ├── tasks.py
│   └── grader.py
├── app.py
├── analytics.py
├── llm_agent.py
├── logger.py
├── baseline.py
├── openenv.yaml
├── report.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Tasks

1. Spam filtering
2. Meeting response
3. Urgent system failure detection

## Observation Space

Each observation is a structured object with:

- `email.subject`: subject line of the current email
- `email.body`: body text of the current email
- `step`: current step number in the episode
- `history`: optional interaction history string

## Action Space

Each action is a structured object with:

- `action_type`: one of `reply`, `ignore`, or `mark_urgent`
- `response`: optional reply text
- `reason`: short explanation for the chosen action
- `confidence`: heuristic confidence score between `0.0` and `1.0`

## Agent

The current agent uses a small deterministic policy to:

- Detect urgent incidents, meetings, and spam
- Decide the correct action without external APIs
- Generate a short response when needed
- Explain its decision with a reason and confidence score

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:7860`.

## Deploy

You can run this locally or upload it to Hugging Face Spaces with the Docker SDK.

## Evaluation

Scores range from `0.0` to `1.0` based on:

- Action correctness
- Keyword understanding
- Response quality

The project also saves logs, a score chart, and a PDF summary so each run is easy to inspect.

## Generated Artifacts

Each app run can produce:

- `logs.json` for tracked task results
- `performance.png` for score visualization
- `report.pdf` for a lightweight evaluation report with summary stats

## Checklist

- App runs without errors
- Gradio UI opens correctly
- Scores are generated
- `performance.png` is created
- `report.pdf` is created
- Docker container runs correctly
- README is clean and current

## How To Deploy

1. Go to Hugging Face and create an account.
2. Create a new Space.
3. Choose `Docker` as the SDK.
4. Name it `email-triage-agent`.
5. Upload the project files.
