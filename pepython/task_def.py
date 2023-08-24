import subprocess
import sys

from . import common as cmn


task_registry = {}


def task(task_func):
    """
    Decorate your tasks to register them. The name of the function is the
    public task name used to invoke it from the command line.
    """
    task_registry[task_func.__name__] = task_func
    return task_func


def s(command, verbose=False, fail_fast=True, interactive=False):
    """
    Run a shell command.
    """

    completed_process = None
    output = None
    if interactive:
        completed_process = subprocess.run(
            command,
            shell=True,
            encoding="utf-8",
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        output = {
            "exit_code": completed_process.returncode,
        }
    else:
        completed_process = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output = {
            "exit_code": completed_process.returncode,
            "out": completed_process.stdout,
            "err": completed_process.stderr,
        }

    result = None
    if completed_process.returncode == 0:
        result = cmn.OkResult(output)
    else:
        result = cmn.ErrorResult(output)

    fail = fail_fast and not result.ok

    if verbose or fail:
        cmn.logger.log(
            "Executed shell command '{command}'\n"
            "exit code was: {exit_code}\n".format(
                command=command,
                **result.value
            )
        )

    if (verbose or fail) and not interactive:
        cmn.logger.log(
            "stdout was:\n{out}\n"
            "stderr was:\n{err}".format(
                **result.value
            )
        )

    if fail:
        cmn.fail(f"Failed executing shell command '{command}'")

    return result
