# NORI-server

## Setup

### 1. Install Poetry

Follow the instructions of the [official installation guide](https://python-poetry.org/docs/#installation).

### 2. (Optional) Configure Poetry

```sh
poetry config virtualenvs.in-project true
poetry env use $(which python)
```

### 3. Start the virtual environment

```sh
poetry env activate
```

### 4. Install dependencies

```sh
poetry sync --no-root
```

### 5. Start the server

```sh
poetry run python src/main.py
```

## Update API version

If you, as a developer, want to implement the API of another version, follow the instructions:

### 1. Setup the environment

```sh
poetry sync --no-root --extras dev
poetry env activate
```

### 2. Change the API version

```sh
cd protos
git checkout <version>
```

Change `<version>` to the version you want.

### 3. Generate codes from .proto files

```sh
poetry run python scripts/generate.py
```

> [!NOTE]
> The generate script use the [Protoletariat](https://github.com/cpcloud/protoletariat) to fix the path problem. If you encounter the "File Not Found Error" (especially in Windows), try to add the parent directory path of the `protol` command execution file to the `PATH` environment variable. (Or just copy the file into your Python bin directory, though it's not a good idea.)

### 4. Development

Programming, Commit, Open PR.

## Lint and format

Before commit and PR, please run `ruff check`, `ruff format`, `mypy .` to check and format the code.
