import os
import subprocess

import pytest

# Helpers and definitions ######################################################

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "data")

def run(command, assert_success=True):
    completed_process = subprocess.run(
        command,
        shell=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if assert_success:
        if completed_process.returncode != 0:
            print("Non-zero exit running " + command)
            print("Stdout was:\n" + completed_process.stdout)
            print("Stderr was:\n" + completed_process.stderr)
            assert False

    return completed_process

# End-to-end tests #############################################################

def test_happy_path():
    defs_path = os.path.join(TEST_DATA_PATH, "tasks.py")
    assert "Total = 12" in run(f"pepython --defs-path {defs_path} sum_to_echoed_5 4 3").stdout

