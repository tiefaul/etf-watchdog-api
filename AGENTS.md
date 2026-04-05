# Agent Guidelines for ETF Watchdog API

This document serves as the primary reference for AI agents and developers working in this repository. Follow these guidelines strictly to maintain code quality, consistency, and stability.

---

## 1. Project Overview & Architecture

**ETF Watchdog API** is a personal ETF tracker built with FastAPI. It monitors stock prices using the Twelve Data API.

### Core Tech Stack
* **Language:** Python 3.14+ (Required)
* **Framework:** FastAPI
* **Package Manager:** `uv`
* **Type Checking:** `basedpyright`
* **Database:** SQLite (via SQLModel)
* **External API:** Twelve Data (Async `aiohttp` client)

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

---

## 2. Environment & Build Commands

Always use `uv` for dependency and environment management.

### Installation & Setup
1.  **Sync Dependencies:**
    ```bash
    uv sync
    ```
    *Creates/updates the `.venv` directory based on `uv.lock`.*

2.  **Environment Variables:**
    * Ensure a `.env` file exists in the project root.
    * Required keys (see `example.env` if available):
        * `TWELVE_DATA_API_KEY`: API key for stock data.
        * `NEWS_DATA_API_KEY`: API key for news data. *(Note: Not implemented yet).*

### Running the Development Server
* **Development Server (Hot Reload):**
    ```bash
    uv run fastapi dev app/main.py
    ```
    *Runs on `http://127.0.0.1:8000`.*

### Docker Deployment
* The `Dockerfile` uses a multi-stage `uv` build.
* **Build:** `docker build -t etf-watchdog .`
* **Run:** `docker run -p 8000:8000 --env-file .env etf-watchdog`

### Testing & Verification
> [!IMPORTANT]  
> **Do not run a test suite (e.g., `pytest`).** Automated tests have not been implemented.

* **Runtime Testing:** Use the manual test script to verify functions ad-hoc:
    ```bash
    uv run python test.py
    ```
* **Type Checking (Critical):** Must pass before confirming any changes.
    ```bash
    uv run basedpyright
    ```

---

## 3. Code Style & Conventions

Adhere to the existing style found in `app/`.

### Imports
Organize imports in the following order (refactor mixed imports when touching files):
1.  **Standard Library:** `os`, `logging`, `datetime`, `typing`
2.  **Third-Party:** `fastapi`, `pydantic`, `sqlmodel`, `aiohttp`, `dotenv`
3.  **Local Application:** `from .services...`, `from app.internal...`

* Use **relative imports** (e.g., `from ..services.stock_service import Stock`) within `app/routers/` and `app/services/`.
* Avoid `import *`.

### Typing & Pydantic
* **Strict Typing:** All function arguments and return values must have type hints.
* **Syntax:** Use Python 3.10+ union syntax (`str | None`) instead of `Optional[str]`.
* **FastAPI:** Use `Annotated` for dependencies and query parameters.
    ```python
    # Correct
    async def get_stock(
        symbol: Annotated[str, Path(min_length=1)],
        db: SessionDep
    ) -> dict: ...
    ```

### Asynchronous Patterns
* The application is fully async. Route handlers and I/O bound service methods (DB, API calls) must be `async def`.
* Use `aiohttp` for external requests (managed via `Stock` class singleton).
* **Do not** use the blocking `requests` library.

### Database (SQLModel)
* Define models using `SQLModel`. Use `table=True` for DB tables.
* Access the database using the `SessionDep` dependency (in `app/internal/database.py`).
* Config is currently SQLite (`sqlitedb.db`).

### Error Handling
* Use `fastapi.HTTPException` for API errors with descriptive `detail` messages.
* Catch specific exceptions (e.g., `KeyError` in the service layer) and re-raise as `HTTPException` in routers, or handle gracefully.

### Logging
* **Setup:** Logging is configured via `logging_config.json`. Ensure `setup_logging()` is called at the module level if necessary (refer to `app/routers/stocks.py`).
* **Usage:**
    ```python
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info("Fetching stock data...")
    logger.error("Failed to connect to API")
    ```

---

## 4. Agent Operational Rules & Safety

**When in doubt, ASK.** Proactive communication prevents mistakes.

### 4.1 Execution Protocols
1.  **Analysis First:** Before editing, use file-reading tools (like `glob` or `read`) to understand the structure. Do not use terminal commands for analysis without permission.
2.  **Plan Before Execution:** Present a clear plan of action. Outline intended steps and **WAIT FOR EXPLICIT USER APPROVAL** before modifying code or running **ANY** command in the terminal.
3.  **Incremental Changes:** Make small, verifiable changes. Clean up legacy code (e.g., mixed imports) only if it relates to the current task.
4.  **Verification:** Outline the verification commands (like `uv run basedpyright` or `uv run python test.py`) in your plan, but **DO NOT RUN THEM** until the user explicitly approves the command execution.
5.  **Secrets Safety:** NEVER commit API keys or secrets. Use `os.getenv` and `.env` files.
6.  **Documentation:** Update this `AGENTS.md` file if you introduce new tools or patterns.

### 4.2 Strict Permissions
**CRITICAL: ZERO-COMMAND POLICY WITHOUT APPROVAL.**
Always ask for explicit permission and clarification BEFORE:
* Executing **ANY** shell or terminal command using the Bash tool. This includes all `uv run` commands, testing, type-checking, `git` commands, or even read-only diagnostic commands. There are zero exceptions.
* Writing or modifying code if the user's intent or the implementation strategy is unclear.
* Installing new Python dependencies (e.g., `uv add <package>`).
* Deleting any files or directories.

> [!IMPORTANT]
> **A good rule of thumb:** If you think a human should be in the loop to authorize an action, choose a design direction, or confirm a destructive command—Stop and ask for permission!
