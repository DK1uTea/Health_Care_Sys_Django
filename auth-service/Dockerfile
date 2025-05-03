FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Start command with retry logic
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]