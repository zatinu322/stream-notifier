set shell := ["powershell.exe", "-c"]

lint:
    uvx --from editorconfig-checker ec ./src
    uvx ruff check ./src
    uvx --with pydantic --python 3.12 mypy .

format:
    uvx ruff check --fix ./src
