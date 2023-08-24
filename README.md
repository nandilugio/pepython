# PePython

Need help organizing your project's tasks?

Don't want to learn a complex tool with an unnecessarily cumbersome syntax or API?

Want to specify your tasks __in plain Python__ still having easy and flexible __access to the shell__?

**Just call PePython!**

## Install

```bash
pip install pepython
```

## Quick start

Define your tasks in a `tasks.py` file your root directory. Tasks are just __plain Python__ functions. Note how dependencies are just calls in the body of the tasks themselves, alowing all kinds of dependencies and parameter forwarding (see the parameters in action further down!).

```python
from pepython.task_def import task, s

@task
def clean():
    s("rm -rf build dist *.egg-info")

@task
def build():
    clean()
    s("pipenv run python setup.py sdist bdist_wheel")

@task
def publish():
    s("pipenv run twine upload dist/*", interactive=True)

@task
def build_and_publish():
    build()     # These are
    publish()   #  dependencies!
```

Then just call PePython!

```
$ pepython --help
Usage:
        pepython [--defs-path path-to-your-tasks-definitions.py] task [task params ...]

$ pepython clean
Executed task 'clean' successfuly.

$ pepython build_and_publish
Enter your username: your-name-here
Enter your password: ************
Uploading distributions to https://test.pypi.org/legacy/
Uploading pepython-0.1.0-py2-none-any.whl
100%|█████████████████████████████████████████████████████| 7.77k/7.77k [00:00<00:00, 42.6kB/s]
Uploading pepython-0.1.0.tar.gz
100%|█████████████████████████████████████████████████████| 5.65k/5.65k [00:01<00:00, 4.74kB/s]

Executed task 'build_and_publish' successfuly.
```

Note how **dependencies** are __just method calls__ in the body of the tasks themselves. This allows easy forwarding of params and a more flexible schema than some configured pre/post dependencies, like it's done in other tools.

If you need task **arguments**, they are defined naturally, again in plain Pyhton:

```python
@task
def task_args(first_arg, second_arg, *rest_of_args):
    print(
        f"You've passed {first_arg} and {second_arg} as "
        f"the 2 first parms, then passed:\n{rest_of_args}."
    )
```

```
$ pepython task_args a b c d e
You've passed a and b as the 2 first parms, then passed:
('c', 'd', 'e').

Executed task 'task_args' successfuly.
```

The main idea is to use the Python language for your task automation, with all of it's flexibility but without loosing the shell. This is why there's `s()` (short for _shell_).

`s()` is meant to to be easy to use. Above we saw how using the `interactive` option, the password prompt was **handled interactively by the user**, while other **non interactive processes** can be left to be managed by the task. We'll demonstrate it here, along with the `fail_fast` option, that when set to false, allows the task to manage the errors:

```python
@task
def process_python_files():
    ls_result = s("ls *py", fail_fast=False)

    if not ls_result.ok:
        exit("No python files here")

    python_files_raw = ls_result.value['out'].split("\n")
    python_files = [f.strip() for f in python_files_raw if f.strip()]

    print(
        f"These are the python files in this directory:\n{python_files}"
    )
```

```
$ pepython process_python_files
These are the python files in this directory:
['setup.py', 'tasks.py']

Executed task 'shell_returned_values' successfuly.
```

`s()` can also receive the `verbose` option so you can see the exit code, stdout and stderr printed as follows:

```
Executed shell command 'ls *py'
exit code was: 0
stdout was:
setup.py
tasks.py

stderr was:

```

## Contributing

Make sure you have the lastest `pip` and `pipenv` versions:

```bash
pip install --upgrade pip pipenv
```

To start developing, start the environment by:

```bash
pipenv shell
pipenv install -d
```

The installed `pepython` within the pipenv environment is the editable (alla `pip install -e .`) version of the package, so you can manually test right away.

This tool uses both [`pipenv`](https://pipenv.readthedocs.io/) for development and [`setuptools`](https://setuptools.readthedocs.io/) for packaging and distribution. To this date there is not a 100% community-accepted best practice so I've taken [this approach](https://github.com/pypa/pipenv/issues/209#issuecomment-337409290). In summary:

To add an _application_ dependency, add it in `setup.py` and leave it with a loose version definition. Then, just do `pipenv install -e .` to install the dependency. Pipenv locking mecanism will work as expected, since pepython itself is in the `[packages]` section of `Pipfile` (check `Pipfile.lock` and you'll find the deps there).

To add a _development_ dependency, add it to `Pipfile` via `pipenv install -d <my-dependency>`.

This way there's a single source of truth for package definition. No need to repeat the deps in `setup.py` and `Pipfile*`.

### Tests

To test the project run [`pytest`](https://docs.pytest.org/) inside the `pipenv`. Once you have something running, run [`tox`](https://github.com/tox-dev/tox) to check it's compatible with all python versions supported.

IMPORTANT: in order to make `tox` test with different python versions, those have to be installed. [`pyenv`](https://github.com/pyenv/pyenv) is used for that purpose and should work out of the box. Check the required versions in [`tox.ini`](https://github.com/nandilugio/bumpytrack/blob/master/tox.ini) and related files.

### Dev tasks automation and publishing to PyPI

This project uses `pepython` itself for automation. There you'll find tasks to build and publish the package to PyPI.

## License

This project is licensed under the MIT License - see the [`LICENSE`](https://github.com/nandilugio/pepython/blob/master/LICENSE) file for details.

