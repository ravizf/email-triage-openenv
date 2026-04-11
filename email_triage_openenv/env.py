from .models import Observation
from .tasks import TASKS
from .grader import grade


class EmailTriageEnv:
    def __init__(self):
        self.current_task = None
        self.step_count = 0

    def reset(self, task_id=0):
        self.current_task = TASKS[task_id]
        self.step_count = 0
        return Observation(email=self.current_task["email"], step=0)

    def step(self, action):
        self.step_count += 1
        reward = grade(self.current_task, action)
        done = True
        info = {"task_id": self.current_task["id"], "difficulty": self.current_task["difficulty"]}
        observation = Observation(email=self.current_task["email"], step=self.step_count)
        return observation, reward, done, info

    def state(self):
        return {
            "task": self.current_task,
            "step_count": self.step_count,
        }
