# Task Scheduler

## Description

**Task Scheduler** is a Python package that loads tasks definitions from a text file, obtains the critical path, calculates the expected runtime, runs the tasks in parallel threads and obtains the actual runtime.

## Installation

### 1. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

#### 2. Install the package (and its dependencies)
```bash
pip install ./task_scheduler
```

## Usage

You can run the CLI directly:

```bash
wf-scheduler --validate-tasks
wf-scheduler --run-tasks
```

Or, you can run the example provided:

```bash
python myapp.py
```

This example imports and runs the Scheduler instance:

```python
from task_scheduler.scheduler import Scheduler

scheduler = Scheduler("MyAppScheduler", args.tasks_file)
scheduler.validate_tasks()
scheduler.run_tasks()
```

Tasks should be defined in a text file with the following format:

```
# name, duration, [dependencies]
A, 2, []
B, 4, ['A']
C, 1, ['A']
D, 3, ['B', 'C']
E, 1, ['A']
F, 7, ['D', 'E']
G, 1, []
```

Task functions must be defined using the `@task` decorator. The name should match the task name in the file:

```python
@task(name="A")
def taskA():
    time.sleep(2)
    print("Task A finished.")
```

## Reference

```bash
usage: wf-scheduler [-h] [-t TASKS_FILE] [-m TASKS_MODULE] [-v] [-r]

options:
  -h, --help            show this help message and exit
  -t TASKS_FILE, --tasks-file TASKS_FILE
  -m TASKS_MODULE, --tasks-module TASKS_MODULE
  -v, --validate-tasks
  -r, --run-tasks
  ```