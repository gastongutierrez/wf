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
    
    def __repr__(self):
        return (f"Task(name={self.name!r}, duration={self.duration}, "
                f"dependencies={self.dependencies}, "
                f"function={self.function.__name__ if self.function else None})")

    def __str__(self):
        return (f"{self.name}: (duration: {self.duration}, "
                f"dependencies: {self.dependencies})")

    def run(self):
        if self.function:
            return self.function()
        else:
            logging.warning(f"Task {self.name}: no function assigned.")

class Scheduler:
    def __init__(self, name: str, tasks_file: str):
        self.name = name
        self.tasks: dict[str, Task] = {}
        self._load_tasks(tasks_file)

    def _load_tasks(self, tasks_file: str):
        pass

    def validate_tasks(self):
        pass

    def run_tasks(self):
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    def example_task():
        print("Running Task...")

    task = Task(name="Task", duration=3, function=example_task)
    print(f"Name: {task.name}")
    print(f"Duration: {task.duration}")
    print(f"Dependencies: {task.dependencies}")
    task.run()

    print(str(task))

    print(repr(task))