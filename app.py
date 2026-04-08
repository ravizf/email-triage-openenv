from typing import Any, Dict, Optional

from fastapi import Body, FastAPI, HTTPException, Query
from pydantic import BaseModel

from email_triage_openenv.env import EmailTriageEnv
from email_triage_openenv.models import Action


app = FastAPI(title="Email Triage OpenEnv API")
env = EmailTriageEnv()
DIFFICULTY_TO_TASK_ID = {"easy": 0, "medium": 1, "hard": 2}


class ResetRequest(BaseModel):
    task_id: int = 0


class StepResponse(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool
    info: Dict[str, Any]


def model_to_dict(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return value


def normalize_task_selection(
    task_id: Optional[int],
    difficulty: Optional[str],
    body: Optional[ResetRequest],
) -> int:
    if task_id is not None:
        selected_task_id = task_id
    elif body is not None and body.task_id is not None:
        selected_task_id = body.task_id
    elif difficulty is not None:
        normalized_difficulty = difficulty.strip().lower()
        if normalized_difficulty not in DIFFICULTY_TO_TASK_ID:
            raise HTTPException(status_code=400, detail="Invalid difficulty")
        selected_task_id = DIFFICULTY_TO_TASK_ID[normalized_difficulty]
    else:
        selected_task_id = 0

    if selected_task_id not in DIFFICULTY_TO_TASK_ID.values():
        raise HTTPException(status_code=400, detail="Invalid task_id")

    return selected_task_id


def task_metadata(task_id: int) -> Dict[str, Any]:
    difficulty = next(
        name for name, mapped_task_id in DIFFICULTY_TO_TASK_ID.items() if mapped_task_id == task_id
    )
    return {"task_id": task_id, "difficulty": difficulty}


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "status": "ok",
        "message": "Email Triage OpenEnv API",
        "endpoints": ["/reset", "/step", "/state", "/health"],
        "supported_difficulties": list(DIFFICULTY_TO_TASK_ID.keys()),
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "initialized": env.task is not None}


@app.post("/reset")
def reset(
    payload: Optional[ResetRequest] = Body(default=None),
    task_id: Optional[int] = Query(default=None),
    difficulty: Optional[str] = Query(default=None),
) -> Dict[str, Any]:
    selected_task_id = normalize_task_selection(task_id, difficulty, payload)

    try:
        observation = env.reset(selected_task_id)
    except (IndexError, TypeError, KeyError):
        raise HTTPException(status_code=400, detail="Invalid task selection")

    return {
        "observation": model_to_dict(observation),
        "task": task_metadata(selected_task_id),
    }


@app.post("/step", response_model=StepResponse)
def step(action: Action) -> StepResponse:
    if env.task is None:
        raise HTTPException(status_code=400, detail="Call /reset before /step")

    observation, reward, done, info = env.step(action)
    return StepResponse(
        observation=model_to_dict(observation),
        reward=reward,
        done=done,
        info=model_to_dict(info),
    )


@app.get("/state")
def state() -> Dict[str, Any]:
    if env.task is None:
        return {"initialized": False, "state": None, "task": None}

    current_state = model_to_dict(env.state())
    current_task_id = current_state.get("id") if isinstance(current_state, dict) else None
    metadata = task_metadata(current_task_id) if current_task_id in DIFFICULTY_TO_TASK_ID.values() else None
    return {"initialized": True, "state": current_state, "task": metadata}
