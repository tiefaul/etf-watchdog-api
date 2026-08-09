# ETF Watchdog API 🐕📈

A full-stack ETF tracker with a high-performance **FastAPI** backend and a new **SvelteKit** frontend. The backend leverages the **Twelve Data API** for real-time and historical market data, while the frontend provides a modern UI for viewing tracked symbols.

> **Note:** This is a personal project under active development.

## Key Features

- **FastAPI Powered:** Built on Python 3.14+ for high performance and strict typing.
- **Asynchronous:** Uses `aiohttp` for non-blocking external API requests.
- **Svelte Frontend:** Includes a SvelteKit + Tailwind CSS client app under `frontend/`.
- **Test Coverage:** Includes both synchronous and asynchronous tests for services and routers.
- **Modern Tooling:** Managed by `uv` for lightning-fast dependency resolution.
- **Docker Ready:** Includes a multi-stage Dockerfile for easy containerization.
- **Market Data:** Integrates seamlessly with Twelve Data.

## Tech Stack

- **Backend Framework:** FastAPI, Pydantic, SQLModel
- **Frontend Framework:** SvelteKit (Svelte 5), Tailwind CSS
- **Languages:** Python 3.14+, TypeScript/JavaScript
- **Package Managers:** uv (backend), npm/pnpm (frontend)
- **Data Sources:** Twelve Data API, Newsdata.io
- **Database:** SQLite

## Getting Started

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) installed
- Node.js 20+ (for the Svelte frontend)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/etf-watchdog-api.git
    cd etf-watchdog-api
    ```

2.  **Sync backend dependencies:**
    ```bash
    uv sync
    ```

3.  **Install frontend dependencies:**
    ```bash
    cd frontend
    npm install
    ```

4.  **Configure Environment:**
    Create a `.env` file in the root directory and add your Twelve Data and NewsData.io API keys:
    ```env
    TWELVE_DATA_API_KEY=your_twelve_data_api_key_here
    NEWS_DATA_API_KEY=your_news_data_api_key_here
    ```

### Running the Application

**Local Development:**

Start the backend:
```bash
uv run fastapi dev backend/main.py
```
Start the frontend in a second terminal:
```bash
cd frontend
npm run dev
```

- API: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173`

**Docker:**
```bash
docker build -t etf-watchdog .
docker run -p 8000:8000 --env-file .env etf-watchdog
```

## Testing

Sync and async tests live under `tests/`.

```bash
uv run pytest tests
```

## Documentation

Project docs live under `docs/` and are organized by purpose:

- `docs/architecture/` covers project structure and backend/frontend design details.
- `docs/deployment/` includes Docker build and run guidance for local container usage.
- `docs/learning/` stores personal learning notes, reference links, and FastAPI tutorial snippets used as quick examples.

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/etfs/` | List all tracked stocks. |
| `POST` | `/api/etfs/` | Create a stock to track using a valid ticker symbol. |
| `DELETE` | `/api/etfs/{symbol}` | Delete a tracked symbol and its related price records. |
| `GET` | `/api/etfs/{symbol}/price` | Get current price details for a symbol. |
| `GET` | `/api/etfs/{symbol}/price?price_date=YYYY-MM-DD` | Get historical close price for a specific date. |
| `GET` | `/api/etfs/{symbol}/news` | Get the latest news articles for a specific stock. |
