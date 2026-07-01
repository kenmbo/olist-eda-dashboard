# Start with a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Deps
COPY requirements-min.txt .
RUN pip install --no-cache-dir -r requirements-min.txt

# Coopy main repo files
COPY . .

# Create data directory (if it doesn't exist)
RUN mkdir -p data

# Curl from my cloud storage
RUN apt-get update && apt-get install -y curl && \
    curl -o data/olist.sqlite "https://storage.googleapis.com/olist-dashboard-assets-123/olist.sqlite" && \
    apt-get clean

CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}

