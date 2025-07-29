import logging
from argparse import ArgumentParser
from .scheduler import Scheduler
import importlib.util
import os
import sys

def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    parser = ArgumentParser()
    parser.add_argument("-t", "--tasks-file", default="tasks.txt")
    parser.add_argument("-m", "--tasks-module", default="tasks.py")
    parser.add_argument("-v", "--validate-tasks", action="store_true")
    parser.add_argument("-r", "--run-tasks", action="store_true")
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    try:
        if not os.path.exists(args.tasks_module):
            raise FileNotFoundError(f"Tasks module file '{args.tasks_module}' not found.")
        spec = importlib.util.spec_from_file_location("tasks", args.tasks_module)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules["tasks"] = module
            spec.loader.exec_module(module)
        else:
            raise ImportError(f"Could not load tasks module from {args.tasks_module}") 
        scheduler = Scheduler("MyScheduler", args.tasks_file)
        if args.validate_tasks:
            scheduler.validate_tasks()
        if args.run_tasks:
            scheduler.run_tasks()
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
