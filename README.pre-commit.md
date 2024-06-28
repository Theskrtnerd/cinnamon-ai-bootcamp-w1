# Pre-commit

## About Pre-commit

Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks.

To have a deep understanding and know advanced usages please read [official docs](https://pre-commit.com/).

## How to use

Make sure the pre-commit package is installed by poetry:

```bash
$ poetry install
```

Run `pre-commit install` to set up the git hook scripts

```bash
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

now pre-commit will run automatically on git commit!

In default, pre-commit will only run on changed files during git hooks. We should run `pre-commit run --all-files` when after installing pre-commit or adding new hooks.

```bash
$ pre-commit run --all-files
Check Yaml...........................................(no files to check)Skipped
Check Toml...........................................(no files to check)Skipped
Fix End of Files.........................................................Passed
Trim Trailing Whitespace.................................................Passed
Detect AWS Credentials...................................................Passed
Detect Private Key.......................................................Passed
Check for added large files..............................................Passed
black....................................................................Passed
isort....................................................................Passed
flake8...................................................................Passed
autoflake................................................................Passed
prettier.................................................................Passed
```

## Installed pre-commit hooks

The pre-commit configs are in the ".pre-commit-config.yaml" file which was based on Ms. Lita's configurations.

Pre-commit hooks:

- A set of hooks in [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)(_Some out-of-the-box hooks for pre-commit._):
  - check-yaml
  - check-toml
  - end-of-file-fixer
  - trailing-whitespace
  - detect-aws-credentials
  - detect-private-key
  - check-added-large-files
- [black](https://github.com/psf/black): _The Uncompromising Code Formatter._
- [isort](https://github.com/PyCQA/isort): _i**sort** your imports, so you don't have to._
- [flake8](https://github.com/PyCQA/flake8): _flake8 is a python tool that glues together pycodestyle, pyflakes, mccabe, and third-party plugins to check the style and quality of some python code._
- [autoflake](https://github.com/PyCQA/autoflake): _removes unused imports and unused variables from Python code_
- [mirrors-prettier](https://github.com/pre-commit/mirrors-prettier) _Prettier is an opinionated code formatter._

## Hook configuration details

There are some pre-commit hooks need further configurations.

### isort

Because we use isort alongside black, thus we need to add `--profile black` argument for black compatibility. [Learn more](https://pycqa.github.io/isort/docs/configuration/black_compatibility.html)

```yaml
- repo: https://github.com/PyCQA/isort
  rev: 5.13.2
  hooks:
    - id: isort
      args: ["--profile", "black"]
```

### flake8

flake8 need to have a separate configuration file name ".flake8":

```
[flake8]
ignore = E203, E266, E501, W503, F403, F401
max-line-length = 100
max-complexity = 18
select = B,C,E,F,M,T4,B9
```

Above is a sample flake8 configuration of Ms. Lita. Explanation:

- Ignored errors:
  - E203: whitespace before ‘:’
  - E266: too many leading ‘#’ for block comment
  - E501: line too long (82 > 79 characters)
  - W503: line break occurred before a binary operator
  - F403: ‘from module import \*’ used; unable to detect undefined names
  - F401: module imported but unused
- Max line length is 100 characters
- Max complexity is 18 which is [Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
- Selected checkers:
  - B: [Bugbear](https://github.com/PyCQA/flake8-bugbear) (A plugin for Flake8 finding likely bugs and design problems in your program)
  - C: [McCabe](https://github.com/PyCQA/mccabe) (McCabe complexity checker for Python)
  - E: [pycodestyle](https://github.com/PyCQA/pycodestyle) (pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.)
  - F: [Pyflakes](https://github.com/PyCQA/pyflakes) (A simple program which checks Python source files for errors.)
  - M: ?
  - T4: ?
  - B9: ?

### Prettier

Prettier is also a code formatter similar to black but for markdown and yaml files.

```yaml
  - repo: https://github.com/pre-commit/mirrors-prettier
  rev: v4.0.0-alpha.8
  hooks:
    - id: prettier
      types_or: [markdown, yaml]
```
