# PePython

Need help organizing your project's tasks? Just call PePython!

## Install

```bash
pip install pepython
```

## Quick start

Define your tasks in a `tasks.py` file your root directory. Note how dependencies are just method calls in the body of the tasks themselves. This allow params passing/forwarding and a more flexible schema than just pre/post dependencies.

```python
from pepython.task_def import task, s

@task
def clean(*args):
    s("rm -rf build dist *.egg-info")

@task
def build(*args):
    clean()
    s("pipenv run python setup.py sdist bdist_wheel")

@task
def publish(*args):
    s("pipenv run twine upload dist/*", interactive=True)

@task
def build_and_publish(*args):
    build()
    publish()
```

Then just call for PePython!

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

If you need task **arguments**, they are defined naturally:

```python
@task
def task_args(first_arg, second_arg, *rest_of_args):
    print(
        "You've passed {} and {} as the 2 first parms, then passed:\n{}."
        .format(first_arg, second_arg, rest_of_args)
    )
```

```
$ pepython task_args a b c d e
You've passed a and b as the 2 first parms, then passed:
('c', 'd', 'e').

Executed task 'task_args' successfuly.
```

The main idea is to use Python for your task automation, with all of it's flexibility but without loosing the shell. This is why there is `s()` (short for _shell_).

Apart from the `interactive` param shown above (see the password prompt in the output), it has some other possibilities:

**Interactive processes** are easily left piped to the user:

```python
@task
def change_pass():
    s("passwd", interactive=True)
```

```
$ pepython change_pass
Changing password for nando.
(current) UNIX password:
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully

Executed task 'change_pass' successfuly.
```

While other **non interactive processes** can be left to be managed by the task:

```python
@task
def process_python_files():
    ls_result = s("ls *py", fail_fast=False, verbose=True)

    if not ls_result.ok:
        exit("No python files here")

    python_files_raw = ls_result.value['out'].split("\n")
    python_files = [f.strip() for f in python_files_raw if f.strip()]

    print(
        "These are the python files in this directory:\n{}"
        .format(python_files)
    )
```

```
$ pepython process_python_files
Executed shell command 'ls *py'
exit code was: 0
stdout was:
setup.py
tasks.py

stderr was:

These are the python files in this directory:
[u'setup.py', u'tasks.py']

Executed task 'shell_returned_values' successfuly.
```

## Development

Make sure you have the lastest `pip` and `pipenv` versions:

```bash
pip install --upgrade pip pipenv
```

To start developing, start the environment by:

```bash
pipenv shell
pipenv install -d
```

This tool uses both [`pipenv`](https://pipenv.readthedocs.io/) for development and [`setuptools`](https://setuptools.readthedocs.io/) for packaging and distribution. To this date there is not a 100% community-accepted best practice so I've taken [this approach](https://github.com/pypa/pipenv/issues/209#issuecomment-337409290). In summary:

To add an _application_ dependency, add it in `setup.py` and leave it with a loose version definition. Then, just do `pipenv install -e .` to install the dependency. Pipenv locking mecanism will work as expected, since pepython itself in in the `[packages]` section of `Pipfile` (check `Pipfile.lock` and you'll find the deps there).

To add a _development_ dependency, add it to `Pipfile` via `pipenv install -d <my-dependency>`.

This way there's a single source of truth for package definition. No need to repeat the deps in `setup.py` and `Pipfile*`.

### Tests

To test the project run [`pytest`](https://docs.pytest.org/) inside the `pipenv`.

### Dev tasks automation and publishing to PyPI

This project uses `pepython` itself for automation. There you'll find tasks to build and publish the package to PyPI.

## License

This project is licensed under the MIT License - see the [`LICENSE`](https://github.com/nandilugio/pepython/blob/master/LICENSE) file for details.
