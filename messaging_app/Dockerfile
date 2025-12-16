# Dockerfile - Fixed Version
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# REMOVE this line or ensure messaging_app exists:
# ENV DJANGO_SETTINGS_MODULE=messaging_app.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create non-root user (optional - comment out if causing issues)
RUN useradd -m -u 1000 django \
    && chown -R django:django /app
USER django

# REMOVE collectstatic or add conditional check
# RUN python manage.py collectstatic --noinput || echo "Skipping collectstatic"

# Expose port
EXPOSE 8000

# Use simpler command first, then switch to gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Once working, change to:
# CMD ["sh", "-c", "python manage.py migrate && gunicorn messaging_app.wsgi:application --bind 0.0.0.0:8000 --workers 3"]


echo "Mapping: Host port 8000 -> Container port 8000"
docker run -d \
  --name messaging-container \
  -p 8000:8000 \  
  messaging-app

############ UPDATE tasks 3 #########
# Multi-stage build for smaller final image

# Stage 1: Builder
FROM python:3.10-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libmariadb-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies in virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim as runtime

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -s /bin/false appuser

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libmariadb-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/logs \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "alx_travel_app.wsgi:application"]
