from task_scheduler.scheduler import task
import time

@task(name="A")
def taskA():
    time.sleep(2)
    print("Task A finished.")

@task(name="B")
def taskB():
    time.sleep(4)
    print("Task B finished.")

@task(name="C")
def taskC():
    time.sleep(1)
    print("Task C finished.")

@task(name="D")
def taskD():
    time.sleep(3)
    print("Task D finished.")

@task(name="E")
def taskE():
    time.sleep(1)
    print("Task E finished.")

@task(name="F")
def taskF():
    time.sleep(7)
    print("Task F finished.")

@task(name="G")
def taskG():
    time.sleep(1)
    print("Task G finished.")