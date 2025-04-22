# 🚀 SWIFT Codes API

A high-performance, production-ready FastAPI application for managing and querying SWIFT/BIC codes, featuring Redis caching, Prometheus monitoring, and automated testing.

---

## ✨ Features

- **RESTful API** for managing SWIFT codes (CRUD)
- **Redis caching** for fast repeated queries
- **SQLAlchemy ORM** with SQLite (easy to switch to PostgreSQL/MySQL)
- **Prometheus** metrics for monitoring
- **Dockerized** for easy deployment
- **Automated testing** with Pytest
- **Interactive API docs** via Swagger UI & ReDoc

---

## 🗂️ Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── project/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── monitoring.py
│   └── ...
└── tests/
    └── test_api.py
```

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Rac00nCanFly/SWIFT_codes_python.git
cd SWIFT_codes_python
```

### 2. Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will:
- Build the FastAPI app image
- Start the app on [http://localhost:8080](http://localhost:8080)
- Start Redis on port 6379

---

## 📚 API Documentation

- **Swagger UI:** [http://localhost:8080/v1/docs](http://localhost:8080/v1/docs)  
- **ReDoc:** [http://localhost:8080/v1/redoc](http://localhost:8080/v1/redoc)

---

## 🛠️ Configuration

Configuration is primarily handled via `docker-compose.yml`:

```yaml
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      redis:
        condition: service_healthy

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    ports:
      - "6379:6379"
```

> ℹ️ You can override the Redis connection string using the `REDIS_URL` environment variable.

---

## 📦 Dependencies

Listed in `requirements.txt`:

```txt
fastapi>=0.68.0
uvicorn==0.29.0
fastapi-redis-cache==0.5.0
pandas==2.2.3
pydantic==2.11.3
pytest==8.3.4
redis==5.0.3
SQLAlchemy==2.0.37
prometheus-client==0.20.0
fastapi-prometheus-exporter==0.4.0
httpx==0.27.0
```

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/swift-codes` | POST | Create a new SWIFT code |
| `/v1/swift-codes/{swift_code}` | GET | Get details for a SWIFT code |
| `/v1/swift-codes/{swift_code}` | DELETE | Delete a SWIFT code |
| `/v1/swift-codes/country/{country_iso2}` | GET | List all SWIFT codes for a country |

### 📌 Example: Create a SWIFT code

```bash
curl -X POST http://localhost:8080/v1/swift-codes \
-H "Content-Type: application/json" \
-d '{
  "swiftCode": "TESTCODEXXX",
  "bankName": "Test Bank",
  "address": "Test Address",
  "countryISO2": "PL",
  "countryName": "Poland",
  "isHeadquarter": true
}'
```

---

## 📊 Monitoring

Prometheus metrics available at:

> [http://localhost:8080/metrics](http://localhost:8080/metrics)

### Setup with Grafana:

1. Add Prometheus as a data source  
   → URL: `http://localhost:9090`  
2. Import a dashboard (e.g., ID **11074**)

---

## 🧪 Running Tests

Run all tests inside the container:

```bash
docker-compose run app pytest tests/ -v
```

Run a specific test:

```bash
docker-compose run app pytest tests/test_api.py::test_create_and_get_swift_code -v
```

---

## 🧱 Customization

- **Switch database**: Edit `project/database.py` and install the appropriate driver.
- **Add endpoints**: Update `project/main.py` and corresponding models in `project/schemas.py`.
- **Static files/templates**: See [FastAPI’s template docs][4].

---

