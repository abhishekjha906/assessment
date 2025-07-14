# Use official Python image
FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy app code
COPY app/ /app/app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Environment variables for DB
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=hrdb
ENV POSTGRES_USER=hruser
ENV POSTGRES_PASSWORD=hrpass

# Start FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
