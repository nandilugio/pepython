from pepython.task_def import task, s

@task
def sum_to_echoed_5(*args):
    echoed_5 = int(s("echo 5").value['out'].strip())
    total = sum([int(n) for n in args]) + echoed_5
    print(f"Total = {total}")

