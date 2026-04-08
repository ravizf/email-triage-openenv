# Email Triage Demo

## Overview

This project is a small email triage environment with three sample tasks. It includes:

- `inference.py` for evaluator-facing submission runs
- `app.py` for the OpenEnv-compatible API server used in deployment
- `demo_app.py` for a local Gradio demo
- simple reporting artifacts for local inspection

## Features

- OpenEnv-style interface (`step`, `reset`, `state`)
- Three sample tasks with increasing difficulty
- Partial reward grading
- OpenAI-compatible submission path in `inference.py`
- OpenEnv-compatible API server for validator checks
- Interactive Gradio UI for local demo use
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

## Submission Inference

`inference.py` is the source of truth for submission. It uses the OpenAI Python client and reads these variables:

- `API_BASE_URL`
- `MODEL_NAME`
- `HF_TOKEN` as an optional token
- `LOCAL_IMAGE_NAME` only if you use `from_docker_image()`

The script prints only the required structured logs:

- `[START]`
- `[STEP]`
- `[END]`

## Run Locally

```bash
pip install -r requirements.txt
```

Run the API server used for deployment and automated checks:

```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

The OpenEnv API supports:

- `POST /reset?difficulty=easy|medium|hard`
- `POST /reset` with a JSON body like `{"task_id": 1}`
- `POST /step` with the `Action` payload
- `GET /state`
- `GET /health`

Set environment variables for the evaluator path:

```bash
export API_BASE_URL="https://your-openai-compatible-endpoint/v1"
export MODEL_NAME="your-model-name"
export HF_TOKEN="your-token-if-needed"
python inference.py
```

For the Gradio demo, run:

```bash
python demo_app.py
```

Then open `http://127.0.0.1:7860`.

## Deploy

You can run this locally or upload it to Hugging Face Spaces with the Docker SDK. The container now starts the OpenEnv API server by default so automated reset/step checks receive JSON responses instead of the Gradio HTML shell.

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

- `inference.py` uses the OpenAI client configured through env vars
- Only `API_BASE_URL` and `MODEL_NAME` have defaults
- `HF_TOKEN` is optional
- Structured stdout follows `[START]`, `[STEP]`, `[END]`
- deployed `app.py` serves JSON OpenEnv endpoints
- `demo_app.py` remains available for local Gradio testing

## How To Deploy

1. Go to Hugging Face and create an account.
2. Create a new Space.
3. Choose `Docker` as the SDK.
4. Name it `email-triage-agent`.
5. Upload the project files.
