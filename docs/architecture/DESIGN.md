```bash
etf-watchdog-api/
├── LICENSE
├── Dockerfile
├── backend/        # Main application package
│   ├── __init__.py
│   ├── internal/        # Internal modules not exposed to external users
│   │   ├── __init__.py
│   │   └── models.py       # Internal data models
│   ├── main.py         # Main application entry point
│   ├── routers/
│   │   ├── __init__.py
│   │   └── stocks.py       # Router for stock-related endpoints
│   └── services/
│       ├── __init__.py
│       ├── app_state.py            # Shared application state
│       ├── lifespan.py             # Lifespan startup/shutdown management
│       ├── logger_service.py       # Service layer for logging
│       └── stock_service.py        # Service layer for stock-related operations
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── test_stocks.py
│   └── services/
│       ├── __init__.py
│       └── test_stock_service.py
├── docs/
│   ├── architecture/
│   │   ├── DESIGN.md       # Design documentation
│   │   └── LOGGER.md       # Documentation for the logger service
│   ├── deployment/
│   │   └── DOCKER.md       # Documentation for Docker usage
│   └── learning/
│       ├── COPILOT.md      # Documentation for GitHub Copilot usage
│       ├── REFERENCES.md   # Reference links for tutorials
│       └── tutorial-snippets/
│           ├── README.md
│           └── basics/     # Basic tutorial snippets
├── logs/       # Directory for log placement
├── logging_config.json         # Logging configuration
├── pyproject.toml
├── pytest.toml
└── README.md
```
