import logging
from argparse import ArgumentParser
from task_scheduler.scheduler import Scheduler
import sys
import tasks

def main():
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
        scheduler = Scheduler("MyAppScheduler", args.tasks_file)
        if args.validate_tasks:
            scheduler.validate_tasks()
        if args.run_tasks:
            scheduler.run_tasks()
    except ValueError as e:
        logging.error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    main()
