FROM python:3.9-slim

WORKDIR /app

# Install system dependencies needed for TensorFlow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies including ML libraries
COPY requirements.txt .
RUN pip install --no-cache-dir \
    protobuf==3.20.0 \
    Django==3.2.19 \
    djangorestframework==3.14.0 \
    psycopg2-binary==2.9.6 \
    requests==2.28.2 \
    gunicorn==21.2.0 \
    python-dotenv==1.0.0 \
    django-cors-headers==4.0.0 \
    dj-database-url==1.2.0 \
    numpy==1.21.0 \
    tensorflow-cpu==2.8.0 \
    scikit-learn==1.0.2 \
    joblib==1.1.0

# Copy project
COPY . .

# Create the templates directory
RUN mkdir -p /app/ai/templates/ai

# Create model directory
RUN mkdir -p /app/ai/models

# Add health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8006/health/ || exit 1

# Start the service
EXPOSE 8006
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8006