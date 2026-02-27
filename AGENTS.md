# Agent Guidelines for ETF Watchdog API

This document serves as the primary reference for AI agents and developers working in this repository.
Follow these guidelines strictly to maintain code quality, consistency, and stability.

## 1. Project Overview & Architecture

**ETF Watchdog API** is a personal ETF tracker built with FastAPI. It monitors stock prices using the Twelve Data API.

### Core Tech Stack
- **Language:** Python 3.14+ (Required)
- **Framework:** FastAPI
- **Package Manager:** `uv`
- **Type Checking:** `basedpyright`
- **Database:** SQLite (via SQLModel)
- **External API:** Twelve Data (Async `aiohttp` client)

### Directory Structure
```text
.
├── app/
│   ├── main.py              # Application entry point & lifespan management
│   ├── routers/             # API Route handlers (e.g., stocks.py)
│   ├── services/            # Business logic & External API clients
│   ├── internal/            # Database config & core utilities
│   └── __init__.py
├── docs/                    # Project documentation
│   ├── architecture/        # Architecture & Design docs (DESIGN.md, LOGGER.md)
│   ├── deployment/          # Deployment docs (DOCKER.md)
│   ├── learning/            # Learning notes & references (COPILOT.md, REFERENCES.md)
│   └── tutorial-snippets/   # Code snippets
├── logs/                    # Runtime logs (gitignored)
├── logging_config.json      # Logger configuration
├── pyproject.toml           # Project dependencies & tool config
├── uv.lock                  # Lockfile (DO NOT DELETE)
└── test.py                  # Ad-hoc testing script
```

## 2. Environment & Build Commands

Always use `uv` for dependency and environment management.

### Installation
1.  **Sync Dependencies:**
    ```bash
    uv sync
    ```
    *This creates/updates the `.venv` directory based on `uv.lock`.*

2.  **Environment Variables:**
    -   Ensure a `.env` file exists in the project root.
    -   Required keys (see `example.env` if available):
        -   `TWELVE_DATA_API_KEY`: API key for stock data.
        -   `NEWS_DATA_API_KEY `: API key for news data. (NOTE: This is not implemented yet.)

### Safety and Permissions

Ask first:
- Ask for permission to install Python dependencies using uv. i.e `uv add python-dotenv`.
- Never `git push` without authorization.
- Never delete any files or folders with permission.
- A good rule of thumb. If you think a human should be in the loop to authorize an action. Ask for permission!

### Running the Development Server
*   **Development Server (Hot Reload):**
    ```bash
    uv run fastapi dev app/main.py
    ```
    *Runs on `http://127.0.0.1:8000`.*

### Running the Docker container
*   **Example Container/Docker:**
    -   The `Dockerfile` uses a multi-stage `uv` build.
    -   Build: `docker build -t etf-watchdog .`
    -   Run: `docker run -p 8000:8000 --env-file .env etf-watchdog`

# !> [!IMPORTANT]
> Do not run Tests. Tests have not been implemented and are only used by me to test functions.

<!-- ### Testing & Verification -->
<!-- *   **Run Tests:** -->
<!--     Currently, use the manual test script. -->
<!--     ```bash -->
<!--     uv run python test.py -->
<!--     ``` -->
<!--     *Note: When refactoring, verify behavior with this script. If adding new features, consider adding a proper `pytest` suite in `tests/`.* -->
<!---->
<!-- *   **Type Checking (Critical):** -->
<!--     ```bash -->
<!--     uv run basedpyright -->
<!--     ``` -->
<!--     *Must pass before confirming any changes.* -->

## 3. Code Style & Conventions

Adhere to the existing style found in `app/`.

### Imports
Organize imports in the following order (refactor mixed imports when touching files):
1.  **Standard Library** (`os`, `logging`, `datetime`, `typing`)
2.  **Third-Party** (`fastapi`, `pydantic`, `sqlmodel`, `aiohttp`, `dotenv`)
3.  **Local Application** (`from .services...`, `from app.internal...`)

*   Use **relative imports** (e.g., `from ..services.stock_service import Stock`) within `app/routers/` and `app/services/`.
*   Avoid `import *`.

### Typing & Pydantic
*   **Strict Typing:** All function arguments and return values must have type hints.
*   **Syntax:** Use Python 3.10+ union syntax (`str | None`) instead of `Optional[str]`.
*   **FastAPI:** Use `Annotated` for dependencies and query parameters.
    ```python
    # Correct
    async def get_stock(
        symbol: Annotated[str, Path(min_length=1)],
        db: SessionDep
    ) -> dict: ...
    ```

### Asynchronous Patterns
*   The application is fully async.
*   Route handlers must be `async def`.
*   I/O bound service methods (DB, API calls) must be `async def`.
*   Use `aiohttp` for external requests (managed via `Stock` class singleton).
*   **Do not** use blocking `requests` library.

### Database (SQLModel)
*   Define models using `SQLModel`.
*   Use `table=True` for DB tables.
*   Access the database using the `SessionDep` dependency (in `app/internal/database.py`).
*   Config is currently SQLite (`sqlitedb.db`).

### Error Handling
*   Use `fastapi.HTTPException` for API errors.
*   Include descriptive `detail` messages.
*   Catch specific exceptions (e.g., `KeyError` in service layer) and re-raise as `HTTPException` in routers or handle gracefully.

### Logging
*   **Setup:** Logging is configured via `logging_config.json`.
*   **Usage:**
    ```python
    import logging
    logger = logging.getLogger(__name__)
    # ...
    logger.info("Fetching stock data...")
    logger.error("Failed to connect to API")
    ```
*   Ensure `setup_logging()` is called at the module level if necessary (refer to `app/routers/stocks.py`).

## 4. Agent Operational Rules

1.  **Analysis First:** Before editing, run `ls -R` or `glob` to understand the structure and `read` relevant files.
2.  **Incremental Changes:** Make small, verifiable changes.
3.  **Verification:**
    -   After editing, ALWAYS run `uv run basedpyright` to check for type errors.
    -   Run `uv run python test.py` to ensure runtime stability.
4.  **Secrets Safety:** NEVER commit API keys or secrets. Use `os.getenv` and `.env` files.
5.  **Documentation:** Update `AGENTS.md` if you introduce new tools or patterns.
6.  **Refactoring:** If you encounter legacy code (e.g., mixed imports), clean it up only if it relates to your current task.
