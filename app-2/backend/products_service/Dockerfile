# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy from the monorepo root context
COPY backend-requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Run application
FROM python:3.11-slim

# Create a non-root user
RUN groupadd -r servicegroup && useradd -r -g servicegroup serviceuser

WORKDIR /app

# Copy virtual env from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy ONLY the products_service code from the root context
COPY backend/products_service/ .

# Ensure correct permissions
RUN chown -R serviceuser:servicegroup /app

USER serviceuser

EXPOSE 5002

CMD ["opentelemetry-instrument", "gunicorn", "--bind", "0.0.0.0:5002", "app:app"]
