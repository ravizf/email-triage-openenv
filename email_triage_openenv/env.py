from .models import Observation, Action
from .tasks import TASKS
from .grader import grade

class EmailTriageEnv:
    def __init__(self):
        self.task = None
        self.step_count = 0
        self.max_steps = 2

    def reset(self, task_id=0):
        self.task = TASKS[task_id]
        self.step_count = 0
        return Observation(email=self.task["email"], step=0)

    def step(self, action: Action):
        self.step_count += 1

        reward = grade(self.task, action, self.step_count)

        done = self.step_count >= self.max_steps

        return (
            Observation(email=self.task["email"], step=self.step_count),
            reward,
            done,
            {}
        )

    def state(self):
        return self.task