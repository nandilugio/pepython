import imp
import os
import sys

from . import task_def
from . import common as cmn


# Helpers ####################################################################

def _parse_args(args, user_defs):
    try:
        task_name = args[0]
    except IndexError:
        cmn.fail("Need to pass a task name as first argument.")

    if task_name not in user_defs.task_registry:
        cmn.fail(f"Task '{task_name}' not defined. Forgot to add '@task' above it?")

    task_args = args[1:]

    return task_name, task_args


def _load_task_defs(defs_path):
    try:
        imp.load_source("user_task_defs", defs_path)
    except IOError:
        cmn.fail(f"Cant access definitions file '{defs_path}'.")


def _run_task(task_name, task_args):
    task_def.task_registry[task_name](*task_args)
    cmn.logger.log(f"\nExecuted task '{task_name}' successfuly.")


##############################################################################

def main(defs_path, args):
    _load_task_defs(defs_path)
    task_name, task_args = _parse_args(args, task_def)
    _run_task(task_name, task_args)


def commandline_entrypoint():
    defs_path = None
    args = None

    first_arg = cmn.list_get(sys.argv, 1)
    if first_arg in ["--help", "-h"]:
        executable_name = os.path.basename(sys.argv[0])
        cmn.logger.log(f"Usage: \n\t{executable_name} "
        "[--defs-path path-to-your-tasks-definitions.py] task [task params ...]\n")
        exit(0)
    
    elif first_arg == "--defs-path":
        defs_path = sys.argv[2:3][0]
        args = sys.argv[3:]
    
    else:
        current_folder = os.getcwd()
        defs_path = os.path.join(current_folder, "tasks.py")
        args = sys.argv[1:]

    main(defs_path, args)


if __name__ == "__main__":
    commandline_entrypoint()
