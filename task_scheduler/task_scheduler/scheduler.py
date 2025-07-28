import logging
from typing import Optional, Callable

class Task:
    def __init__(self, name: str, duration: int, 
                 dependencies: Optional[list[str]] = None, 
                 function: Optional[Callable] = None):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies if dependencies is not None else []
        self.function = function

    def run(self):
        if self.function:
            return self.function()
        else:
            logging.warning(f"Task {self.name}: no function assigned.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    def example_task():
        print("Running Task...")

    task = Task(name="Task", duration=3, function=example_task)
    print(f"Name: {task.name}")
    print(f"Duration: {task.duration}")
    print(f"Dependencies: {task.dependencies}")
    task.run()
