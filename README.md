# ETF Watchdog API 🐕📈

A high-performance, asynchronous REST API built with **FastAPI** to track ETF and stock prices. This project leverages the **Twelve Data API** for real-time and historical market data, designed for speed and modern Python standards.

> **Note:** This is a personal project under active development.

## 🚀 Key Features

- **FastAPI Powered:** Built on Python 3.14+ for high performance and strict typing.
- **Asynchronous:** Uses `aiohttp` for non-blocking external API requests.
- **Modern Tooling:** Managed by `uv` for lightning-fast dependency resolution.
- **Docker Ready:** Includes a multi-stage Dockerfile for easy containerization.
- **Market Data:** Integrates seamlessly with Twelve Data.

## 🛠️ Tech Stack

- **Framework:** FastAPI, Pydantic
- **Language:** Python 3.14+
- **Package Manager:** uv
- **Data Source:** Twelve Data API
- **Database:** SQLModel / SQLite

## ⚡ Getting Started

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) installed

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/etf-watchdog-api.git
    cd etf-watchdog-api
    ```

2.  **Sync dependencies:**
    ```bash
    uv sync
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory and add your Twelve Data API key:
    ```env
    TWELVE_DATA_API_KEY=your_api_key_here
    ```

### Running the Application

**Local Development:**
```bash
uv run fastapi dev app/main.py
```
The API will be available at `http://127.0.0.1:8000`.

**Docker:**
```bash
docker build -t etf-watchdog .
docker run -p 8000:8000 --env-file .env etf-watchdog
```

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/stocks/` | List all tracked stocks. |
| `GET` | `/api/stocks/{symbol}?price=true` | Get current price details for a symbol. |
| `GET` | `/api/stocks/{symbol}?date=YYYY-MM-DD` | Get historical close price for a specific date. |
