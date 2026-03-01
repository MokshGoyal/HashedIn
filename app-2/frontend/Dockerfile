# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy from the monorepo root context
COPY frontend-requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Run application
FROM python:3.11-slim

# Create a non-root user
RUN groupadd -r frontgroup && useradd -r -g frontgroup frontuser

WORKDIR /app

# Copy virtual env from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy ONLY the frontend code from the root context
COPY frontend/ .

# Ensure correct permissions
RUN chown -R frontuser:frontgroup /app

USER frontuser

EXPOSE 5000

CMD ["opentelemetry-instrument", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
