```bash
etf-watchdog-api/
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
├── docs/
│   ├── COPILOT.md      # Documentation for GitHub Copilot usage
│   ├── DESIGN.md      # Design documentation
│   └── tutorial-snippets/
│       ├── REFERENCES.md    # Reference links for tutorials
│       └── basics      # Basic tutorial snippets
├── pyproject.toml
```
