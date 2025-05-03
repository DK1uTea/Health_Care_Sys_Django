FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for ML libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create model directory
RUN mkdir -p /app/models/diagnostic

# Run migrations and start server
EXPOSE 8006
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8006"]