```bash
etf-watchdog-api/
├── LICENSE
├── app/        # Main application package
│   ├── __init__.py
│   ├── dependencies/
│   ├── internal/        # Internal modules not exposed to external users
│   │   ├── __init__.py
│   │   └── database.py     # Database connection and session management
│   ├── main.py         # Main application entry point
│   ├── routers/
│   │   ├── __init__.py
│   │   └── stocks.py       # Router for stock-related endpoints
│   └── services/
│       ├── __init__.py
│       └── stock_service.py        # Service layer for stock-related operations
│       └── logger_service.py       # Service layer for logging
├── docs/
│   ├── architecture/
│   │   ├── DESIGN.md       # Design documentation
│   │   └── LOGGER.md       # Documentation for the logger service
│   ├── deployment/
│   │   └── DOCKER.md       # Documentation for Docker usage
│   ├── learning/
│   │   ├── COPILOT.md      # Documentation for GitHub Copilot usage
│   │   └── REFERENCES.md   # Reference links for tutorials
│   └── tutorial-snippets/
│       └── basics          # Basic tutorial snippets
├── logs/       # Directory for log placement
├── logging_config.json         # Logging configuration
├── pyproject.toml
```
