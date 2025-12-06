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
