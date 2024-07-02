# cinnamon-ai-bootcamp-w1

The homework for Cinnamon AI Bootcamp Week 1. The project is a OCR Script that can read all text lines from documents

## Features

- Convert [`.png`, `.tiff`, `.pdf`, `.docx`, `.heic`] to images.
- Extract text from images using OCR.
- (Optional) Upload result to cloud system.

## How to use

### 1. Install Poetry:

- Linux, MacOS, Windows (WSL): `curl -sSL https://install.python-poetry.org | python3 -`
- Windows: create `venv`, then `pip install poetry`

### 2. Install all the dependencies:

- Use `poetry install`

### 3. Install poppler:

- For MacOS: `brew install poppler`
- For Ubuntu/Linux: `sudo apt update`

  `sudo apt install poppler-utils`

- For Windows: https://poppler.freedesktop.org

### 4. Run all the files:

- To run the script: `poetry run python your_script.py`
- To run the tests: `poetry run pytest`

### 5. Libraries/Dependencies management:

- Add new dependency / install new library: `poetry add <package-name>`
- Update dependencies and `poetry.lock` file: `poetry update <package-name>`
- Remove dependencies: `poetry remove <package-name>`

### 6. Other commands:

- Activate the environment: `poetry shell`
- Deactivate the environement: `exit`
- To learn more, go to [this link](https://python-poetry.org/docs/cli/)
