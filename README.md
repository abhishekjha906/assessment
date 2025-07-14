# HR Employee Search API

A Python FastAPI microservice for searching an HR company's employee directory. Supports multi-tenant safety, dynamic output columns, rate limiting, and is containerized for scalable deployment.

## Features
- Search employees with filters: firstname, lastname, contact, department, position, location, status
- Dynamic output columns per organization
- Multi-tenant safety (no data leaks between organizations)
- Naive in-memory rate limiting (no external libraries)
- Simulated sharded, indexed in-memory DB for scalability
- OpenAPI documentation
- Containerized with Docker
- Unit tested

## Setup (Unix-based)

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd assessment
   ```
2. **Start services with Docker Compose**
   ```sh
   docker-compose up --build
   ```
   This will start both the FastAPI service and a PostgreSQL database.
3. **Access API docs**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs)

## Database
- PostgreSQL is used for employee data storage.
- Default credentials (see `docker-compose.yml`):
  - DB: hrdb
  - User: hruser
  - Password: hrpass
  - Host: db

## Usage
- All requests must include the `X-Org-Id` header for multi-tenant safety.
- Use `/search` endpoint with POST method and JSON body for filters and columns.

## Testing
- Unit tests are in the `app/tests/` directory.
- To run tests (requires pytest):
   ```sh
   pip install pytest
   pytest app/tests/
   ```

## Notes
- Only Python standard libraries and FastAPI dependencies are used (except for testing).
- Rate limiting is naive and in-memory; for production, use a distributed solution.
- DB is simulated in-memory for demonstration; replace with a real DB for production.
