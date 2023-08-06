# Python utility functions

## install
[PyPI home](https://pypi.org/project/puf/).

`pip install puf`

Use `pip install -e .` to test locally.

## build, publish
See this [tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) for detailed instructions.
```shell
pip install -U pip build twine

python -m build
python -m twine upload dist/*
# enter __token__
# enter PyPI token
```

## test
See [python unittest](https://docs.python.org/3/library/unittest.html).
```shell
python -m unittest
```

- https://mysqlclient.readthedocs.io/user_guide.html
- https://pypi.org/project/mysqlclient/
