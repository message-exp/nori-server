# nori-server

## Setup the environment

### Dev container (recommend)

1. Install [Docker](https://www.docker.com/).

2. If you're using Windows OS, connect to WSL first.

3. Open the project directory.

4. Select "Reopen in Container" and wait until the process is complete.

### Local

1. Install Python (recommend using [pyenv](https://github.com/pyenv/pyenv) or [uv](https://docs.astral.sh/uv/concepts/python-versions/#requesting-a-version)).

2. Install [Poetry](https://python-poetry.org/docs/#installation).

3. (Optional) Configure Poetry.

    ```sh
    poetry config virtualenvs.in-project true
    poetry env use $(which python)
    ```

4. Install dependencies.

    ```sh
    poetry install --extras dev
    ```

## Start the server

1. Activate the Python virtual environment.

    ```sh
    eval $(poetry env activate)
    ```

2. Pull files in git submodule.

    ```sh
    git submodule update --init --recursive
    ```

3. Generate codes from protos.

    ```sh
    python scripts/generate.py
    ```

4. Start the server.

    ```sh
    python src/main.py
    ```

## Update Nori API version

If you, as a developer, want to implement the API of another version, follow the instructions:

1. Setup the environment (follow the instructions above).

2. Start the server to ensure your dev environment has been set up. You can stop the server once it starts successfully.

3. Change the API version.

    ```sh
    cd protos
    git checkout <version>
    ```

    Change `<version>` to the version you want.

4. Generate codes from .proto files.

    ```sh
    python scripts/generate.py
    ```

> [!NOTE]
> The generate script use the [Protoletariat](https://github.com/cpcloud/protoletariat) to fix the path problem. If you encounter the "File Not Found Error" (especially in Windows), try to add the parent directory path of the `protol` command execution file to the `PATH` environment variable. (Or just copy the file into your Python bin directory, though it's not a good idea.)

5. Modify the code and implement the new features in the new version.

## Development

Programming, Commit, Open PR.

## Database Migration

1. Create a New Migration Script  

```bash
cd src
alembic revision --autogenerate -m "{message}"
```

- Generates a new migration script based on changes in your SQLAlchemy models.  
- `-m "{message}"` adds a description to track changes.  


1. Upgrade the Database

```bash
cd src
alembic upgrade {revision_id}
```

- Upgrades the database schema to a specific migration version.  
- Use `head` to apply all migrations to the latest version:  
  ```bash
  alembic upgrade head
  ```


1. Downgrade the Database

```bash
cd src
alembic downgrade {revision_id}
```

- Rolls back the database schema to a specific migration version.  
- Use `-1` to revert only the last migration:  
  ```bash
  alembic downgrade -1
  ```


## Lint and format

Before commit and PR, please run `ruff check`, `ruff format`, `mypy .` to check and format the code.
