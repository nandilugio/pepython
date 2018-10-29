from pepython.task_def import task, s


@task
def clean(*args):
    s("rm -rf build dist *.egg-info")


@task
def build(*args):
    s("pipenv run pip install --upgrade setuptools wheel")
    s("pipenv run python setup.py sdist bdist_wheel")


@task
def publish(*args):
    s("pipenv run pip install --upgrade twine")
    #s("pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
    s("pipenv run twine upload dist/*")


@task
def build_and_publish(*args):
    clean()
    build()
    publish()

# TODO: delete!!
@task
def test(*args):
    res = s("ls " + args[0])
    print("res was:\n" + res.value['out'])