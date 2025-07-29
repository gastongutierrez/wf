from asciinet import graph_to_ascii
from ast import literal_eval
import logging
import networkx as nx
from typing import Optional, Callable

TASKS = {}

def task(func=None, *, name=None):
    def wrapper(f):
        task_name = name or f.__name__
        TASKS[task_name] = f
        return f

    if func is None:
        return wrapper
    else:
        return wrapper(func)

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
        self._validated = False
        self.expected_runtime: Optional[int] = None

    def _load_tasks(self, tasks_file: str):
        with open(tasks_file, 'r') as f:
            for line_number, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                try:
                    name, duration, dependencies = [part.strip() for part in line.split(',', 2)]
                    if name in self.tasks:
                        raise ValueError(f"Duplicate task '{name}': line {line_number}. "
                                         f"Duplicate task names are not allowed.")
                    duration = int(duration)
                    try:
                        dependencies = literal_eval(dependencies)
                        if not isinstance(dependencies, list):
                            raise ValueError("Dependencies must be a list.")
                    except (SyntaxError, ValueError) as e:
                        raise ValueError(f"Invalid dependency format: line {line_number}: {e}")
                    if name in TASKS:
                        function = TASKS[name]
                    else:
                        logging.warning(f"Task {name}: no function assigned. Using fallback.")
                        function = lambda n=name: logging.warning(f"Task {n}: no function assigned.")
                    self.tasks[name] = Task(name, duration, dependencies, function)
                except Exception as e:
                    raise ValueError(f"Failed to parse line {line_number}: {line} — {e}")
            if not self.tasks:
                raise ValueError("No tasks were loaded. Please review the tasks file.")

    def validate_tasks(self):
        logging.info("Validating task list...")

        G = nx.DiGraph()
        for name, task in self.tasks.items():
            G.add_node(name, duration=task.duration)
            for dependency in task.dependencies:
                if dependency not in self.tasks:
                    raise ValueError(f"Task '{name}' has a missing dependency '{dependency}'")
                G.add_edge(dependency, name)

        if not nx.is_directed_acyclic_graph(G):
            cycles = list(nx.simple_cycles(G))
            for i, cycle in enumerate(cycles, 1):
                logging.error(f"Cycle {i}: {' -> '.join(cycle + [cycle[0]])}")
            raise ValueError(f"Task graph contains {len(cycles)} cycle(s). Validation failed.")

        ascii_graph = graph_to_ascii(G)
        logging.info("\n" + ascii_graph)

        topological_sort_list = list(nx.topological_sort(G))
        tasks_finish_time = {}
        for task in topological_sort_list:
            predecessors_list = list(G.predecessors(task))
            task_earliest_start = max(
                (tasks_finish_time[predecessor] for predecessor in predecessors_list), 
                default=0
            )
            tasks_finish_time[task] = task_earliest_start + self.tasks[task].duration

        self.expected_runtime = max(tasks_finish_time.values(), default=0)
        logging.info(f"Expected total runtime: {self.expected_runtime} seconds")

        task_stages = {}
        for task, finish_time in tasks_finish_time.items():
            start = finish_time - self.tasks[task].duration
            task_stages.setdefault(start, []).append(task)

        self.execution_stages = [task_stages[start_time] for start_time in sorted(task_stages)]
        self._validated = True

    def run_tasks(self):
        pass
