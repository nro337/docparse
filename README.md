<!-- Create readme for docparse -->
# docparse
Tool for parsing academic papers I'm reading and extracting key information.

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) 

## Requirements
- Python 3.14+
- uv (for environment management)

## Packages
- uv
- ruff
- docling
- commitizen


## Development
To set up the development environment, run:
```bash
uv sync
source .venv/bin/activate
python main.py
```

To add new packages, use:
```bash
uv add <package-name>
```

To add commits
```bash
cz c
```

To bump version
```bash
cz bump
```

## Usage
Run the main script with:
```bash
python main.py
```

## To lint the code
Run:
```bash
ruff check
```

To format the code, run:
```bash
ruff format
```