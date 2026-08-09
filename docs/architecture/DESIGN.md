```bash
etf-watchdog-api/
|-- LICENSE
|-- Dockerfile
|-- backend/                     # FastAPI backend application package
|   |-- __init__.py
|   |-- internal/                # Internal modules not exposed externally
|   |   |-- __init__.py
|   |   `-- models.py            # Internal data models
|   |-- main.py                  # Backend entry point
|   |-- routers/
|   |   |-- __init__.py
|   |   `-- stocks.py            # Stock/ETF API route handlers
|   `-- services/
|       |-- __init__.py
|       |-- app_state.py         # Shared application state
|       |-- lifespan.py          # Startup/shutdown lifecycle handlers
|       |-- logger_service.py    # Logging service layer
|       `-- stock_service.py     # Market data service layer
|-- frontend/                    # SvelteKit frontend client
|   |-- src/
|   |   |-- app.d.ts
|   |   |-- app.html             # HTML shell for Svelte app
|   |   |-- error.html
|   |   |-- lib/
|   |   |   |-- assets/
|   |   |   `-- components/      # Reusable UI components
|   |   `-- routes/              # SvelteKit routes/pages
|   |-- static/                  # Static assets served directly
|   |-- package.json
|   |-- tsconfig.json
|   `-- vite.config.ts
|-- tests/
|   |-- __init__.py
|   |-- conftest.py
|   |-- routers/
|   |   |-- __init__.py
|   |   `-- test_stocks.py
|   `-- services/
|       |-- __init__.py
|       `-- test_stock_service.py
|-- docs/
|   |-- architecture/
|   |   |-- DESIGN.md            # High-level repository structure
|   |   `-- LOGGER.md            # Logger service and configuration details
|   |-- deployment/
|   |   `-- DOCKER.md            # Docker build/run instructions
|   `-- learning/
|       |-- COPILOT.md
|       |-- REFERENCES.md
|       `-- tutorial-snippets/
|           |-- README.md
|           `-- basics/
|-- logs/                        # Runtime log files
|-- logging_config.json          # Logging configuration
|-- pyproject.toml
|-- pytest.toml
`-- README.md
```
