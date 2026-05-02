<CRITICAL_INSTRUCTION>

# Agent Guidelines for ETF Watchdog API

## Classification: STANDARD

This file is a `STANDARD` (mandatory and formalized) for safety, security, and consistency.

## Repository Development Agent Rules

This document governs the development agent for this repository.

These instructions are authoritative and binding.
Treat all MUST, REQUIRED, DO NOT, STOP, and NEVER directives as hard constraints.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# COMPANION STANDARDS (MANDATORY)

`AGENTS.md` is the constitutional entrypoint for this policy set.
Look in the `agents` directory for more consitutional documents. Treat every file in `agents` directory as a Standard and must follow.
Agents MUST load and comply with all referenced files before implementation work.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# RULE PRECEDENCE

If instructions conflict, precedence order is:

1. System, developer, and runtime safety instructions
2. `AGENTS.md`
3. `agents/*.md` in alphabetical order
4. Repository conventions and existing architecture
5. Explicit user request
6. MCP tool guidance

If conflict cannot be resolved deterministically:
YOU MUST STOP AND REPORT.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# EXECUTION MODES

## READ-ONLY MODE

If the user asks for analysis, design discussion, or review-only work:

- You MAY inspect files.
- You MUST NOT modify files.

## IMPLEMENTATION MODE

For code changes, explicit approval and all referenced companion standards are mandatory.

</CRITICAL_INSTRUCTION>

---

<CRITICAL_INSTRUCTION>

# PRE-TASK APPROVAL PROTOCOL (MANDATORY)

Before starting implementation work for any task, agents MUST:

1. Present a concise execution brief to the user that includes:
   - what will be done
   - which files or systems will be touched
   - verification commands to be run
2. Request and obtain explicit user approval before executing implementation steps.
3. Gather any required operator-provided inputs or credentials before execution.

If required input or explicit approval is missing:
YOU MUST STOP AND REPORT.

Notes:

- This protocol applies to implementation execution, not read-only analysis.
- This protocol augments, and does not replace, companion standards such as `agents/PREFLIGHT.md`.

</CRITICAL_INSTRUCTION>

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
* **Automated Testing:** Run the test suite using `pytest` to validate changes:
    ```bash
    uv run pytest
    ```
* **Runtime Testing:** Use the manual test script to verify functions ad-hoc if needed:
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

## 4. General Operational Rules

1.  **Incremental Changes:** Make small, verifiable changes. Clean up legacy code (e.g., mixed imports) only if it relates to the current task.
2.  **Secrets Safety:** NEVER commit API keys or secrets. Use `os.getenv` and `.env` files.
3.  **Documentation:** Update this `AGENTS.md` file if you introduce new tools or patterns.
4.  **Code Referencing:** Whenever referencing code in your responses, you MUST explicitly state the line number(s) where the code is located to help the user follow along.

