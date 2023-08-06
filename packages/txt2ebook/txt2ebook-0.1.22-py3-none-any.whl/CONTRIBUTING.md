# Contributing

Setting up different Python environments, we need to install all supported
Python version using [pyenv](https://github.com/pyenv/pyenv):

```bash
pyenv install 3.7.16
pyenv install 3.8.16
pyenv install 3.9.16
pyenv install 3.10.9
pyenv install 3.11.1
```

Setting up development environment and install dependencies:

```bash
python -m pip install --upgrade pip poetry
poetry install
poetry check
```

Create a virtualenv for the current running Python version:

```bash
$ poetry env list
txt2ebook-HLRzIsQs-py3.7 (Activated)
```

Show all available tox tasks:

```bash
$ tox -av
...
default environments:
py37    -> testing against python3.7
py38    -> testing against python3.8
py39    -> testing against python3.9
py310   -> testing against python3.10
py311   -> testing against python3.11
cover   -> generate code coverage report in html
doc     -> generate sphinx documentation in html
gettext -> update pot/po/mo files
```

To run specific test:

```bash
tox -e py37,py38,py39,py310,py311 -- tests/test_tokenizer.py
```

For code lint, we're using `pre-commit`:

```bash
pre-commit install
pre-commit clean
pre-commit run --all-files
```

We're using zero-based versioning.

For patches or bug fixes:

```bash
poetry version patch
```

For feature release:

```bash
poetry version minor
```
