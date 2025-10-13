```bash
stock_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py               # Entry point of your FastAPI app
│   ├── core/
│   │   ├── config.py         # Configuration (API keys, settings, env variables)
│   │   └── logger.py         # Optional logging setup
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py         # Combines all routes together
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── stocks.py     # Routes for getting stock data
│   │       └── health.py     # Health check or testing route
│   ├── services/
│   │   ├── __init__.py
│   │   ├── stock_service.py  # Logic for fetching stock info (e.g., using yfinance)
│   ├── models/
│   │   ├── __init__.py
│   │   └── stock_model.py    # Pydantic models (schemas)
│   └── utils/
│       ├── __init__.py
│       └── helpers.py        # Optional helpers like date validation
│
├── requirements.txt
└── README.md
```
